from __future__ import annotations

import argparse

from .embedder import Embedder
from .ingest import ingest_cases
from .normalize import normalize_scotus, normalize_uscode
from .retriever import search
from .validate import validate_cases


def main() -> None:
    parser = argparse.ArgumentParser(description="AI Legal Intelligence CLI")
    parser.add_argument(
        "command",
        choices=["ingest", "query", "normalize", "validate"],
        help="Operation to perform",
    )
    parser.add_argument("--text", dest="text", help="Query text for retrieval")
    parser.add_argument(
        "--top-k", dest="top_k", type=int, default=3, help="Top K results"
    )
    # Normalize options
    parser.add_argument(
        "--adapter",
        choices=["scotus", "uscode"],
        default="scotus",
        help="Normalization adapter (default: scotus)",
    )
    parser.add_argument(
        "--source",
        help="Path to source JSON/JSONL file",
    )
    parser.add_argument(
        "--out",
        dest="out",
        help="Output directory for normalized cases (defaults to data/cases)",
    )
    parser.add_argument(
        "--source-tag", dest="source_tag", help="Provenance label to include in outputs"
    )
    parser.add_argument(
        "--dry-run",
        dest="dry_run",
        action="store_true",
        help="Parse and report without writing files",
    )
    parser.add_argument(
        "--limit", dest="limit", type=int, help="Maximum records to process"
    )
    parser.add_argument(
        "--overwrite",
        dest="overwrite",
        action="store_true",
        help="Overwrite files instead of appending counters",
    )
    parser.add_argument(
        "--rebuild",
        dest="rebuild",
        action="store_true",
        help="Rebuild vectors from scratch during ingest",
    )
    args = parser.parse_args()

    if args.command == "ingest":
        names, _ = ingest_cases(rebuild=args.rebuild)
        print(f"Ingested {len(names)} cases (rebuild={args.rebuild}).")
    elif args.command == "query":
        if not args.text:
            parser.error("--text is required for 'query'")
        emb = Embedder().encode_texts([args.text])[0]
        results = search(emb, top_k=args.top_k)
        for name, score in results:
            print(f"{name:<40} similarity={score:.3f}")
    elif args.command == "normalize":
        if not args.source:
            parser.error("--source is required for 'normalize'")
        from pathlib import Path

        out_dir = Path(args.out) if args.out else None
        src = Path(args.source)
        if args.adapter == "scotus":
            written = normalize_scotus(
                src,
                out_dir=out_dir,
                source_tag=args.source_tag,
                limit=args.limit,
                dry_run=args.dry_run,
                overwrite=args.overwrite,
            )
        elif args.adapter == "uscode":
            written = normalize_uscode(
                src,
                out_dir=out_dir,
                source_tag=args.source_tag,
                limit=args.limit,
                dry_run=args.dry_run,
                overwrite=args.overwrite,
            )
        else:
            parser.error(f"Unsupported adapter: {args.adapter}")
        dest = out_dir or "data/cases"
        print(f"Wrote {len(written)} normalized cases to {dest}")
        print(f"(dry_run={args.dry_run})")
    elif args.command == "validate":
        from pathlib import Path

        errors = validate_cases(Path(args.out) if args.out else None)
        if not errors:
            print("Validation passed: all cases valid.")
        else:
            for file, msg in errors:
                print(f"{file}: {msg}")
            raise SystemExit(1)


if __name__ == "__main__":
    main()

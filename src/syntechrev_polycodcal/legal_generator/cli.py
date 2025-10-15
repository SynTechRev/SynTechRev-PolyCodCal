from __future__ import annotations

import argparse
import sys

from .embedder import Embedder
from .ingest import ingest_cases
from .normalize import normalize_amjur, normalize_blacks, normalize_scotus, normalize_uscode
from .retriever import search
from .validator import validate_cases


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
        choices=["scotus", "uscode", "blacks", "amjur"],
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
        "--source-tag",
        dest="source_tag",
        help="Provenance label applied to all records in a batch",
    )
    parser.add_argument(
        "--dry-run",
        dest="dry_run",
        action="store_true",
        help="Parse and report counts without writing files",
    )
    parser.add_argument(
        "--limit",
        dest="limit",
        type=int,
        help="Process at most N records",
    )
    parser.add_argument(
        "--overwrite",
        dest="overwrite",
        action="store_true",
        help="Replace files with same stem; default append-with-counter",
    )
    # Ingest options
    parser.add_argument(
        "--rebuild",
        dest="rebuild",
        action="store_true",
        help="Rebuild vectors from scratch (default: append)",
    )
    # Validate options
    parser.add_argument(
        "--dir",
        dest="dir",
        help="Directory containing case files to validate (default: data/cases)",
    )
    args = parser.parse_args()

    if args.command == "ingest":
        mode = "rebuild" if args.rebuild else "append"
        names, _ = ingest_cases(rebuild=args.rebuild)
        print(f"Ingested {len(names)} cases (mode: {mode}).")
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
        
        kwargs = {
            "out_dir": out_dir,
            "source_tag": args.source_tag,
            "dry_run": args.dry_run,
            "limit": args.limit,
            "overwrite": args.overwrite,
        }
        
        if args.adapter == "scotus":
            written = normalize_scotus(src, **kwargs)
        elif args.adapter == "uscode":
            written = normalize_uscode(src, **kwargs)
        elif args.adapter == "blacks":
            written = normalize_blacks(src, **kwargs)
        elif args.adapter == "amjur":
            written = normalize_amjur(src, **kwargs)
        else:
            parser.error(f"Unsupported adapter: {args.adapter}")
        
        if not args.dry_run:
            print(
                f"Wrote {len(written)} normalized cases to {(out_dir or 'data/cases')}"
            )
    elif args.command == "validate":
        from pathlib import Path

        case_dir = Path(args.dir) if args.dir else None
        errors = validate_cases(case_dir)
        if errors:
            print(f"Validation failed with {len(errors)} error(s):")
            for err in errors:
                print(f"  - {err}")
            sys.exit(1)
        else:
            print("Validation passed: all cases conform to schema.")
            sys.exit(0)


if __name__ == "__main__":
    main()

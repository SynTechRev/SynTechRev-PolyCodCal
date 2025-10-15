from __future__ import annotations

import argparse

from .embedder import Embedder
from .ingest import ingest_cases
from .normalize import normalize_scotus
from .retriever import search


def main() -> None:
    parser = argparse.ArgumentParser(description="AI Legal Intelligence CLI")
    parser.add_argument(
        "command", choices=["ingest", "query", "normalize"], help="Operation to perform"
    )
    parser.add_argument("--text", dest="text", help="Query text for retrieval")
    parser.add_argument(
        "--top-k", dest="top_k", type=int, default=3, help="Top K results"
    )
    # Normalize options
    parser.add_argument(
        "--adapter",
        choices=["scotus"],
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
    args = parser.parse_args()

    if args.command == "ingest":
        names, _ = ingest_cases()
        print(f"Ingested {len(names)} cases.")
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
            written = normalize_scotus(src, out_dir=out_dir)
        else:
            parser.error(f"Unsupported adapter: {args.adapter}")
        print(f"Wrote {len(written)} normalized cases to {(out_dir or 'data/cases')}")


if __name__ == "__main__":
    main()

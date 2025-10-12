from __future__ import annotations

import argparse

from .embedder import Embedder
from .ingest import ingest_cases
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
        msg = (
            "Normalize mode is a placeholder. See docs/PHASE6_INGESTION.md "
            "for normalization schema and adapters."
        )
        print(msg)


if __name__ == "__main__":
    main()

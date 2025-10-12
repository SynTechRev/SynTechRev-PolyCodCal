from __future__ import annotations

import argparse

from .embedder import Embedder
from .ingest import ingest_cases
from .normalize import normalize_private, normalize_scotus, normalize_uscode
from .retriever import search


def main() -> None:
    parser = argparse.ArgumentParser(description="AI Legal Intelligence CLI")
    subparsers = parser.add_subparsers(dest="command", help="Operation to perform")

    # Ingest command
    subparsers.add_parser("ingest", help="Ingest normalized cases and build embeddings")

    # Query command
    query_parser = subparsers.add_parser("query", help="Search for similar cases")
    query_parser.add_argument("--text", dest="text", required=True, help="Query text")
    query_parser.add_argument(
        "--top-k", dest="top_k", type=int, default=3, help="Top K results"
    )

    # Normalize command with subcommands
    normalize_parser = subparsers.add_parser(
        "normalize", help="Normalize raw data sources"
    )
    normalize_subparsers = normalize_parser.add_subparsers(
        dest="source", help="Data source to normalize"
    )

    # SCOTUS normalization
    scotus_parser = normalize_subparsers.add_parser(
        "scotus", help="Normalize Supreme Court opinions"
    )
    scotus_parser.add_argument(
        "--parallel",
        action="store_true",
        default=True,
        help="Use parallel processing (default: True)",
    )
    scotus_parser.add_argument(
        "--no-parallel", action="store_false", dest="parallel", help="Disable parallel processing"
    )

    # US Code normalization
    uscode_parser = normalize_subparsers.add_parser(
        "uscode", help="Normalize U.S. Code sections"
    )
    uscode_parser.add_argument(
        "--parallel",
        action="store_true",
        default=True,
        help="Use parallel processing (default: True)",
    )
    uscode_parser.add_argument(
        "--no-parallel", action="store_false", dest="parallel", help="Disable parallel processing"
    )

    # Private sources normalization
    normalize_subparsers.add_parser(
        "private", help="Normalize proprietary sources (Black's Law, AmJur)"
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    if args.command == "ingest":
        names, _ = ingest_cases()
        print(f"Ingested {len(names)} cases.")
    elif args.command == "query":
        emb = Embedder().encode_texts([args.text])[0]
        results = search(emb, top_k=args.top_k)
        if results:
            for name, score in results:
                print(f"{name:<40} similarity={score:.3f}")
        else:
            print("No results found. Did you run 'ingest' first?")
    elif args.command == "normalize":
        if not args.source:
            normalize_parser.print_help()
            return

        if args.source == "scotus":
            parallel = getattr(args, "parallel", True)
            paths = normalize_scotus(parallel=parallel)
            print(f"\n✓ Normalized {len(paths)} SCOTUS cases")
        elif args.source == "uscode":
            parallel = getattr(args, "parallel", True)
            paths = normalize_uscode(parallel=parallel)
            print(f"\n✓ Normalized {len(paths)} US Code sections")
        elif args.source == "private":
            paths = normalize_private()
            print(f"\n✓ Normalized {len(paths)} private source records")

        if paths:
            print(f"Next step: Run 'ingest' to build embeddings")


if __name__ == "__main__":
    main()

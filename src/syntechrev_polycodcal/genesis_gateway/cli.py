"""Command-line interface for Genesis Gateway.

Provides CLI commands for processing inspirations through the Genesis Gateway.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

from syntechrev_polycodcal.genesis_gateway import GenesisGateway


def process_command(args: argparse.Namespace) -> int:
    """Process an inspiration through the Gateway.

    Args:
        args: Command-line arguments

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    gateway = GenesisGateway(alignment_threshold=args.threshold)

    try:
        result = gateway.process(
            content=args.content,
            source=args.source,
            intent=args.intent,
            signature=args.signature,
        )

        if args.output == "json":
            # Convert datetime objects to strings for JSON serialization
            output_data = {
                "aligned": result["aligned"],
                "invocation": {
                    "intent": result["invocation"]["intent"],
                    "timestamp": result["invocation"]["timestamp"].isoformat(),
                    "signature": result["invocation"]["signature"],
                    "declaration": result["invocation"]["declaration"],
                },
                "inspiration": {
                    "content": result["inspiration"].content,
                    "source": result["inspiration"].source,
                    "timestamp": result["inspiration"].timestamp.isoformat(),
                },
                "construct": {
                    "truth": result["construct"]["truth"],
                    "faith": result["construct"]["faith"],
                    "justice": result["construct"]["justice"],
                    "mercy": result["construct"]["mercy"],
                    "axioms": result["construct"]["axioms"],
                    "constraints": result["construct"]["constraints"],
                },
            }

            if result["artifact"]:
                output_data["artifact"] = {
                    "name": result["artifact"].name,
                    "alignment_score": result["artifact"].alignment_score,
                    "seal": result["artifact"].seal,
                }

            print(json.dumps(output_data, indent=2))
        else:
            # Human-readable output
            print("=" * 80)
            print("GENESIS GATEWAY PROCESSING RESULT")
            print("=" * 80)
            print()
            print(f"Content:   {result['inspiration'].content[:60]}...")
            print(f"Source:    {result['inspiration'].source}")
            print(f"Aligned:   {result['aligned']}")
            print()
            print("Alignment Metrics:")
            print(f"  Truth:   {result['construct']['truth']:.3f}")
            print(f"  Faith:   {result['construct']['faith']:.3f}")
            print(f"  Justice: {result['construct']['justice']:.3f}")
            print(f"  Mercy:   {result['construct']['mercy']:.3f}")
            print()

            if result["artifact"]:
                print(f"✓ Artifact Compiled: {result['artifact'].name}")
                print(f"  Alignment Score: {result['artifact'].alignment_score:.3f}")
                print(f"  Seal: {result['artifact'].seal}")
            else:
                print("✗ Not aligned - artifact not compiled")

            print()

        return 0

    except Exception as e:
        print(f"Error processing inspiration: {e}", file=sys.stderr)
        return 1


def batch_command(args: argparse.Namespace) -> int:
    """Process multiple inspirations from a file.

    Args:
        args: Command-line arguments

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    gateway = GenesisGateway(alignment_threshold=args.threshold)

    try:
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"Error: Input file not found: {args.input}", file=sys.stderr)
            return 1

        with open(input_path, "r", encoding="utf-8") as f:
            inspirations = json.load(f)

        if not isinstance(inspirations, list):
            inspirations = [inspirations]

        results = gateway.batch_process(inspirations)

        if args.output == "json":
            # Simplified JSON output
            output_data = []
            for result in results:
                if "error" in result:
                    output_data.append({"error": result["error"]})
                else:
                    output_data.append(
                        {
                            "aligned": result["aligned"],
                            "source": result["inspiration"].source,
                            "artifact_created": result["artifact"] is not None,
                        }
                    )
            print(json.dumps(output_data, indent=2))
        else:
            print("=" * 80)
            print("GENESIS GATEWAY BATCH PROCESSING")
            print("=" * 80)
            print()
            print(f"Processed: {len(results)} inspirations")

            aligned_count = sum(1 for r in results if "error" not in r and r["aligned"])
            error_count = sum(1 for r in results if "error" in r)

            print(f"Aligned:   {aligned_count}")
            print(f"Rejected:  {len(results) - aligned_count - error_count}")
            print(f"Errors:    {error_count}")
            print()

            if args.verbose:
                for i, result in enumerate(results, 1):
                    if "error" in result:
                        print(f"{i}. ERROR: {result['error']}")
                    else:
                        status = "✓" if result["aligned"] else "✗"
                        print(
                            f"{i}. {status} {result['inspiration'].source} - "
                            f"{'Compiled' if result['artifact'] else 'Rejected'}"
                        )

        return 0

    except Exception as e:
        print(f"Error batch processing: {e}", file=sys.stderr)
        return 1


def report_command(args: argparse.Namespace) -> int:
    """Generate a Gateway activity report.

    Args:
        args: Command-line arguments

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    gateway = GenesisGateway(alignment_threshold=args.threshold)

    # Load previous state if specified
    if args.load:
        print("Note: State loading not implemented in this version", file=sys.stderr)

    # Process some sample data if needed
    print(gateway.generate_report())
    return 0


def reflect_command(args: argparse.Namespace) -> int:
    """Perform reflection and auto-audit.

    Args:
        args: Command-line arguments

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    gateway = GenesisGateway(alignment_threshold=args.threshold)

    # Note: In real usage, would load gateway state
    reflection = gateway.reflect()

    if args.output == "json":
        # Convert datetime to string
        output_data = dict(reflection)
        output_data["audit_timestamp"] = reflection["audit_timestamp"].isoformat()
        print(json.dumps(output_data, indent=2))
    else:
        print("=" * 80)
        print("GENESIS GATEWAY REFLECTION & AUTO-AUDIT")
        print("=" * 80)
        print()
        print(f"Total Inspirations:     {reflection['total_inspirations']}")
        print(f"Total Compiled:         {reflection['total_compiled']}")
        print(f"Alignment Pass Rate:    {reflection['alignment_pass_rate']:.1%}")
        print(f"Average Alignment:      {reflection['average_alignment_score']:.3f}")
        print(f"High Alignment (≥0.9):  {reflection['high_alignment_count']}")
        print()
        print(
            f"Mirrors Constants:      {'✓ YES' if reflection['mirrors_constants'] else '✗ NO'}"
        )
        print(f"Audit Timestamp:        {reflection['audit_timestamp'].isoformat()}")
        print()

    return 0


def main(argv: Optional[list[str]] = None) -> int:
    """Main CLI entry point.

    Args:
        argv: Command-line arguments (default: sys.argv[1:])

    Returns:
        Exit code
    """
    parser = argparse.ArgumentParser(
        description="Genesis Gateway - Creative Intelligence Layer",
        epilog='Example: genesis-gateway process "Divine wisdom guides all"',
    )

    parser.add_argument(
        "--threshold",
        type=float,
        default=0.8,
        help="Alignment threshold (default: 0.8)",
    )

    parser.add_argument(
        "--output",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Process command
    process_parser = subparsers.add_parser("process", help="Process an inspiration")
    process_parser.add_argument("content", help="Inspiration content")
    process_parser.add_argument(
        "--source", default="unknown", help="Source type (default: unknown)"
    )
    process_parser.add_argument("--intent", help="Declared intent")
    process_parser.add_argument("--signature", help="Numerological signature")

    # Batch command
    batch_parser = subparsers.add_parser(
        "batch", help="Process multiple inspirations from file"
    )
    batch_parser.add_argument("input", help="Input JSON file with inspirations")
    batch_parser.add_argument(
        "--verbose", "-v", action="store_true", help="Show detailed results"
    )

    # Report command
    report_parser = subparsers.add_parser("report", help="Generate activity report")
    report_parser.add_argument("--load", help="Load state from file")

    # Reflect command
    subparsers.add_parser("reflect", help="Perform reflection and auto-audit")

    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        return 1

    if args.command == "process":
        return process_command(args)
    elif args.command == "batch":
        return batch_command(args)
    elif args.command == "report":
        return report_command(args)
    elif args.command == "reflect":
        return reflect_command(args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Generate a report on legal data entries by doctrine and jurisdiction.

This script analyzes the legal case database and produces a Markdown summary
showing the distribution of cases across different legal doctrines and
jurisdictions.

Usage:
    python scripts/legal_data_report.py [--data-path DATA_PATH] [--output OUTPUT]

Arguments:
    --data-path: Path to legal cases directory (default: data/cases)
    --output: Output file path (default: stdout)

Example:
    python scripts/legal_data_report.py
    python scripts/legal_data_report.py --data-path data/cases --output report.md
"""

import argparse
import sys
from collections import Counter
from typing import Dict, List

from syntechrev_polycodcal.data_loader import load_legal_records
from syntechrev_polycodcal.schemas.legal_record import LegalRecord


def generate_report(records: List[LegalRecord]) -> str:
    """Generate a Markdown report from legal records.

    Args:
        records: List of LegalRecord objects to analyze

    Returns:
        Markdown-formatted report string
    """
    if not records:
        return "# Legal Data Report\n\nNo records found.\n"

    # Count by doctrine
    doctrine_counts = Counter(r.doctrine for r in records)

    # Count by jurisdiction
    jurisdiction_counts = Counter(r.jurisdiction for r in records)

    # Count by court
    court_counts = Counter(r.court for r in records)

    # Group by decade
    decade_counts: Dict[str, int] = {}
    for record in records:
        decade = (record.year // 10) * 10
        decade_key = f"{decade}s"
        decade_counts[decade_key] = decade_counts.get(decade_key, 0) + 1

    # Build report
    lines = [
        "# Legal Data Report",
        "",
        f"**Total Cases**: {len(records)}",
        f"**Date Range**: {min(r.year for r in records)}-{max(r.year for r in records)}",
        "",
        "## Cases by Legal Doctrine",
        "",
        "| Doctrine | Count | Percentage |",
        "|----------|-------|------------|",
    ]

    for doctrine, count in doctrine_counts.most_common():
        percentage = (count / len(records)) * 100
        lines.append(f"| {doctrine} | {count} | {percentage:.1f}% |")

    lines.extend(
        [
            "",
            "## Cases by Jurisdiction",
            "",
            "| Jurisdiction | Count |",
            "|--------------|-------|",
        ]
    )

    for jurisdiction, count in jurisdiction_counts.most_common():
        lines.append(f"| {jurisdiction} | {count} |")

    lines.extend(
        [
            "",
            "## Cases by Court",
            "",
            "| Court | Count |",
            "|-------|-------|",
        ]
    )

    for court, count in court_counts.most_common():
        lines.append(f"| {court} | {count} |")

    lines.extend(
        [
            "",
            "## Cases by Decade",
            "",
            "| Decade | Count |",
            "|--------|-------|",
        ]
    )

    for decade in sorted(decade_counts.keys()):
        lines.append(f"| {decade} | {decade_counts[decade]} |")

    lines.extend(
        [
            "",
            "## Case List",
            "",
            "| Year | Case Name | Doctrine |",
            "|------|-----------|----------|",
        ]
    )

    for record in sorted(records, key=lambda r: r.year):
        lines.append(f"| {record.year} | {record.case_name} | {record.doctrine} |")

    lines.extend(
        [
            "",
            "---",
            "",
            f"*Report generated from {len(records)} legal records*",
        ]
    )

    return "\n".join(lines)


def main() -> None:
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Generate a report on legal data entries"
    )
    parser.add_argument(
        "--data-path",
        default="data/cases",
        help="Path to legal cases directory (default: data/cases)",
    )
    parser.add_argument(
        "--output",
        help="Output file path (default: stdout)",
    )

    args = parser.parse_args()

    try:
        # Load records
        records = load_legal_records(args.data_path)

        # Generate report
        report = generate_report(records)

        # Output report
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(report)
            print(f"Report written to {args.output}", file=sys.stderr)
        else:
            print(report)

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

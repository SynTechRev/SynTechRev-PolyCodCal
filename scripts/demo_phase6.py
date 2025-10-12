#!/usr/bin/env python3
"""Phase 6 Demonstration Script

This script demonstrates the Phase 6 legal data ingestion system capabilities.
It creates sample data, normalizes it, ingests it, and performs queries.
"""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

# Add src to path for direct script execution
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from syntechrev_polycodcal.legal_generator.normalize import (
    normalize_scotus,
    normalize_uscode,
)
from syntechrev_polycodcal.legal_generator.ingest import ingest_cases
from syntechrev_polycodcal.legal_generator.retriever import search
from syntechrev_polycodcal.legal_generator.embedder import Embedder
from syntechrev_polycodcal.legal_generator.schema import validate_record


def print_header(text: str) -> None:
    """Print a formatted section header."""
    print(f"\n{'=' * 60}")
    print(f"  {text}")
    print(f"{'=' * 60}\n")


def demo_schema_validation() -> None:
    """Demonstrate schema validation."""
    print_header("Schema Validation Demo")

    # Valid record
    valid_record = {
        "case_name": "Test v. Example",
        "summary": "This is a test case summary.",
        "source": "scotus",
        "citation": "123 U.S. 456",
        "date": "2024-01-15",
    }

    print("Validating a valid record:")
    print(json.dumps(valid_record, indent=2))
    errors = validate_record(valid_record)
    print(f"✓ Validation result: {'Valid' if not errors else 'Invalid'}")

    # Invalid record
    invalid_record = {
        "case_name": "Test Case",
        # Missing summary
        "source": "invalid_source",
    }

    print("\nValidating an invalid record:")
    print(json.dumps(invalid_record, indent=2))
    errors = validate_record(invalid_record)
    if errors:
        print("✗ Validation errors:")
        for error in errors:
            print(f"  - {error}")


def demo_normalization() -> None:
    """Demonstrate normalization adapters."""
    print_header("Normalization Demo")

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)

        # Create sample SCOTUS JSON
        scotus_dir = tmp_path / "scotus"
        scotus_dir.mkdir()

        sample_scotus = {
            "case_name": "Demo v. Example",
            "opinion_text": "This is a sample Supreme Court opinion for demonstration.",
            "citation": "999 U.S. 123",
            "decision_date": "2024-01-15",
        }

        (scotus_dir / "demo_case.json").write_text(
            json.dumps(sample_scotus), encoding="utf-8"
        )

        print("Sample SCOTUS file created:")
        print(json.dumps(sample_scotus, indent=2))

        # Normalize
        output_dir = tmp_path / "cases"
        paths = normalize_scotus(
            source_dir=scotus_dir, output_dir=output_dir, parallel=False
        )

        print(f"\n✓ Normalized {len(paths)} SCOTUS case(s)")

        if paths:
            with open(paths[0], "r", encoding="utf-8") as f:
                normalized = json.load(f)
            print("\nNormalized output:")
            print(json.dumps(normalized, indent=2))


def demo_ingestion_and_retrieval() -> None:
    """Demonstrate ingestion and retrieval using actual case files."""
    print_header("Ingestion & Retrieval Demo")

    # Check if example cases exist
    from syntechrev_polycodcal.legal_generator.config import CASE_DIR

    case_files = list(CASE_DIR.glob("*.json"))

    if not case_files:
        print("⚠️  No case files found in data/cases/")
        print("Please add some case files first.")
        return

    print(f"Found {len(case_files)} case file(s) in {CASE_DIR}")

    # Ingest
    print("\nIngesting cases...")
    names, embeddings = ingest_cases()
    print(f"✓ Ingested {len(names)} cases")
    print(f"  Embedding shape: {embeddings.shape}")

    # Sample queries
    queries = [
        "right to counsel",
        "equal protection",
        "fourth amendment search",
    ]

    embedder = Embedder()

    for query_text in queries:
        print(f"\n📝 Query: '{query_text}'")
        query_emb = embedder.encode_texts([query_text])[0]
        results = search(query_emb, top_k=3)

        if results:
            print("   Results:")
            for case_name, similarity in results:
                print(f"   - {case_name:<35} similarity={similarity:.3f}")
        else:
            print("   No results found")


def demo_parallel_processing() -> None:
    """Demonstrate parallel processing capability."""
    print_header("Parallel Processing Demo")

    print("The normalization adapters support parallel processing:")
    print("- Automatically enabled for datasets with >10 files")
    print("- Uses Python's ProcessPoolExecutor")
    print("- Can be disabled with --no-parallel flag")
    print("\nExample:")
    print("  # With parallel processing (default)")
    print("  python -m syntechrev_polycodcal.legal_generator.cli normalize scotus")
    print("\n  # Without parallel processing")
    print(
        "  python -m syntechrev_polycodcal.legal_generator.cli normalize scotus --no-parallel"
    )


def main() -> None:
    """Run all demonstrations."""
    print("\n" + "=" * 60)
    print("  Phase 6 Legal Data Ingestion System - Demonstration")
    print("=" * 60)

    try:
        demo_schema_validation()
        demo_normalization()
        demo_parallel_processing()
        demo_ingestion_and_retrieval()

        print_header("Demo Complete")
        print("✓ All demonstrations completed successfully!")
        print("\nNext steps:")
        print("1. Add your own legal data to data/sources/")
        print("2. Run: python -m syntechrev_polycodcal.legal_generator.cli normalize <source>")
        print("3. Run: python -m syntechrev_polycodcal.legal_generator.cli ingest")
        print("4. Run: python -m syntechrev_polycodcal.legal_generator.cli query --text 'your query'")
        print("\nSee docs/PHASE6_QUICK_START.md for detailed instructions.")

    except Exception as e:
        print(f"\n✗ Error during demonstration: {e}")
        import traceback

        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())

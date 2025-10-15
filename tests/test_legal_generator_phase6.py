from __future__ import annotations

import json

from syntechrev_polycodcal.legal_generator import ingest
from syntechrev_polycodcal.legal_generator.ingest import ingest_cases
from syntechrev_polycodcal.legal_generator.normalize import (
    normalize_amjur,
    normalize_blacks,
    normalize_scotus,
)
from syntechrev_polycodcal.legal_generator.validator import validate_cases


def test_normalize_scotus_with_metadata(tmp_path):
    """Test that normalize_scotus adds metadata fields."""
    source = tmp_path / "scotus.json"
    source.write_text(
        json.dumps(
            {
                "title": "Test Case",
                "summary": "Test summary",
                "citation": "123 U.S. 456",
                "date": "2024-01-15",
            }
        ),
        encoding="utf-8",
    )

    out_dir = tmp_path / "cases"
    written = normalize_scotus(source, out_dir=out_dir, source_tag="test")

    assert len(written) == 1
    with written[0].open("r", encoding="utf-8") as f:
        data = json.load(f)

    assert "id" in data
    assert data["source"] == "test"
    assert data["citation"] == "123 U.S. 456"
    assert data["date"] == "2024-01-15"
    assert data["schema_version"] == "1.0"


def test_normalize_with_dry_run(tmp_path, capsys):
    """Test that dry_run reports counts without writing files."""
    source = tmp_path / "scotus.jsonl"
    lines = [
        json.dumps({"title": "Case 1", "summary": "Summary 1"}),
        json.dumps({"title": "Case 2", "summary": "Summary 2"}),
    ]
    source.write_text("\n".join(lines), encoding="utf-8")

    out_dir = tmp_path / "cases"
    written = normalize_scotus(source, out_dir=out_dir, dry_run=True)

    assert len(written) == 0
    assert not out_dir.exists() or len(list(out_dir.glob("*.json"))) == 0
    captured = capsys.readouterr()
    assert "[DRY RUN]" in captured.out
    assert "2 records" in captured.out


def test_normalize_with_limit(tmp_path):
    """Test that limit restricts number of records processed."""
    source = tmp_path / "scotus.jsonl"
    lines = [
        json.dumps({"title": f"Case {i}", "summary": f"Summary {i}"}) for i in range(5)
    ]
    source.write_text("\n".join(lines), encoding="utf-8")

    out_dir = tmp_path / "cases"
    written = normalize_scotus(source, out_dir=out_dir, limit=3)

    assert len(written) == 3


def test_normalize_with_overwrite(tmp_path):
    """Test that overwrite replaces existing files with same ID."""
    source = tmp_path / "scotus.json"
    # Use same summary so ID stays the same
    data = {"title": "Test Case", "summary": "Same summary"}
    source.write_text(json.dumps(data), encoding="utf-8")

    out_dir = tmp_path / "cases"
    written1 = normalize_scotus(source, out_dir=out_dir)
    assert len(written1) == 1

    # Re-normalize with overwrite (same ID, so should replace)
    written2 = normalize_scotus(source, out_dir=out_dir, overwrite=True)

    assert len(written2) == 1
    # Should have same file path since ID is the same
    assert written1[0] == written2[0]
    assert len(list(out_dir.glob("*.json"))) == 1


def test_normalize_deduplication(tmp_path):
    """Test that duplicate IDs are skipped unless overwrite is True."""
    source = tmp_path / "scotus.jsonl"
    lines = [
        json.dumps({"title": "Case A", "summary": "Summary"}),
        json.dumps({"title": "Case A", "summary": "Summary"}),  # Duplicate
    ]
    source.write_text("\n".join(lines), encoding="utf-8")

    out_dir = tmp_path / "cases"
    written = normalize_scotus(source, out_dir=out_dir)

    # Should only write 1 file (duplicate skipped)
    assert len(written) == 1


def test_normalize_blacks_adapter(tmp_path):
    """Test Black's Law Dictionary adapter."""
    source = tmp_path / "blacks.json"
    source.write_text(
        json.dumps(
            {
                "term": "Habeas Corpus",
                "definition": "A writ requiring person to be brought before judge",
                "examples": ["Example 1", "Example 2"],
            }
        ),
        encoding="utf-8",
    )

    out_dir = tmp_path / "cases"
    written = normalize_blacks(source, out_dir=out_dir)

    assert len(written) == 1
    with written[0].open("r", encoding="utf-8") as f:
        data = json.load(f)

    assert data["case_name"] == "Habeas Corpus"
    assert "writ" in data["summary"]
    assert "Example 1" in data["opinion_text"]
    assert data["source"] == "blacks"


def test_normalize_blacks_missing_examples(tmp_path):
    """Test Black's adapter handles missing examples."""
    source = tmp_path / "blacks.json"
    source.write_text(
        json.dumps({"term": "Tort", "definition": "A civil wrong"}), encoding="utf-8"
    )

    out_dir = tmp_path / "cases"
    written = normalize_blacks(source, out_dir=out_dir)

    assert len(written) == 1
    with written[0].open("r", encoding="utf-8") as f:
        data = json.load(f)

    assert data["case_name"] == "Tort"
    assert "opinion_text" not in data or not data.get("opinion_text")


def test_normalize_amjur_adapter(tmp_path):
    """Test American Jurisprudence adapter."""
    source = tmp_path / "amjur.json"
    source.write_text(
        json.dumps(
            {
                "title": "Constitutional Law",
                "abstract": "Overview of constitutional principles",
                "body": "Full article text here...",
            }
        ),
        encoding="utf-8",
    )

    out_dir = tmp_path / "cases"
    written = normalize_amjur(source, out_dir=out_dir)

    assert len(written) == 1
    with written[0].open("r", encoding="utf-8") as f:
        data = json.load(f)

    assert data["case_name"] == "Constitutional Law"
    assert data["summary"] == "Overview of constitutional principles"
    assert data["opinion_text"] == "Full article text here..."
    assert data["source"] == "amjur"


def test_normalize_amjur_missing_abstract(tmp_path):
    """Test AmJur adapter uses body excerpt when abstract missing."""
    source = tmp_path / "amjur.json"
    body_text = "A" * 300  # Longer than 200 chars
    source.write_text(
        json.dumps({"title": "Article", "body": body_text}), encoding="utf-8"
    )

    out_dir = tmp_path / "cases"
    written = normalize_amjur(source, out_dir=out_dir)

    assert len(written) == 1
    with written[0].open("r", encoding="utf-8") as f:
        data = json.load(f)

    # Summary should be first 200 chars of body
    assert len(data["summary"]) == 200
    assert data["summary"] == body_text[:200]


def test_validator_with_valid_cases(tmp_path, monkeypatch):
    """Test validator passes for valid cases."""
    from syntechrev_polycodcal.legal_generator import validator

    case_dir = tmp_path / "cases"
    case_dir.mkdir()

    (case_dir / "case1.json").write_text(
        json.dumps(
            {
                "id": "abc123",
                "case_name": "Test Case",
                "summary": "Valid summary",
                "source": "scotus",
            }
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(validator, "CASE_DIR", case_dir)
    errors = validate_cases()
    assert len(errors) == 0


def test_validator_detects_missing_required_fields(tmp_path, monkeypatch):
    """Test validator detects missing required fields."""
    from syntechrev_polycodcal.legal_generator import validator

    case_dir = tmp_path / "cases"
    case_dir.mkdir()

    # Missing summary
    (case_dir / "bad_case.json").write_text(
        json.dumps({"case_name": "Test"}), encoding="utf-8"
    )

    monkeypatch.setattr(validator, "CASE_DIR", case_dir)
    errors = validate_cases()
    assert len(errors) > 0
    assert any("summary" in err.lower() for err in errors)


def test_validator_detects_wrong_field_types(tmp_path, monkeypatch):
    """Test validator detects incorrect field types."""
    from syntechrev_polycodcal.legal_generator import validator

    case_dir = tmp_path / "cases"
    case_dir.mkdir()

    # case_name should be string, not int
    (case_dir / "bad_type.json").write_text(
        json.dumps({"case_name": 123, "summary": "Summary"}), encoding="utf-8"
    )

    monkeypatch.setattr(validator, "CASE_DIR", case_dir)
    errors = validate_cases()
    assert len(errors) > 0
    assert any("string" in err.lower() for err in errors)


def test_ingest_writes_metadata_file(tmp_path, monkeypatch):
    """Test that ingest writes vectors.meta.json."""
    case_dir = tmp_path / "cases"
    case_dir.mkdir()
    vector_dir = tmp_path / "vectors"

    (case_dir / "test.json").write_text(
        json.dumps({"case_name": "Test", "summary": "Summary"}), encoding="utf-8"
    )

    monkeypatch.setattr(ingest, "CASE_DIR", case_dir)
    monkeypatch.setattr(ingest, "VECTOR_DIR", vector_dir)
    monkeypatch.setattr(ingest, "VECTOR_PATH", vector_dir / "embeddings.npz")

    names, _ = ingest_cases()
    assert len(names) == 1

    meta_path = vector_dir / "vectors.meta.json"
    assert meta_path.exists()

    with meta_path.open("r", encoding="utf-8") as f:
        metadata = json.load(f)

    assert "model" in metadata
    assert "created_at" in metadata
    assert metadata["count"] == 1
    assert metadata["dim"] == 256
    assert "file_version" in metadata
    assert "names_hash" in metadata


def test_ingest_append_mode(tmp_path, monkeypatch):
    """Test ingest append mode (default behavior)."""
    case_dir = tmp_path / "cases"
    case_dir.mkdir()
    vector_dir = tmp_path / "vectors"

    (case_dir / "test.json").write_text(
        json.dumps({"case_name": "Test", "summary": "Summary"}), encoding="utf-8"
    )

    monkeypatch.setattr(ingest, "CASE_DIR", case_dir)
    monkeypatch.setattr(ingest, "VECTOR_DIR", vector_dir)
    monkeypatch.setattr(ingest, "VECTOR_PATH", vector_dir / "embeddings.npz")

    # First ingest
    names1, _ = ingest_cases(rebuild=False)
    assert len(names1) == 1

    # In current implementation, re-running ingest re-processes all files
    # This test verifies the function accepts rebuild parameter
    names2, _ = ingest_cases(rebuild=True)
    assert len(names2) == 1

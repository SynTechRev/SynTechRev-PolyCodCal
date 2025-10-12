"""Tests for legal data normalization adapters."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from syntechrev_polycodcal.legal_generator.normalize import (
    normalize_private,
    normalize_scotus,
    normalize_uscode,
)


@pytest.fixture
def scotus_source_dir(tmp_path):
    """Create temporary SCOTUS source directory with test files."""
    source_dir = tmp_path / "scotus"
    source_dir.mkdir()

    # Create JSON test file
    json_case = {
        "case_name": "Test v. Case",
        "opinion_text": "This is a test opinion.",
        "citation": "123 U.S. 456",
        "decision_date": "2024-01-15",
    }
    (source_dir / "test_case.json").write_text(
        json.dumps(json_case), encoding="utf-8"
    )

    # Create TXT test file
    (source_dir / "another_case.txt").write_text(
        "This is a plain text opinion.", encoding="utf-8"
    )

    return source_dir


@pytest.fixture
def uscode_source_dir(tmp_path):
    """Create temporary US Code source directory with test files."""
    source_dir = tmp_path / "uscode"
    source_dir.mkdir()

    # Create TXT test file with title/section pattern
    (source_dir / "title_42_section_1983.txt").write_text(
        "Every person who, under color of law, deprives another of rights...",
        encoding="utf-8",
    )

    return source_dir


@pytest.fixture
def private_source_dir(tmp_path):
    """Create temporary private source directory with test files."""
    source_dir = tmp_path / "private"
    source_dir.mkdir()

    # Create JSON test file (simulating Black's Law Dictionary)
    term = {
        "term": "Due Process",
        "definition": "The conduct of legal proceedings according to established rules.",
    }
    (source_dir / "blacks_due_process.json").write_text(
        json.dumps(term), encoding="utf-8"
    )

    return source_dir


def test_normalize_scotus_json(scotus_source_dir, tmp_path):
    """Test SCOTUS JSON normalization."""
    output_dir = tmp_path / "cases"
    paths = normalize_scotus(
        source_dir=scotus_source_dir, output_dir=output_dir, parallel=False
    )

    assert len(paths) == 2
    assert output_dir.exists()

    # Check that normalized files were created
    json_files = list(output_dir.glob("*.json"))
    assert len(json_files) == 2

    # Verify content of first file
    with open(json_files[0], "r", encoding="utf-8") as f:
        record = json.load(f)

    assert "case_name" in record
    assert "summary" in record
    assert record["source"] == "scotus"


def test_normalize_scotus_txt(scotus_source_dir, tmp_path):
    """Test SCOTUS TXT normalization."""
    output_dir = tmp_path / "cases"
    paths = normalize_scotus(
        source_dir=scotus_source_dir, output_dir=output_dir, parallel=False
    )

    assert len(paths) == 2

    # Find the TXT-derived file
    txt_derived = None
    for path in paths:
        with open(path, "r", encoding="utf-8") as f:
            record = json.load(f)
        if "another case" in record["case_name"].lower():
            txt_derived = record
            break

    assert txt_derived is not None
    assert "plain text opinion" in txt_derived["summary"]


def test_normalize_scotus_empty_dir(tmp_path):
    """Test SCOTUS normalization with empty directory."""
    source_dir = tmp_path / "empty"
    source_dir.mkdir()
    output_dir = tmp_path / "cases"

    paths = normalize_scotus(
        source_dir=source_dir, output_dir=output_dir, parallel=False
    )
    assert paths == []


def test_normalize_scotus_nonexistent_dir(tmp_path):
    """Test SCOTUS normalization with non-existent directory."""
    source_dir = tmp_path / "nonexistent"
    output_dir = tmp_path / "cases"

    paths = normalize_scotus(
        source_dir=source_dir, output_dir=output_dir, parallel=False
    )
    assert paths == []


def test_normalize_uscode_txt(uscode_source_dir, tmp_path):
    """Test US Code TXT normalization."""
    output_dir = tmp_path / "cases"
    paths = normalize_uscode(
        source_dir=uscode_source_dir, output_dir=output_dir, parallel=False
    )

    assert len(paths) == 1

    # Verify content
    with open(paths[0], "r", encoding="utf-8") as f:
        record = json.load(f)

    assert record["source"] == "uscode"
    assert record["jurisdiction"] == "federal"
    assert "Title 42" in record["case_name"]
    assert "Section 1983" in record["case_name"]
    assert "42 U.S.C. § 1983" in record["citation"]


def test_normalize_uscode_empty_dir(tmp_path):
    """Test US Code normalization with empty directory."""
    source_dir = tmp_path / "empty"
    source_dir.mkdir()
    output_dir = tmp_path / "cases"

    paths = normalize_uscode(
        source_dir=source_dir, output_dir=output_dir, parallel=False
    )
    assert paths == []


def test_normalize_private_json(private_source_dir, tmp_path):
    """Test private source JSON normalization."""
    output_dir = tmp_path / "cases"
    paths = normalize_private(source_dir=private_source_dir, output_dir=output_dir)

    assert len(paths) == 1

    # Verify content
    with open(paths[0], "r", encoding="utf-8") as f:
        record = json.load(f)

    assert record["source"] == "blackslaw"
    assert "Due Process" in record["case_name"]
    assert "legal proceedings" in record["summary"]


def test_normalize_private_empty_dir(tmp_path):
    """Test private source normalization with empty directory."""
    source_dir = tmp_path / "empty"
    source_dir.mkdir()
    output_dir = tmp_path / "cases"

    paths = normalize_private(source_dir=source_dir, output_dir=output_dir)
    assert paths == []


def test_normalize_private_nonexistent_dir(tmp_path):
    """Test private source normalization with non-existent directory."""
    source_dir = tmp_path / "nonexistent"
    output_dir = tmp_path / "cases"

    paths = normalize_private(source_dir=source_dir, output_dir=output_dir)
    assert paths == []


def test_normalize_handles_invalid_json(tmp_path):
    """Test that invalid JSON is handled gracefully."""
    source_dir = tmp_path / "scotus"
    source_dir.mkdir()

    # Create invalid JSON file
    (source_dir / "invalid.json").write_text("{ invalid json", encoding="utf-8")

    output_dir = tmp_path / "cases"
    paths = normalize_scotus(
        source_dir=source_dir, output_dir=output_dir, parallel=False
    )

    # Should handle error gracefully and return empty list
    assert paths == []


def test_normalize_creates_output_dir(tmp_path):
    """Test that output directory is created if it doesn't exist."""
    source_dir = tmp_path / "scotus"
    source_dir.mkdir()
    (source_dir / "test.txt").write_text("Test content", encoding="utf-8")

    output_dir = tmp_path / "nonexistent" / "cases"
    paths = normalize_scotus(
        source_dir=source_dir, output_dir=output_dir, parallel=False
    )

    assert output_dir.exists()
    assert len(paths) == 1


def test_normalize_parallel_flag(scotus_source_dir, tmp_path):
    """Test that parallel flag is handled correctly."""
    output_dir = tmp_path / "cases"

    # Test with parallel=True (should work even with few files)
    paths_parallel = normalize_scotus(
        source_dir=scotus_source_dir, output_dir=output_dir, parallel=True
    )

    # Clean output for sequential test
    for file in output_dir.glob("*.json"):
        file.unlink()

    # Test with parallel=False
    paths_sequential = normalize_scotus(
        source_dir=scotus_source_dir, output_dir=output_dir, parallel=False
    )

    # Should produce same number of outputs
    assert len(paths_parallel) == len(paths_sequential)

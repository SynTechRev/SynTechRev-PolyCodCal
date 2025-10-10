"""Tests for the data_loader module."""

import json
import pathlib
import tempfile

import pytest
from pydantic import ValidationError

from syntechrev_polycodcal.data_loader import load_legal_records
from syntechrev_polycodcal.schemas.legal_record import LegalRecord


def test_load_legal_records_success():
    """Test that load_legal_records successfully loads all case files."""
    records = load_legal_records("data/cases")

    assert len(records) == 10
    assert all(isinstance(r, LegalRecord) for r in records)


def test_load_legal_records_all_required_fields():
    """Test that all loaded records have required fields populated."""
    records = load_legal_records("data/cases")

    for record in records:
        assert record.case_name
        assert record.year > 0
        assert record.citation
        assert record.court
        assert record.jurisdiction
        assert record.doctrine
        assert record.summary
        assert record.holding
        assert record.significance


def test_specific_case_marbury():
    """Test that a specific case (Marbury v. Madison) loads with expected values."""
    records = load_legal_records("data/cases")

    marbury = next((r for r in records if "Marbury" in r.case_name), None)
    assert marbury is not None
    assert marbury.year == 1803
    assert "review" in marbury.holding.lower()
    assert "unconstitutional" in marbury.holding.lower()
    assert marbury.court == "U.S. Supreme Court"
    assert marbury.jurisdiction == "Federal"


def test_specific_case_brown():
    """Test that Brown v. Board of Education loads correctly."""
    records = load_legal_records("data/cases")

    brown = next((r for r in records if "Brown" in r.case_name), None)
    assert brown is not None
    assert brown.year == 1954
    assert brown.doctrine == "Civil Rights"
    assert "equal" in brown.holding.lower()


def test_load_legal_records_nonexistent_path():
    """Test that load_legal_records raises FileNotFoundError for nonexistent path."""
    with pytest.raises(FileNotFoundError) as exc_info:
        load_legal_records("nonexistent/path")

    assert "does not exist" in str(exc_info.value)


def test_load_legal_records_empty_directory():
    """Test that load_legal_records returns empty list for directory with no JSON files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        records = load_legal_records(tmpdir)
        assert records == []


def test_load_legal_records_invalid_json():
    """Test that load_legal_records raises JSONDecodeError for invalid JSON."""
    with tempfile.TemporaryDirectory() as tmpdir:
        invalid_file = pathlib.Path(tmpdir) / "invalid.json"
        invalid_file.write_text("{invalid json content", encoding="utf-8")

        with pytest.raises(json.JSONDecodeError):
            load_legal_records(tmpdir)


def test_load_legal_records_invalid_schema():
    """Test that load_legal_records raises ValidationError for data not matching schema."""
    with tempfile.TemporaryDirectory() as tmpdir:
        invalid_file = pathlib.Path(tmpdir) / "invalid.json"
        # Missing required fields
        invalid_file.write_text('{"case_name": "Test"}', encoding="utf-8")

        with pytest.raises(ValidationError):
            load_legal_records(tmpdir)


def test_legal_record_schema_validation():
    """Test that LegalRecord schema validates correctly."""
    valid_data = {
        "case_name": "Test Case",
        "year": 2000,
        "citation": "123 U.S. 456",
        "court": "Test Court",
        "jurisdiction": "Test Jurisdiction",
        "doctrine": "Test Doctrine",
        "summary": "Test summary",
        "holding": "Test holding",
        "significance": "Test significance",
    }

    record = LegalRecord(**valid_data)
    assert record.case_name == "Test Case"
    assert record.year == 2000
    assert record.keywords is None  # Optional field


def test_legal_record_with_keywords():
    """Test that LegalRecord correctly handles optional keywords field."""
    records = load_legal_records("data/cases")

    # Check that at least one record has keywords
    records_with_keywords = [r for r in records if r.keywords is not None]
    assert len(records_with_keywords) > 0

    # Verify keywords is a list
    for record in records_with_keywords:
        assert isinstance(record.keywords, list)
        assert all(isinstance(k, str) for k in record.keywords)


def test_all_cases_present():
    """Test that all 10 expected landmark cases are present."""
    records = load_legal_records("data/cases")

    expected_cases = [
        "Marbury v. Madison",
        "Brown v. Board of Education",
        "Gideon v. Wainwright",
        "Miranda v. Arizona",
        "Loving v. Virginia",
        "Tinker v. Des Moines",
        "Roe v. Wade",
        "United States v. Nixon",
        "Erie Railroad",
        "Shelby County v. Holder",
    ]

    case_names = [r.case_name for r in records]

    for expected in expected_cases:
        assert any(expected in name for name in case_names), f"{expected} not found"


def test_year_range():
    """Test that all cases are within expected year range."""
    records = load_legal_records("data/cases")

    years = [r.year for r in records]
    assert min(years) >= 1803  # Marbury v. Madison
    assert max(years) <= 2025  # Current year cap
    assert all(isinstance(y, int) for y in years)


def test_doctrine_diversity():
    """Test that cases cover multiple legal doctrines."""
    records = load_legal_records("data/cases")

    doctrines = {r.doctrine for r in records}
    assert len(doctrines) >= 3  # Should have at least 3 different doctrines


def test_court_consistency():
    """Test that all cases are from U.S. Supreme Court."""
    records = load_legal_records("data/cases")

    for record in records:
        assert "Supreme Court" in record.court


def test_jurisdiction_consistency():
    """Test that all cases have Federal jurisdiction."""
    records = load_legal_records("data/cases")

    for record in records:
        assert record.jurisdiction == "Federal"

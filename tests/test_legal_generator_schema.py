"""Tests for legal record schema validation."""

from __future__ import annotations

from syntechrev_polycodcal.legal_generator.schema import is_valid_record, validate_record


def test_validate_minimal_valid_record():
    """Test validation of minimal valid record."""
    record = {"case_name": "Test Case", "summary": "Test summary", "source": "scotus"}
    errors = validate_record(record)
    assert errors == []
    assert is_valid_record(record) is True


def test_validate_missing_case_name():
    """Test validation fails for missing case_name."""
    record = {"summary": "Test summary"}
    errors = validate_record(record)
    assert len(errors) == 1
    assert "case_name" in errors[0]
    assert is_valid_record(record) is False


def test_validate_missing_summary():
    """Test validation fails for missing summary."""
    record = {"case_name": "Test Case"}
    errors = validate_record(record)
    assert len(errors) == 1
    assert "summary" in errors[0]
    assert is_valid_record(record) is False


def test_validate_invalid_source():
    """Test validation fails for invalid source."""
    record = {
        "case_name": "Test Case",
        "summary": "Test summary",
        "source": "invalid",
    }
    errors = validate_record(record)
    assert len(errors) == 1
    assert "source" in errors[0]


def test_validate_valid_sources():
    """Test validation succeeds for all valid sources."""
    valid_sources = ["scotus", "uscode", "blackslaw", "amjur", "custom"]
    for source in valid_sources:
        record = {
            "case_name": "Test Case",
            "summary": "Test summary",
            "source": source,
        }
        errors = validate_record(record)
        assert errors == [], f"Source {source} should be valid"


def test_validate_date_format():
    """Test date format validation."""
    # Valid date
    record = {
        "case_name": "Test Case",
        "summary": "Test summary",
        "date": "2024-01-15",
    }
    errors = validate_record(record)
    assert errors == []

    # Invalid date format
    record["date"] = "01/15/2024"
    errors = validate_record(record)
    assert len(errors) == 1
    assert "date" in errors[0]

    # Invalid date
    record["date"] = "not-a-date"
    errors = validate_record(record)
    assert len(errors) == 1


def test_validate_optional_fields():
    """Test validation with all optional fields."""
    record = {
        "case_name": "Test Case",
        "summary": "Test summary",
        "source": "scotus",
        "citation": "123 U.S. 456",
        "date": "2024-01-15",
        "jurisdiction": "federal",
    }
    errors = validate_record(record)
    assert errors == []


def test_validate_type_errors():
    """Test validation catches type errors."""
    # case_name must be string
    record = {"case_name": 123, "summary": "Test summary"}
    errors = validate_record(record)
    assert any("case_name" in err for err in errors)

    # summary must be string
    record = {"case_name": "Test", "summary": 123}
    errors = validate_record(record)
    assert any("summary" in err for err in errors)

    # citation must be string
    record = {"case_name": "Test", "summary": "Text", "citation": 123}
    errors = validate_record(record)
    assert any("citation" in err for err in errors)

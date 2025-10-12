"""Schema validation for normalized legal records.

This module provides validation for the normalized JSON schema used
in the Phase 6 ingestion pipeline.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List


def validate_record(record: Dict[str, Any]) -> List[str]:
    """Validate a normalized legal record against the schema.

    Args:
        record: Dictionary containing the record data

    Returns:
        List of validation error messages (empty if valid)

    Example:
        >>> record = {"case_name": "Test", "summary": "Text", "source": "scotus"}
        >>> errors = validate_record(record)
        >>> len(errors)
        0
    """
    errors: List[str] = []

    # Required fields
    if "case_name" not in record:
        errors.append("Missing required field: case_name")
    elif not isinstance(record["case_name"], str):
        errors.append("Field 'case_name' must be a string")

    if "summary" not in record:
        errors.append("Missing required field: summary")
    elif not isinstance(record["summary"], str):
        errors.append("Field 'summary' must be a string")

    # Source field validation
    if "source" in record:
        valid_sources = {"scotus", "uscode", "blackslaw", "amjur", "custom"}
        if record["source"] not in valid_sources:
            errors.append(
                f"Invalid source '{record['source']}'. "
                f"Must be one of: {', '.join(sorted(valid_sources))}"
            )

    # Optional field type validation
    if "citation" in record and not isinstance(record["citation"], str):
        errors.append("Field 'citation' must be a string")

    if "jurisdiction" in record and not isinstance(record["jurisdiction"], str):
        errors.append("Field 'jurisdiction' must be a string")

    # Date validation
    if "date" in record:
        if not isinstance(record["date"], str):
            errors.append("Field 'date' must be a string")
        else:
            # Try to parse as YYYY-MM-DD
            try:
                datetime.strptime(record["date"], "%Y-%m-%d")
            except ValueError:
                errors.append(
                    f"Field 'date' must be in YYYY-MM-DD format, got: {record['date']}"
                )

    return errors


def is_valid_record(record: Dict[str, Any]) -> bool:
    """Check if a record is valid.

    Args:
        record: Dictionary containing the record data

    Returns:
        True if valid, False otherwise
    """
    return len(validate_record(record)) == 0

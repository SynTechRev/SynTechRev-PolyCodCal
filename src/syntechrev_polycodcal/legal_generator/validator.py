from __future__ import annotations

import json
import pathlib
from typing import List, Optional

from .config import CASE_DIR


def validate_cases(case_dir: Optional[pathlib.Path] = None) -> List[str]:
    """Validate legal case files for schema compliance.

    Args:
        case_dir: Optional directory containing case files (defaults to CASE_DIR)

    Returns:
        List of error messages (empty if validation passes)
    """
    cdir = case_dir or CASE_DIR
    if not cdir.exists():
        return [f"Case directory does not exist: {cdir}"]

    errors: List[str] = []
    required_fields = ["case_name", "summary"]
    string_fields = [
        "case_name",
        "summary",
        "source",
        "citation",
        "jurisdiction",
        "date",
        "schema_version",
    ]

    for file_path in sorted(cdir.glob("*.json")):
        try:
            with file_path.open("r", encoding="utf-8") as f:
                record = json.load(f)
        except json.JSONDecodeError as e:
            errors.append(f"{file_path.name}: Invalid JSON - {e}")
            continue
        except IOError as e:
            errors.append(f"{file_path.name}: Cannot read file - {e}")
            continue

        if not isinstance(record, dict):
            errors.append(f"{file_path.name}: Root must be a JSON object")
            continue

        # Check required fields
        for field in required_fields:
            if field not in record:
                errors.append(f"{file_path.name}: Missing required field '{field}'")
            elif not isinstance(record[field], str):
                errors.append(
                    f"{file_path.name}: Field '{field}' must be a string, "
                    f"got {type(record[field]).__name__}"
                )
            elif not record[field].strip():
                errors.append(f"{file_path.name}: Field '{field}' cannot be empty")

        # Check optional string fields if present
        for field in string_fields:
            if field in record and not isinstance(record[field], str):
                errors.append(
                    f"{file_path.name}: Field '{field}' must be a string, "
                    f"got {type(record[field]).__name__}"
                )

    return errors

"""Data loader for legal case records."""

import json
import pathlib
from typing import List

from .schemas.legal_record import LegalRecord


def load_legal_records(path: str = "data/cases") -> List[LegalRecord]:
    """Load legal case records from JSON files.

    Args:
        path: Path to directory containing JSON case files. Defaults to "data/cases".

    Returns:
        List of LegalRecord objects parsed from JSON files.

    Raises:
        FileNotFoundError: If the specified path does not exist.
        json.JSONDecodeError: If a JSON file cannot be parsed.
        pydantic.ValidationError: If a record doesn't match the schema.

    Example:
        >>> records = load_legal_records("data/cases")
        >>> print(f"Loaded {len(records)} legal records")
    """
    records: List[LegalRecord] = []
    path_obj = pathlib.Path(path)

    if not path_obj.exists():
        raise FileNotFoundError(f"Path does not exist: {path}")

    for file in path_obj.glob("*.json"):
        with open(file, encoding="utf-8") as f:
            data = json.load(f)
            records.append(LegalRecord(**data))

    return records

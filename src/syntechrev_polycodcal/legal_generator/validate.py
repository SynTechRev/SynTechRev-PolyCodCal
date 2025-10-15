from __future__ import annotations

import json
import pathlib
from typing import List, Tuple

from .config import CASE_DIR


def validate_cases(path: pathlib.Path | None = None) -> List[Tuple[pathlib.Path, str]]:
    """Validate normalized case JSON files.

    Checks required fields and types.

    Returns a list of (file, error_message) for each invalid file.
    """
    base = path or CASE_DIR
    errors: List[Tuple[pathlib.Path, str]] = []
    if not base.exists():
        errors.append((base, "directory does not exist"))
        return errors

    for p in sorted(base.glob("*.json")):
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except Exception as e:  # noqa: BLE001
            errors.append((p, f"invalid JSON: {e}"))
            continue
        # required fields
        for field in ("case_name", "summary"):
            if field not in data or not isinstance(data[field], str) or not data[field]:
                errors.append((p, f"missing/invalid field: {field}"))
        # optional types
        if "id" in data and not isinstance(data["id"], str):
            errors.append((p, "invalid type for id"))
        if "source" in data and not isinstance(data["source"], str):
            errors.append((p, "invalid type for source"))
    return errors

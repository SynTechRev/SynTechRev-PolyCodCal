from __future__ import annotations

import json
import pathlib
from typing import Iterable, List, Mapping, Optional

from .config import CASE_DIR


def _ensure_out_dir(out_dir: Optional[pathlib.Path]) -> pathlib.Path:
    out = out_dir or CASE_DIR
    out.mkdir(parents=True, exist_ok=True)
    return out


def _load_json_records(source: pathlib.Path) -> Iterable[Mapping[str, object]]:
    """Load records from JSON or JSONL file.

    Args:
        source: Path to a .json or .jsonl file containing case records.

    Yields:
        Parsed dict records.
    """
    suffix = source.suffix.lower()
    if suffix == ".jsonl":
        with source.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                yield json.loads(line)
    elif suffix == ".json":
        with source.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    yield item
        elif isinstance(data, dict):
            # Single record
            yield data
        else:
            raise ValueError("Unsupported JSON structure: expected list or object")
    else:
        raise ValueError("Unsupported source format: use .json or .jsonl")


def normalize_scotus(
    source: pathlib.Path,
    out_dir: Optional[pathlib.Path] = None,
) -> List[pathlib.Path]:
    """Normalize SCOTUS-like records into project case schema.

    Input schema is flexible; fields are mapped in a best-effort way:
    - case_name: record["case_name"] or record["title"] or record["name"]
    - summary: record["summary"] or composed from headnote/opinion if present
    - facts/holding/opinion_text: passthrough if available

    Writes one JSON file per case into out_dir (default CASE_DIR).

    Returns:
        List of written file paths.
    """
    out = _ensure_out_dir(out_dir)
    written: List[pathlib.Path] = []

    for rec in _load_json_records(source):
        # Extract basic fields with fallbacks
        case_name = str(
            rec.get("case_name")
            or rec.get("title")
            or rec.get("name")
            or "Untitled Case"
        )
        summary: str = str(
            rec.get("summary") or rec.get("syllabus") or rec.get("headnote") or ""
        )
        facts = rec.get("facts")
        holding = rec.get("holding")
        opinion_text = rec.get("opinion_text") or rec.get("opinion")

        payload = {
            "case_name": case_name,
            "summary": summary,
        }
        if facts is not None:
            payload["facts"] = facts
        if holding is not None:
            payload["holding"] = holding
        if opinion_text is not None:
            payload["opinion_text"] = opinion_text

        # Derive filename from case name (safe-ish)
        stem = (
            case_name.replace(" ", "_").replace("/", "-").replace("\\", "-").strip("._")
            or "case"
        )
        # Avoid overly long filenames
        stem = stem[:120]
        out_path = out / f"{stem}.json"

        # Ensure uniqueness by appending counter if needed
        counter = 1
        final_path = out_path
        while final_path.exists():
            final_path = out / f"{stem}_{counter}.json"
            counter += 1

        final_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        written.append(final_path)

    return written


def normalize_uscode(
    source: pathlib.Path,
    out_dir: Optional[pathlib.Path] = None,
) -> List[pathlib.Path]:
    """Normalize U.S. Code-like entries into the project case schema.

    Expected flexible inputs (per record):
    - title: int | str (e.g., 42)
    - section: str | int (e.g., "§1983" or 1983)
    - heading: str (short caption)
    - text: str (full section text)

    Mappings:
    - case_name := f"USC Title {title} §{section}: {heading}" (best-effort)
    - summary := heading or first 200 chars of text
    - opinion_text := text
    """
    out = _ensure_out_dir(out_dir)
    written: List[pathlib.Path] = []

    for rec in _load_json_records(source):
        title = rec.get("title")
        section = rec.get("section") or rec.get("sec")
        heading = rec.get("heading") or rec.get("caption") or ""
        text = rec.get("text") or rec.get("body") or ""

        title_str = str(title) if title is not None else ""
        section_str = str(section) if section is not None else ""
        heading_str = str(heading) if heading is not None else ""
        text_str = str(text) if text is not None else ""

        base = "USC"
        if title_str:
            base += f" Title {title_str}"
        if section_str:
            base += f" §{section_str}"
        case_name = f"{base}: {heading_str}".strip().strip(":") or "USC Section"

        summary = heading_str or text_str[:200]

        payload = {
            "case_name": case_name,
            "summary": summary,
        }
        if text_str:
            payload["opinion_text"] = text_str

        stem = (
            case_name.replace(" ", "_").replace("/", "-").replace("\\", "-").strip("._")
            or "usc_section"
        )[:120]
        out_path = out / f"{stem}.json"
        counter = 1
        final_path = out_path
        while final_path.exists():
            final_path = out / f"{stem}_{counter}.json"
            counter += 1
        final_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        written.append(final_path)

    return written

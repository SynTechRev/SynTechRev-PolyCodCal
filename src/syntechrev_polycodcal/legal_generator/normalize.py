from __future__ import annotations

import hashlib
import json
import pathlib
from typing import Any, Dict, Iterable, List, Mapping, Optional

from .config import CASE_DIR

SCHEMA_VERSION = "1.0"


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


def _compute_stable_id(case_name: str, summary: str) -> str:
    """Compute stable ID hash from case_name and summary.
    
    Args:
        case_name: Case name or title
        summary: Case summary or text
        
    Returns:
        Hex digest of the hash
    """
    content = f"{case_name}|{summary}"
    return hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]


def _add_metadata(
    payload: Dict[str, Any],
    rec: Mapping[str, object],
    source_tag: Optional[str] = None,
) -> None:
    """Add optional metadata fields to normalized payload.
    
    Args:
        payload: The payload dict to augment (modified in place)
        rec: Source record
        source_tag: Optional provenance tag
    """
    payload["schema_version"] = SCHEMA_VERSION
    
    if source_tag:
        payload["source"] = source_tag
    elif "source" in rec:
        payload["source"] = str(rec["source"])
    
    if "citation" in rec:
        payload["citation"] = str(rec["citation"])
    
    if "jurisdiction" in rec:
        payload["jurisdiction"] = str(rec["jurisdiction"])
    
    if "date" in rec:
        payload["date"] = str(rec["date"])


def normalize_scotus(
    source: pathlib.Path,
    out_dir: Optional[pathlib.Path] = None,
    source_tag: Optional[str] = None,
    dry_run: bool = False,
    limit: Optional[int] = None,
    overwrite: bool = False,
) -> List[pathlib.Path]:
    """Normalize SCOTUS-like records into project case schema.

    Input schema is flexible; fields are mapped in a best-effort way:
    - case_name: record["case_name"] or record["title"] or record["name"]
    - summary: record["summary"] or composed from headnote/opinion if present
    - facts/holding/opinion_text: passthrough if available

    Writes one JSON file per case into out_dir (default CASE_DIR).

    Args:
        source: Path to source JSON/JSONL file
        out_dir: Output directory for normalized cases
        source_tag: Optional provenance label for all records
        dry_run: If True, parse and report counts without writing files
        limit: Maximum number of records to process
        overwrite: If True, replace files with same ID; else append counter

    Returns:
        List of written file paths.
    """
    out = _ensure_out_dir(out_dir)
    written: List[pathlib.Path] = []
    seen_ids: Dict[str, pathlib.Path] = {}
    
    if not dry_run:
        # Pre-scan existing files to build ID map
        for existing in out.glob("*.json"):
            try:
                with existing.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                if "id" in data:
                    seen_ids[data["id"]] = existing
            except (json.JSONDecodeError, IOError):
                pass

    count = 0
    for rec in _load_json_records(source):
        if limit is not None and count >= limit:
            break
        count += 1
        
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

        # Compute stable ID
        record_id = _compute_stable_id(case_name, summary)

        payload: Dict[str, Any] = {
            "id": record_id,
            "case_name": case_name,
            "summary": summary,
        }
        if facts is not None:
            payload["facts"] = facts
        if holding is not None:
            payload["holding"] = holding
        if opinion_text is not None:
            payload["opinion_text"] = opinion_text
        
        # Add metadata
        _add_metadata(payload, rec, source_tag or "scotus")

        if dry_run:
            continue
        
        # Check for duplicates
        if not overwrite and record_id in seen_ids:
            continue
        
        # Derive filename from case name (safe-ish)
        stem = (
            case_name.replace(" ", "_").replace("/", "-").replace("\\", "-").strip("._")
            or "case"
        )
        # Avoid overly long filenames
        stem = stem[:120]
        out_path = out / f"{stem}.json"

        # Handle file naming
        if overwrite and record_id in seen_ids:
            final_path = seen_ids[record_id]
        else:
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
        seen_ids[record_id] = final_path

    if dry_run:
        print(f"[DRY RUN] Parsed {count} records (no files written)")
    
    return written


def normalize_uscode(
    source: pathlib.Path,
    out_dir: Optional[pathlib.Path] = None,
    source_tag: Optional[str] = None,
    dry_run: bool = False,
    limit: Optional[int] = None,
    overwrite: bool = False,
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

    Args:
        source: Path to source JSON/JSONL file
        out_dir: Output directory for normalized cases
        source_tag: Optional provenance label for all records
        dry_run: If True, parse and report counts without writing files
        limit: Maximum number of records to process
        overwrite: If True, replace files with same ID; else append counter

    Returns:
        List of written file paths.
    """
    out = _ensure_out_dir(out_dir)
    written: List[pathlib.Path] = []
    seen_ids: Dict[str, pathlib.Path] = {}
    
    if not dry_run:
        # Pre-scan existing files to build ID map
        for existing in out.glob("*.json"):
            try:
                with existing.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                if "id" in data:
                    seen_ids[data["id"]] = existing
            except (json.JSONDecodeError, IOError):
                pass

    count = 0
    for rec in _load_json_records(source):
        if limit is not None and count >= limit:
            break
        count += 1
        
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

        # Compute stable ID
        record_id = _compute_stable_id(case_name, summary)

        payload: Dict[str, Any] = {
            "id": record_id,
            "case_name": case_name,
            "summary": summary,
        }
        if text_str:
            payload["opinion_text"] = text_str
        
        # Add metadata
        _add_metadata(payload, rec, source_tag or "uscode")

        if dry_run:
            continue
        
        # Check for duplicates
        if not overwrite and record_id in seen_ids:
            continue

        stem = (
            case_name.replace(" ", "_").replace("/", "-").replace("\\", "-").strip("._")
            or "usc_section"
        )[:120]
        out_path = out / f"{stem}.json"
        
        # Handle file naming
        if overwrite and record_id in seen_ids:
            final_path = seen_ids[record_id]
        else:
            counter = 1
            final_path = out_path
            while final_path.exists():
                final_path = out / f"{stem}_{counter}.json"
                counter += 1
        
        final_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        written.append(final_path)
        seen_ids[record_id] = final_path

    if dry_run:
        print(f"[DRY RUN] Parsed {count} records (no files written)")
    
    return written


def normalize_blacks(
    source: pathlib.Path,
    out_dir: Optional[pathlib.Path] = None,
    source_tag: Optional[str] = None,
    dry_run: bool = False,
    limit: Optional[int] = None,
    overwrite: bool = False,
) -> List[pathlib.Path]:
    """Normalize Black's Law Dictionary entries into project case schema.

    Expected inputs (per record):
    - term: str (legal term)
    - definition: str (main definition)
    - examples: str | list (optional usage examples)

    Mappings:
    - case_name := term
    - summary := definition
    - opinion_text := examples (joined if list)

    Args:
        source: Path to source JSON/JSONL file
        out_dir: Output directory for normalized cases
        source_tag: Optional provenance label for all records
        dry_run: If True, parse and report counts without writing files
        limit: Maximum number of records to process
        overwrite: If True, replace files with same ID; else append counter

    Returns:
        List of written file paths.
    """
    out = _ensure_out_dir(out_dir)
    written: List[pathlib.Path] = []
    seen_ids: Dict[str, pathlib.Path] = {}
    
    if not dry_run:
        for existing in out.glob("*.json"):
            try:
                with existing.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                if "id" in data:
                    seen_ids[data["id"]] = existing
            except (json.JSONDecodeError, IOError):
                pass

    count = 0
    for rec in _load_json_records(source):
        if limit is not None and count >= limit:
            break
        count += 1
        
        term = str(rec.get("term") or rec.get("title") or "Untitled Term")
        definition = str(rec.get("definition") or rec.get("text") or "")
        examples = rec.get("examples")
        
        # Handle examples as string or list
        examples_text = ""
        if examples:
            if isinstance(examples, list):
                examples_text = " ".join(str(e) for e in examples)
            else:
                examples_text = str(examples)

        # Compute stable ID
        record_id = _compute_stable_id(term, definition)

        payload: Dict[str, Any] = {
            "id": record_id,
            "case_name": term,
            "summary": definition,
        }
        if examples_text:
            payload["opinion_text"] = examples_text
        
        # Add metadata
        _add_metadata(payload, rec, source_tag or "blacks")

        if dry_run:
            continue
        
        # Check for duplicates
        if not overwrite and record_id in seen_ids:
            continue

        stem = (
            term.replace(" ", "_").replace("/", "-").replace("\\", "-").strip("._")
            or "term"
        )[:120]
        out_path = out / f"{stem}.json"
        
        # Handle file naming
        if overwrite and record_id in seen_ids:
            final_path = seen_ids[record_id]
        else:
            counter = 1
            final_path = out_path
            while final_path.exists():
                final_path = out / f"{stem}_{counter}.json"
                counter += 1
        
        final_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        written.append(final_path)
        seen_ids[record_id] = final_path

    if dry_run:
        print(f"[DRY RUN] Parsed {count} records (no files written)")
    
    return written


def normalize_amjur(
    source: pathlib.Path,
    out_dir: Optional[pathlib.Path] = None,
    source_tag: Optional[str] = None,
    dry_run: bool = False,
    limit: Optional[int] = None,
    overwrite: bool = False,
) -> List[pathlib.Path]:
    """Normalize American Jurisprudence entries into project case schema.

    Expected inputs (per record):
    - title: str (article title)
    - abstract: str (short summary)
    - body: str (full article text)

    Mappings:
    - case_name := title
    - summary := abstract or first 200 chars of body
    - opinion_text := body

    Args:
        source: Path to source JSON/JSONL file
        out_dir: Output directory for normalized cases
        source_tag: Optional provenance label for all records
        dry_run: If True, parse and report counts without writing files
        limit: Maximum number of records to process
        overwrite: If True, replace files with same ID; else append counter

    Returns:
        List of written file paths.
    """
    out = _ensure_out_dir(out_dir)
    written: List[pathlib.Path] = []
    seen_ids: Dict[str, pathlib.Path] = {}
    
    if not dry_run:
        for existing in out.glob("*.json"):
            try:
                with existing.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                if "id" in data:
                    seen_ids[data["id"]] = existing
            except (json.JSONDecodeError, IOError):
                pass

    count = 0
    for rec in _load_json_records(source):
        if limit is not None and count >= limit:
            break
        count += 1
        
        title = str(rec.get("title") or rec.get("name") or "Untitled Article")
        abstract = str(rec.get("abstract") or rec.get("summary") or "")
        body = str(rec.get("body") or rec.get("text") or "")
        
        summary = abstract or body[:200]

        # Compute stable ID
        record_id = _compute_stable_id(title, summary)

        payload: Dict[str, Any] = {
            "id": record_id,
            "case_name": title,
            "summary": summary,
        }
        if body:
            payload["opinion_text"] = body
        
        # Add metadata
        _add_metadata(payload, rec, source_tag or "amjur")

        if dry_run:
            continue
        
        # Check for duplicates
        if not overwrite and record_id in seen_ids:
            continue

        stem = (
            title.replace(" ", "_").replace("/", "-").replace("\\", "-").strip("._")
            or "article"
        )[:120]
        out_path = out / f"{stem}.json"
        
        # Handle file naming
        if overwrite and record_id in seen_ids:
            final_path = seen_ids[record_id]
        else:
            counter = 1
            final_path = out_path
            while final_path.exists():
                final_path = out / f"{stem}_{counter}.json"
                counter += 1
        
        final_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        written.append(final_path)
        seen_ids[record_id] = final_path

    if dry_run:
        print(f"[DRY RUN] Parsed {count} records (no files written)")
    
    return written

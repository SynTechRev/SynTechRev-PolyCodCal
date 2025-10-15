from __future__ import annotations

import hashlib
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


def _compute_id(case_name: str, summary: str) -> str:
    h = hashlib.sha1()
    h.update(case_name.encode("utf-8"))
    h.update(b"\n")
    h.update(summary.encode("utf-8"))
    return h.hexdigest()


def normalize_scotus(
    source: pathlib.Path,
    out_dir: Optional[pathlib.Path] = None,
    *,
    source_tag: Optional[str] = None,
    limit: Optional[int] = None,
    dry_run: bool = False,
    overwrite: bool = False,
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
    seen_ids: set[str] = set()

    count = 0
    for rec in _load_json_records(source):
        if limit is not None and count >= limit:
            break
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
        _id = _compute_id(case_name, summary)
        if _id in seen_ids:
            continue
        seen_ids.add(_id)

        payload: dict[str, object] = {
            "case_name": case_name,
            "summary": summary,
        }
        if facts is not None:
            payload["facts"] = facts
        if holding is not None:
            payload["holding"] = holding
        if opinion_text is not None:
            payload["opinion_text"] = opinion_text
        # Optional metadata
        payload["id"] = _id
        if source_tag:
            payload["source"] = source_tag

        # Derive filename from case name (safe-ish)
        stem = (
            case_name.replace(" ", "_").replace("/", "-").replace("\\", "-").strip("._")
            or "case"
        )
        # Avoid overly long filenames
        stem = stem[:120]
        out_path = out / f"{stem}.json"

        if dry_run:
            count += 1
            continue

        # Ensure uniqueness by appending counter if needed (unless overwrite)
        counter = 1
        final_path = out_path
        while final_path.exists() and not overwrite:
            final_path = out / f"{stem}_{counter}.json"
            counter += 1

        final_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        written.append(final_path)
        count += 1

    return written


def normalize_uscode(
    source: pathlib.Path,
    out_dir: Optional[pathlib.Path] = None,
    *,
    source_tag: Optional[str] = None,
    limit: Optional[int] = None,
    dry_run: bool = False,
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
    """
    out = _ensure_out_dir(out_dir)
    written: List[pathlib.Path] = []
    seen_ids: set[str] = set()

    count = 0
    for rec in _load_json_records(source):
        if limit is not None and count >= limit:
            break
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
        _id = _compute_id(case_name, summary)
        if _id in seen_ids:
            continue
        seen_ids.add(_id)

        payload: dict[str, object] = {
            "case_name": case_name,
            "summary": summary,
        }
        if text_str:
            payload["opinion_text"] = text_str
        payload["id"] = _id
        if source_tag:
            payload["source"] = source_tag

        stem = (
            case_name.replace(" ", "_").replace("/", "-").replace("\\", "-").strip("._")
            or "usc_section"
        )[:120]
        out_path = out / f"{stem}.json"
        if dry_run:
            count += 1
            continue

        counter = 1
        final_path = out_path
        while final_path.exists() and not overwrite:
            final_path = out / f"{stem}_{counter}.json"
            counter += 1
        final_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        written.append(final_path)
        count += 1

    return written


def normalize_blacks(
    source: pathlib.Path,
    out_dir: Optional[pathlib.Path] = None,
    *,
    source_tag: Optional[str] = None,
    limit: Optional[int] = None,
    dry_run: bool = False,
    overwrite: bool = False,
) -> List[pathlib.Path]:
    """Normalize Black's Law Dictionary entries.

    Expected flexible inputs (per record):
    - term: str
    - definition|def: str
    - examples: Optional[str|list]

    Mapping:
    - case_name := term
    - summary := first 200 chars of definition
    - opinion_text := definition (+ examples if present)
    """
    out = _ensure_out_dir(out_dir)
    written: List[pathlib.Path] = []
    seen_ids: set[str] = set()

    count = 0
    for rec in _load_json_records(source):
        if limit is not None and count >= limit:
            break
        term = str(rec.get("term") or rec.get("name") or "Untitled Term")
        definition = rec.get("definition") or rec.get("def") or ""
        examples = rec.get("examples")

        definition_str = (
            "\n\n".join(examples) if isinstance(examples, list) else str(examples or "")
        )
        full_text = f"{definition}\n\n{definition_str}".strip()
        summary = str(definition)[:200]

        _id = _compute_id(term, summary)
        if _id in seen_ids:
            continue
        seen_ids.add(_id)

        payload: dict[str, object] = {"case_name": term, "summary": summary, "id": _id}
        if full_text:
            payload["opinion_text"] = full_text
        if source_tag:
            payload["source"] = source_tag

        stem = (
            term.replace(" ", "_").replace("/", "-").replace("\\", "-").strip("._")
            or "blacks_term"
        )[:120]
        out_path = out / f"{stem}.json"
        if dry_run:
            count += 1
            continue

        counter = 1
        final_path = out_path
        while final_path.exists() and not overwrite:
            final_path = out / f"{stem}_{counter}.json"
            counter += 1
        final_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        written.append(final_path)
        count += 1

    return written


def normalize_amjur(
    source: pathlib.Path,
    out_dir: Optional[pathlib.Path] = None,
    *,
    source_tag: Optional[str] = None,
    limit: Optional[int] = None,
    dry_run: bool = False,
    overwrite: bool = False,
) -> List[pathlib.Path]:
    """Normalize American Jurisprudence-style articles.

    Expected flexible inputs (per record):
    - title: str
    - abstract: Optional[str]
    - body|text: Optional[str]

    Mapping:
    - case_name := title
    - summary := abstract or first 200 chars of body
    - opinion_text := body
    """
    out = _ensure_out_dir(out_dir)
    written: List[pathlib.Path] = []
    seen_ids: set[str] = set()

    count = 0
    for rec in _load_json_records(source):
        if limit is not None and count >= limit:
            break
        title = str(rec.get("title") or rec.get("name") or "Untitled Article")
        abstract = str(rec.get("abstract") or "")
        body = str(rec.get("body") or rec.get("text") or "")
        summary = abstract or body[:200]

        _id = _compute_id(title, summary)
        if _id in seen_ids:
            continue
        seen_ids.add(_id)

        payload: dict[str, object] = {"case_name": title, "summary": summary, "id": _id}
        if body:
            payload["opinion_text"] = body
        if source_tag:
            payload["source"] = source_tag

        stem = (
            title.replace(" ", "_").replace("/", "-").replace("\\", "-").strip("._")
            or "amjur_article"
        )[:120]
        out_path = out / f"{stem}.json"
        if dry_run:
            count += 1
            continue

        counter = 1
        final_path = out_path
        while final_path.exists() and not overwrite:
            final_path = out / f"{stem}_{counter}.json"
            counter += 1
        final_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        written.append(final_path)
        count += 1

    return written

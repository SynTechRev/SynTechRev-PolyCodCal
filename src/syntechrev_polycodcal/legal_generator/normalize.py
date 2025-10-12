"""Normalization adapters for legal data sources.

This module provides adapters to convert various legal data formats
(SCOTUS opinions, US Code sections, etc.) into the normalized JSON schema.
"""

from __future__ import annotations

import json
import pathlib
import re
import xml.etree.ElementTree as ET
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Any, Dict, List, Optional

from .config import BASE_DIR, CASE_DIR, DATA_DIR
from .schema import is_valid_record, validate_record


def normalize_scotus(
    source_dir: Optional[pathlib.Path] = None,
    output_dir: Optional[pathlib.Path] = None,
    parallel: bool = True,
) -> List[str]:
    """Normalize Supreme Court opinions to standard JSON format.

    Supports JSON, XML, and TXT formats. Handles common SCOTUS data formats
    from sources like CourtListener, Justia, and official repositories.

    Args:
        source_dir: Directory containing raw SCOTUS files (default: data/sources/scotus)
        output_dir: Output directory for normalized JSON (default: data/cases)
        parallel: Use parallel processing for large datasets

    Returns:
        List of normalized case file paths

    Example:
        >>> # Assuming data/sources/scotus/ contains raw files
        >>> paths = normalize_scotus()
        >>> len(paths)
        5
    """
    src_dir = source_dir or (DATA_DIR / "sources" / "scotus")
    out_dir = output_dir or CASE_DIR

    if not src_dir.exists():
        print(f"Source directory not found: {src_dir}")
        return []

    out_dir.mkdir(parents=True, exist_ok=True)

    # Find all supported files
    files: List[pathlib.Path] = []
    for pattern in ["*.json", "*.xml", "*.txt"]:
        files.extend(src_dir.glob(pattern))

    if not files:
        print(f"No files found in {src_dir}")
        return []

    print(f"Found {len(files)} SCOTUS files to normalize")

    if parallel and len(files) > 10:
        return _normalize_scotus_parallel(files, out_dir)
    else:
        return _normalize_scotus_sequential(files, out_dir)


def _normalize_scotus_sequential(
    files: List[pathlib.Path], out_dir: pathlib.Path
) -> List[str]:
    """Normalize SCOTUS files sequentially."""
    normalized: List[str] = []

    for file_path in files:
        try:
            record = _parse_scotus_file(file_path)
            if record:
                output_path = _save_normalized_record(record, out_dir, "SCOTUS")
                if output_path:
                    normalized.append(str(output_path))
                    print(f"✓ Normalized: {file_path.name}")
        except Exception as e:
            print(f"✗ Error processing {file_path.name}: {e}")

    return normalized


def _normalize_scotus_parallel(
    files: List[pathlib.Path], out_dir: pathlib.Path
) -> List[str]:
    """Normalize SCOTUS files in parallel."""
    normalized: List[str] = []

    with ProcessPoolExecutor() as executor:
        futures = {
            executor.submit(_parse_scotus_file, file_path): file_path
            for file_path in files
        }

        for future in as_completed(futures):
            file_path = futures[future]
            try:
                record = future.result()
                if record:
                    output_path = _save_normalized_record(record, out_dir, "SCOTUS")
                    if output_path:
                        normalized.append(str(output_path))
                        print(f"✓ Normalized: {file_path.name}")
            except Exception as e:
                print(f"✗ Error processing {file_path.name}: {e}")

    return normalized


def _parse_scotus_file(file_path: pathlib.Path) -> Optional[Dict[str, Any]]:
    """Parse a single SCOTUS file into normalized format."""
    suffix = file_path.suffix.lower()

    if suffix == ".json":
        return _parse_scotus_json(file_path)
    elif suffix == ".xml":
        return _parse_scotus_xml(file_path)
    elif suffix == ".txt":
        return _parse_scotus_txt(file_path)

    return None


def _parse_scotus_json(file_path: pathlib.Path) -> Optional[Dict[str, Any]]:
    """Parse SCOTUS JSON file (e.g., from CourtListener)."""
    try:
        with file_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        # Handle different JSON schemas
        case_name = (
            data.get("case_name")
            or data.get("caseName")
            or data.get("name")
            or data.get("title")
            or file_path.stem
        )

        summary = (
            data.get("summary")
            or data.get("opinion_text")
            or data.get("opinionText")
            or data.get("plain_text")
            or data.get("html")
            or data.get("content")
            or ""
        )

        # Clean HTML tags if present
        summary = re.sub(r"<[^>]+>", "", summary)

        record = {
            "case_name": str(case_name),
            "summary": summary.strip(),
            "source": "scotus",
        }

        # Optional fields
        if citation := data.get("citation") or data.get("cite"):
            record["citation"] = str(citation)

        if date := data.get("date") or data.get("decision_date"):
            record["date"] = _normalize_date(str(date))

        if jurisdiction := data.get("jurisdiction"):
            record["jurisdiction"] = str(jurisdiction)

        return record if is_valid_record(record) else None

    except Exception as e:
        print(f"Error parsing JSON {file_path.name}: {e}")
        return None


def _parse_scotus_xml(file_path: pathlib.Path) -> Optional[Dict[str, Any]]:
    """Parse SCOTUS XML file."""
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Try common XML structures
        case_name = (
            _get_xml_text(root, ".//case_name")
            or _get_xml_text(root, ".//title")
            or _get_xml_text(root, ".//name")
            or file_path.stem
        )

        summary = (
            _get_xml_text(root, ".//opinion")
            or _get_xml_text(root, ".//text")
            or _get_xml_text(root, ".//content")
            or _get_xml_text(root, ".//summary")
            or ""
        )

        record = {
            "case_name": str(case_name),
            "summary": summary.strip(),
            "source": "scotus",
        }

        # Optional fields
        if citation := _get_xml_text(root, ".//citation"):
            record["citation"] = citation

        if date := _get_xml_text(root, ".//date"):
            record["date"] = _normalize_date(date)

        return record if is_valid_record(record) else None

    except Exception as e:
        print(f"Error parsing XML {file_path.name}: {e}")
        return None


def _parse_scotus_txt(file_path: pathlib.Path) -> Optional[Dict[str, Any]]:
    """Parse SCOTUS plain text file."""
    try:
        with file_path.open("r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        # Use filename as case name, full content as summary
        record = {
            "case_name": file_path.stem.replace("_", " "),
            "summary": content.strip(),
            "source": "scotus",
        }

        return record if is_valid_record(record) else None

    except Exception as e:
        print(f"Error parsing TXT {file_path.name}: {e}")
        return None


def normalize_uscode(
    source_dir: Optional[pathlib.Path] = None,
    output_dir: Optional[pathlib.Path] = None,
    parallel: bool = True,
) -> List[str]:
    """Normalize U.S. Code sections to standard JSON format.

    Supports XML and TXT formats from sources like uscode.house.gov
    and govinfo.gov.

    Args:
        source_dir: Directory containing raw US Code files (default: data/sources/uscode)
        output_dir: Output directory for normalized JSON (default: data/cases)
        parallel: Use parallel processing for large datasets

    Returns:
        List of normalized file paths

    Example:
        >>> # Assuming data/sources/uscode/ contains raw files
        >>> paths = normalize_uscode()
        >>> len(paths)
        3
    """
    src_dir = source_dir or (DATA_DIR / "sources" / "uscode")
    out_dir = output_dir or CASE_DIR

    if not src_dir.exists():
        print(f"Source directory not found: {src_dir}")
        return []

    out_dir.mkdir(parents=True, exist_ok=True)

    # Find all supported files
    files: List[pathlib.Path] = []
    for pattern in ["*.xml", "*.txt"]:
        files.extend(src_dir.rglob(pattern))

    if not files:
        print(f"No files found in {src_dir}")
        return []

    print(f"Found {len(files)} US Code files to normalize")

    if parallel and len(files) > 10:
        return _normalize_uscode_parallel(files, out_dir)
    else:
        return _normalize_uscode_sequential(files, out_dir)


def _normalize_uscode_sequential(
    files: List[pathlib.Path], out_dir: pathlib.Path
) -> List[str]:
    """Normalize US Code files sequentially."""
    normalized: List[str] = []

    for file_path in files:
        try:
            record = _parse_uscode_file(file_path)
            if record:
                output_path = _save_normalized_record(record, out_dir, "USC")
                if output_path:
                    normalized.append(str(output_path))
                    print(f"✓ Normalized: {file_path.name}")
        except Exception as e:
            print(f"✗ Error processing {file_path.name}: {e}")

    return normalized


def _normalize_uscode_parallel(
    files: List[pathlib.Path], out_dir: pathlib.Path
) -> List[str]:
    """Normalize US Code files in parallel."""
    normalized: List[str] = []

    with ProcessPoolExecutor() as executor:
        futures = {
            executor.submit(_parse_uscode_file, file_path): file_path
            for file_path in files
        }

        for future in as_completed(futures):
            file_path = futures[future]
            try:
                record = future.result()
                if record:
                    output_path = _save_normalized_record(record, out_dir, "USC")
                    if output_path:
                        normalized.append(str(output_path))
                        print(f"✓ Normalized: {file_path.name}")
            except Exception as e:
                print(f"✗ Error processing {file_path.name}: {e}")

    return normalized


def _parse_uscode_file(file_path: pathlib.Path) -> Optional[Dict[str, Any]]:
    """Parse a single US Code file into normalized format."""
    suffix = file_path.suffix.lower()

    if suffix == ".xml":
        return _parse_uscode_xml(file_path)
    elif suffix == ".txt":
        return _parse_uscode_txt(file_path)

    return None


def _parse_uscode_xml(file_path: pathlib.Path) -> Optional[Dict[str, Any]]:
    """Parse US Code XML file."""
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Extract title and section information
        title = _get_xml_text(root, ".//title") or _get_xml_text(root, ".//num")
        section = _get_xml_text(root, ".//section") or _get_xml_text(root, ".//enum")
        heading = _get_xml_text(root, ".//heading") or ""

        case_name = f"USC Title {title} Section {section}"
        if heading:
            case_name += f" - {heading}"

        summary = (
            _get_xml_text(root, ".//text")
            or _get_xml_text(root, ".//content")
            or _get_xml_text(root, ".//chapeau")
            or ""
        )

        record = {
            "case_name": case_name,
            "summary": summary.strip(),
            "source": "uscode",
            "jurisdiction": "federal",
        }

        if title and section:
            record["citation"] = f"{title} U.S.C. § {section}"

        return record if is_valid_record(record) else None

    except Exception as e:
        print(f"Error parsing XML {file_path.name}: {e}")
        return None


def _parse_uscode_txt(file_path: pathlib.Path) -> Optional[Dict[str, Any]]:
    """Parse US Code plain text file."""
    try:
        with file_path.open("r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        # Try to extract title/section from filename or content
        filename = file_path.stem
        match = re.search(r"title[_\s]?(\d+).*?sec(?:tion)?[_\s]?(\d+)", filename, re.I)

        if match:
            title, section = match.groups()
            case_name = f"USC Title {title} Section {section}"
            citation = f"{title} U.S.C. § {section}"
        else:
            case_name = filename.replace("_", " ")
            citation = None

        record = {
            "case_name": case_name,
            "summary": content.strip(),
            "source": "uscode",
            "jurisdiction": "federal",
        }

        if citation:
            record["citation"] = citation

        return record if is_valid_record(record) else None

    except Exception as e:
        print(f"Error parsing TXT {file_path.name}: {e}")
        return None


def normalize_private(
    source_dir: Optional[pathlib.Path] = None,
    output_dir: Optional[pathlib.Path] = None,
) -> List[str]:
    """Normalize proprietary sources (Black's Law, AmJur) to standard JSON format.

    ⚠️  WARNING: Only use this with properly licensed content. Do NOT commit
    raw proprietary materials. This adapter reads from data/sources/private/
    which is excluded from version control.

    Args:
        source_dir: Directory containing licensed raw files (default: data/sources/private)
        output_dir: Output directory for normalized JSON (default: data/cases)

    Returns:
        List of normalized file paths

    Example:
        >>> # Assuming you have licensed content in data/sources/private/
        >>> paths = normalize_private()
        >>> len(paths)
        2
    """
    src_dir = source_dir or (DATA_DIR / "sources" / "private")
    out_dir = output_dir or CASE_DIR

    if not src_dir.exists():
        print(f"Source directory not found: {src_dir}")
        print("This is expected if you don't have licensed content.")
        return []

    out_dir.mkdir(parents=True, exist_ok=True)

    # Find all supported files
    files: List[pathlib.Path] = []
    for pattern in ["*.json", "*.xml", "*.txt"]:
        files.extend(src_dir.glob(pattern))

    if not files:
        print(f"No files found in {src_dir}")
        return []

    print(f"Found {len(files)} private source files to normalize")
    print("⚠️  Ensure you have proper licenses for this content")

    normalized: List[str] = []

    for file_path in files:
        try:
            record = _parse_private_file(file_path)
            if record:
                output_path = _save_normalized_record(record, out_dir, "PRIVATE")
                if output_path:
                    normalized.append(str(output_path))
                    print(f"✓ Normalized: {file_path.name}")
        except Exception as e:
            print(f"✗ Error processing {file_path.name}: {e}")

    return normalized


def _parse_private_file(file_path: pathlib.Path) -> Optional[Dict[str, Any]]:
    """Parse proprietary source file into normalized format."""
    suffix = file_path.suffix.lower()

    try:
        if suffix == ".json":
            with file_path.open("r", encoding="utf-8") as f:
                data = json.load(f)

            case_name = (
                data.get("term")
                or data.get("title")
                or data.get("name")
                or file_path.stem
            )
            summary = (
                data.get("definition")
                or data.get("text")
                or data.get("content")
                or data.get("summary")
                or ""
            )

            # Determine source type from filename
            source = "blackslaw" if "black" in file_path.name.lower() else "amjur"

            record = {
                "case_name": str(case_name),
                "summary": summary.strip(),
                "source": source,
            }

            if citation := data.get("citation"):
                record["citation"] = str(citation)

            return record if is_valid_record(record) else None

        elif suffix in [".xml", ".txt"]:
            # Simple text extraction
            if suffix == ".xml":
                tree = ET.parse(file_path)
                root = tree.getroot()
                content = ET.tostring(root, encoding="unicode", method="text")
            else:
                with file_path.open("r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()

            source = "blackslaw" if "black" in file_path.name.lower() else "amjur"

            record = {
                "case_name": file_path.stem.replace("_", " "),
                "summary": content.strip(),
                "source": source,
            }

            return record if is_valid_record(record) else None

    except Exception as e:
        print(f"Error parsing private file {file_path.name}: {e}")
        return None

    return None


# Helper functions


def _get_xml_text(element: ET.Element, xpath: str) -> str:
    """Extract text from XML element using xpath."""
    found = element.find(xpath)
    if found is not None and found.text:
        return found.text.strip()
    return ""


def _normalize_date(date_str: str) -> str:
    """Normalize date string to YYYY-MM-DD format."""
    # Try common formats
    for fmt in ["%Y-%m-%d", "%Y/%m/%d", "%m/%d/%Y", "%d-%m-%Y"]:
        try:
            from datetime import datetime

            dt = datetime.strptime(date_str[:10], fmt)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue
    # Return as-is if can't parse
    return date_str


def _save_normalized_record(
    record: Dict[str, Any], output_dir: pathlib.Path, prefix: str = ""
) -> Optional[pathlib.Path]:
    """Save normalized record to JSON file.

    Args:
        record: Normalized record dictionary
        output_dir: Output directory
        prefix: Optional prefix for filename

    Returns:
        Path to saved file, or None if validation failed
    """
    # Validate before saving
    errors = validate_record(record)
    if errors:
        print(f"Validation errors: {', '.join(errors)}")
        return None

    # Create safe filename from case_name
    case_name = record.get("case_name", "Unknown")
    safe_name = re.sub(r"[^\w\s-]", "", case_name)
    safe_name = re.sub(r"[-\s]+", "_", safe_name)
    safe_name = safe_name[:100]  # Limit length

    if prefix:
        filename = f"{prefix}_{safe_name}.json"
    else:
        filename = f"{safe_name}.json"

    output_path = output_dir / filename

    # Handle duplicates
    counter = 1
    while output_path.exists():
        if prefix:
            filename = f"{prefix}_{safe_name}_{counter}.json"
        else:
            filename = f"{safe_name}_{counter}.json"
        output_path = output_dir / filename
        counter += 1

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)

    return output_path

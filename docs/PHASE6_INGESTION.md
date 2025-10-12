# Phase 6 Ingestion Guide

This guide explains how to ingest legal data (Supreme Court cases, U.S. Code) into the Phase 6 scaffold, and how to handle proprietary works (e.g., Black's Law Dictionary, American Jurisprudence) safely and legally.

## ⚖️ Licensing & Content Policy

- Supreme Court opinions and U.S. Code are generally public domain. Verify source terms.
- Black's Law Dictionary (5th ed.) and American Jurisprudence are proprietary. Only ingest if you have a valid license. Do NOT commit proprietary content to the repository.
- This repo provides tooling to ingest from your local, licensed copies. It does not distribute copyrighted content.

## 📂 Directory Layout

```
data/
  cases/            # normalized JSON case records (used by current pipeline)
  vectors/          # generated embedding arrays (.npy)
  sources/          # raw source materials (not committed)
    scotus/         # SCOTUS opinions (JSON/TXT/XML as obtained)
    uscode/         # U.S. Code bulk titles (TXT/XML)
    private/        # proprietary sources (Black's, AmJur) — keep local only
```

Add a .gitignore entry to exclude `data/sources/**` if not already ignored.

## 🧱 Record Schema (normalized)

The ingest pipeline expects normalized JSON files under `data/cases/*.json` with at least:

```json
{
  "case_name": "Case Title or Document Name",
  "summary": "Main text (opinion/section/definition or concise summary)",
  "source": "scotus|uscode|blackslaw|amjur|custom",
  "citation": "optional",
  "date": "optional (YYYY-MM-DD)",
  "jurisdiction": "optional"
}
```

Minimal records work — the pipeline uses `summary` first, falling back to other fields, finally `case_name`.

## 🛠️ Ingestion Paths

1) Supreme Court cases (public domain)
- Obtain bulk downloads from reputable sources (e.g., official repositories or licensed providers).
- Convert to normalized JSON and place in `data/cases/`.

2) U.S. Code (public domain)
- Obtain bulk titles (TXT or XML) from official sources (e.g., uscode.house.gov or govinfo.gov).
- Convert to normalized JSON files per title/section and place in `data/cases/`.

3) Proprietary sources (licensed)
- Black's Law Dictionary (5th ed.) and American Jurisprudence: prepare normalized JSON locally.
- Place the files under `data/sources/private/` while transforming; do NOT commit these files.
- After normalization, place only the normalized JSON in `data/cases/` locally; keep it out of version control if it contains copyrighted text.

## 🚀 Running the Pipeline

- Ingest (reads `data/cases/*.json`, embeds, and saves vectors):

```powershell
python -m syntechrev_polycodcal.legal_generator.cli ingest
```

- Query:

```powershell
python -m syntechrev_polycodcal.legal_generator.cli query --text "due process violation" --top-k 5
```

## 🧪 Verifying Locally

- Add 1–2 JSON files under `data/cases/` with a `case_name` and `summary`.
- Run `ingest`, then `query` with relevant phrases; expect your cases to appear with highest similarity.

## 🔄 Normalization Adapters

Phase 6 includes automated adapters for common legal data sources:

### SCOTUS Adapter

Normalizes Supreme Court opinions from various formats:

```bash
# Place raw files in data/sources/scotus/
# Supports: *.json, *.xml, *.txt

python -m syntechrev_polycodcal.legal_generator.cli normalize scotus

# Disable parallel processing for debugging
python -m syntechrev_polycodcal.legal_generator.cli normalize scotus --no-parallel
```

**Supported formats:**
- JSON: CourtListener API format, Justia format, or any JSON with `case_name` and `opinion_text`
- XML: Common SCOTUS XML schemas with `<case_name>` and `<opinion>` tags
- TXT: Plain text opinions (uses filename as case name)

### US Code Adapter

Normalizes U.S. Code sections:

```bash
# Place raw files in data/sources/uscode/
# Supports: *.xml, *.txt

python -m syntechrev_polycodcal.legal_generator.cli normalize uscode

# Disable parallel processing for debugging
python -m syntechrev_polycodcal.legal_generator.cli normalize uscode --no-parallel
```

**Supported formats:**
- XML: Official U.S. Code XML from uscode.house.gov or govinfo.gov
- TXT: Plain text with title/section in filename (e.g., `title_42_section_1983.txt`)

### Private Sources Adapter

Normalizes proprietary content (Black's Law Dictionary, American Jurisprudence):

```bash
# Place licensed files in data/sources/private/
# ⚠️ Only use with valid licenses

python -m syntechrev_polycodcal.legal_generator.cli normalize private
```

**Important**: This adapter is for local use only. Never commit proprietary content to the repository.

## 🧪 Schema Validation

All adapters automatically validate records against the schema. Invalid records are rejected with descriptive error messages:

```python
from syntechrev_polycodcal.legal_generator.schema import validate_record

record = {"case_name": "Test", "summary": "Content"}
errors = validate_record(record)

if errors:
    print("Validation errors:", errors)
else:
    print("Record is valid!")
```

## ⚡ Parallel Processing

For large datasets (>10 files), adapters automatically use parallel processing:

- Uses Python's `ProcessPoolExecutor` for true parallelism
- Processes multiple files simultaneously
- Can be disabled with `--no-parallel` flag for debugging

## 🧱 Custom Adapters (Advanced)

To add a custom adapter for a new source:

1. Add parsing function in `src/syntechrev_polycodcal/legal_generator/normalize.py`
2. Follow the pattern of existing adapters (see `_parse_scotus_json` as example)
3. Return a dict matching the normalized schema
4. Validate with `is_valid_record()` before saving

Example:

```python
def _parse_custom_format(file_path: pathlib.Path) -> Optional[Dict[str, Any]]:
    """Parse custom format into normalized schema."""
    # Your parsing logic here
    record = {
        "case_name": "...",
        "summary": "...",
        "source": "custom",
    }
    return record if is_valid_record(record) else None
```

## ✅ Best Practices

- **Keep raw sources in `data/sources/`** and out of version control (already in `.gitignore`)
- **Normalize to `data/cases/`** using the minimal schema above
- **Re-run `ingest`** whenever you add/update cases to rebuild embeddings
- **Be mindful of copyright** - when in doubt, don't commit the content
- **Use parallel processing** for large datasets to improve performance
- **Validate all records** before ingestion to ensure data quality

## 📊 Example Workflow

Complete workflow for ingesting SCOTUS cases:

```bash
# 1. Place raw SCOTUS files in data/sources/scotus/
#    (e.g., download from CourtListener, Justia, etc.)

# 2. Normalize to standard JSON format
python -m syntechrev_polycodcal.legal_generator.cli normalize scotus

# 3. Build embeddings from normalized cases
python -m syntechrev_polycodcal.legal_generator.cli ingest

# 4. Query the knowledge base
python -m syntechrev_polycodcal.legal_generator.cli query --text "search warrant" --top-k 5
```

## 🔍 Testing Adapters

Run tests to verify adapter functionality:

```bash
# Run all legal generator tests
PYTHONPATH=src pytest tests/test_legal_generator_*.py -v

# Run only schema validation tests
PYTHONPATH=src pytest tests/test_legal_generator_schema.py -v

# Run only normalization adapter tests
PYTHONPATH=src pytest tests/test_legal_generator_normalize.py -v
```

---

For help with a specific data format or to report issues, please open a GitHub issue with sample data (public domain only).

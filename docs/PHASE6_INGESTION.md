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
  "id": "stable-hash-of-case-and-summary",
  "case_name": "Case Title or Document Name",
  "summary": "Main text (opinion/section/definition or concise summary)",
  "schema_version": "1.0",
  "source": "scotus|uscode|blacks|amjur|custom",
  "citation": "optional",
  "date": "optional (YYYY-MM-DD)",
  "jurisdiction": "optional"
}
```

**Required Fields:**
- `case_name`: string (non-empty)
- `summary`: string (non-empty)

**Optional Metadata:**
- `id`: stable hash for deduplication (auto-generated if not provided)
- `schema_version`: currently "1.0"
- `source`: provenance tag indicating origin
- `citation`: legal citation (e.g., "123 U.S. 456")
- `date`: ISO date (YYYY-MM-DD)
- `jurisdiction`: applicable jurisdiction

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


```bash
# POSIX - Default append mode
PYTHONPATH=src python -m syntechrev_polycodcal.legal_generator.cli ingest

# Rebuild mode (clear and rebuild from scratch)
PYTHONPATH=src python -m syntechrev_polycodcal.legal_generator.cli ingest --rebuild
```

```powershell
# Windows - Default append mode
python -m syntechrev_polycodcal.legal_generator.cli ingest

# Rebuild mode
python -m syntechrev_polycodcal.legal_generator.cli ingest --rebuild
```

**Ingest Modes:**
- `--append` (default): Process all current cases and create new embeddings
- `--rebuild`: Same as append in current implementation (future: incremental support)

**Output:**
- `data/vectors/case_embeddings.npz`: Compressed numpy array with names and embeddings
- `data/vectors/vectors.meta.json`: Metadata file containing:
  - `model`: Embedding model name
  - `created_at`: ISO timestamp
  - `count`: Number of cases
  - `dim`: Embedding dimension
  - `file_version`: Schema version
  - `names_hash`: Hash of names array for verification

### Normalize Quickstart (SCOTUS Adapter)

You can now normalize upstream datasets into the project schema with a built-in adapter:

```bash
# SCOTUS-like JSONL/JSON -> normalized case JSON files
PYTHONPATH=src python -m syntechrev_polycodcal.legal_generator.cli normalize \
  --adapter scotus \
  --source path/to/scotus.jsonl \
  --out data/cases \
  --source-tag "scotus-2024"

# Ingest and build vectors
PYTHONPATH=src python -m syntechrev_polycodcal.legal_generator.cli ingest

# Query
PYTHONPATH=src python -m syntechrev_polycodcal.legal_generator.cli query --text "equal protection"
```

**Windows (PowerShell):**
```powershell
$env:PYTHONPATH = "src"
python -m syntechrev_polycodcal.legal_generator.cli normalize `
  --adapter scotus `
  --source path\to\scotus.jsonl `
  --out data\cases `
  --source-tag "scotus-2024"
```

**Normalize Flags:**
- `--source` (required): Path to `.jsonl` (one JSON per line) or `.json` (list or single object)
- `--out`: Output directory (defaults to `data/cases`)
- `--adapter`: Normalization adapter (`scotus`, `uscode`, `blacks`, `amjur`)
- `--source-tag`: Provenance label applied to all records
- `--dry-run`: Parse and report counts without writing files
- `--limit N`: Process at most N records
- `--overwrite`: Replace files with same ID; default appends counter

Notes:
- The adapter maps flexible fields like `title`/`name` to `case_name` and `syllabus`/`headnote` to `summary`.
- Each record gets a stable ID hash computed from `case_name + summary`
- Duplicate IDs are automatically skipped unless `--overwrite` is used

### Normalize U.S. Code

```bash
# JSON list of objects with fields like: title, section, heading, text
PYTHONPATH=src python -m syntechrev_polycodcal.legal_generator.cli normalize \
  --adapter uscode \
  --source path/to/uscode.json \
  --out data/cases

PYTHONPATH=src python -m syntechrev_polycodcal.legal_generator.cli ingest
PYTHONPATH=src python -m syntechrev_polycodcal.legal_generator.cli query --text "civil rights action"
```

**Windows (PowerShell):**
```powershell
python -m syntechrev_polycodcal.legal_generator.cli normalize `
  --adapter uscode `
  --source path\to\uscode.json `
  --out data\cases
```

### Normalize Black's Law Dictionary

```bash
# JSON with fields: term, definition, examples (optional)
PYTHONPATH=src python -m syntechrev_polycodcal.legal_generator.cli normalize \
  --adapter blacks \
  --source path/to/blacks.jsonl \
  --source-tag "blacks-5th-ed"
```

**Input Schema:**
- `term` or `title`: Legal term
- `definition` or `text`: Main definition
- `examples`: Optional usage examples (string or list)

### Normalize American Jurisprudence

```bash
# JSON with fields: title, abstract, body
PYTHONPATH=src python -m syntechrev_polycodcal.legal_generator.cli normalize \
  --adapter amjur \
  --source path/to/amjur.json \
  --source-tag "amjur-2024"
```

**Input Schema:**
- `title` or `name`: Article title
- `abstract` or `summary`: Short summary
- `body` or `text`: Full article text

### Query Examples

```bash
# POSIX
PYTHONPATH=src python -m syntechrev_polycodcal.legal_generator.cli query \
  --text "due process violation" \
  --top-k 5
```

```powershell
# Windows
python -m syntechrev_polycodcal.legal_generator.cli query `
  --text "due process violation" `
  --top-k 5
```

## 🔑 Deduplication & ID Generation

Each normalized case receives a stable ID computed as a hash of `case_name + summary`. This enables:

1. **Automatic deduplication**: Duplicate records (same case_name and summary) are skipped by default
2. **Idempotent normalization**: Running normalize multiple times won't create duplicates
3. **Controlled overwrites**: Use `--overwrite` to replace existing records with matching IDs

**Example workflow:**

```bash
# First run: creates Test_Case.json with ID abc123
PYTHONPATH=src python -m syntechrev_polycodcal.legal_generator.cli normalize \
  --adapter scotus --source cases1.json

# Second run: skips if same ID exists
PYTHONPATH=src python -m syntechrev_polycodcal.legal_generator.cli normalize \
  --adapter scotus --source cases2.json

# Force overwrite of existing IDs
PYTHONPATH=src python -m syntechrev_polycodcal.legal_generator.cli normalize \
  --adapter scotus --source cases_updated.json --overwrite
```

**ID Stability:**
- Same `case_name + summary` → same ID
- Changed summary → different ID (treated as new record)
- IDs are 16-character hex strings (SHA256 truncated)

## 🔍 Validator

Validate normalized cases for schema compliance:

```bash
# POSIX
PYTHONPATH=src python -m syntechrev_polycodcal.legal_generator.cli validate

# With custom directory
PYTHONPATH=src python -m syntechrev_polycodcal.legal_generator.cli validate --dir path/to/cases
```

```powershell
# Windows
python -m syntechrev_polycodcal.legal_generator.cli validate
python -m syntechrev_polycodcal.legal_generator.cli validate --dir path\to\cases
```

The validator checks:
- Required fields present (`case_name`, `summary`)
- Field types are correct (strings for text fields)
- Non-empty values for required fields
- Valid JSON structure

Exit code 0 indicates success; non-zero indicates validation failures with error details printed to stdout.

## 🧪 Verifying Locally

- Add 1–2 JSON files under `data/cases/` with a `case_name` and `summary`.
- Run `validate` to check schema compliance
- Run `ingest`, then `query` with relevant phrases; expect your cases to appear with highest similarity.

## 📊 Adapter Mapping Tables

### SCOTUS Adapter
| Source Field | Mapped To | Notes |
|--------------|-----------|-------|
| `case_name` / `title` / `name` | `case_name` | First available used |
| `summary` / `syllabus` / `headnote` | `summary` | First available used |
| `facts` | `facts` | Optional passthrough |
| `holding` | `holding` | Optional passthrough |
| `opinion_text` / `opinion` | `opinion_text` | Optional passthrough |
| `citation` | `citation` | Optional metadata |
| `date` | `date` | Optional metadata |
| `jurisdiction` | `jurisdiction` | Optional metadata |

### U.S. Code Adapter
| Source Field | Mapped To | Notes |
|--------------|-----------|-------|
| `title` | Part of `case_name` | "USC Title {title}" |
| `section` / `sec` | Part of `case_name` | "§{section}" |
| `heading` / `caption` | `summary` + part of `case_name` | Primary summary source |
| `text` / `body` | `opinion_text` | Full section text |

Output format: `case_name = "USC Title 42 §1983: Civil action for deprivation of rights"`

### Black's Law Dictionary Adapter
| Source Field | Mapped To | Notes |
|--------------|-----------|-------|
| `term` / `title` | `case_name` | Legal term name |
| `definition` / `text` | `summary` | Main definition |
| `examples` | `opinion_text` | String or list (joined with spaces) |

Default `source` tag: `"blacks"`

### American Jurisprudence Adapter
| Source Field | Mapped To | Notes |
|--------------|-----------|-------|
| `title` / `name` | `case_name` | Article title |
| `abstract` / `summary` | `summary` | Falls back to first 200 chars of body |
| `body` / `text` | `opinion_text` | Full article text |

Default `source` tag: `"amjur"`

## 🔄 Custom Importers (Advanced)

You can build source-specific importers that read from `data/sources/<source>` and output normalized JSON under `data/cases/`. Keep proprietary materials local and out of git.

- Example pattern:
  - `sources/scotus/*.json|*.xml` → normalize → `data/cases/CaseName.json`
  - `sources/uscode/TitleXX/*.xml|*.txt` → normalize sections → `data/cases/USC_TitleXX_SecYYY.json`
  - `sources/private/` → normalize locally → output not committed

## ✅ Best Practices

- Keep raw sources in `data/sources/` and out of version control.
- Normalize to `data/cases/` using the minimal schema above.
- Re-run `ingest` whenever you add/update cases.
- Be mindful of copyright; when in doubt, don’t commit the content.

---

For help building a specific importer (e.g., US Code XML → JSON), open an issue or ask for an adapter targeting your source format.

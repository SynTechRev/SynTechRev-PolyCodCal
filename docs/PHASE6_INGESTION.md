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


```powershell
python -m syntechrev_polycodcal.legal_generator.cli ingest
```

### Normalize Quickstart (SCOTUS Adapter)

You can now normalize upstream datasets into the project schema with a built-in adapter:

```bash
# SCOTUS-like JSONL/JSON -> normalized case JSON files
PYTHONPATH=src python -m syntechrev_polycodcal.legal_generator.cli normalize --adapter scotus --source path/to/scotus.jsonl --out data/cases

# Ingest and build vectors
PYTHONPATH=src python -m syntechrev_polycodcal.legal_generator.cli ingest

# Query
PYTHONPATH=src python -m syntechrev_polycodcal.legal_generator.cli query --text "equal protection"
```

Notes:
- `--source` accepts `.jsonl` (one JSON per line) or `.json` (list or single object).
- `--out` defaults to `data/cases` if omitted.
- The adapter maps flexible fields like `title`/`name` to `case_name` and `syllabus`/`headnote` to `summary`.

### Normalize U.S. Code
### Normalize Proprietary Sources (Local Only)

Examples (do not commit proprietary text):

```powershell
# Black's Law Dictionary
python -m syntechrev_polycodcal.legal_generator.cli normalize --adapter blacks --source data\sources\private\blacks.json --out data\cases --source-tag blacks

# American Jurisprudence
python -m syntechrev_polycodcal.legal_generator.cli normalize --adapter amjur --source data\sources\private\amjur.jsonl --out data\cases --source-tag amjur
```

Then ingest and query as usual.

```bash
# JSON list of objects with fields like: title, section, heading, text
PYTHONPATH=src python -m syntechrev_polycodcal.legal_generator.cli normalize --adapter uscode --source path/to/uscode.json --out data/cases

PYTHONPATH=src python -m syntechrev_polycodcal.legal_generator.cli ingest
PYTHONPATH=src python -m syntechrev_polycodcal.legal_generator.cli query --text "civil rights action"
```

- Query:

```powershell
python -m syntechrev_polycodcal.legal_generator.cli query --text "due process violation" --top-k 5
```

## 🧪 Verifying Locally

- Add 1–2 JSON files under `data/cases/` with a `case_name` and `summary`.
- Run `ingest`, then `query` with relevant phrases; expect your cases to appear with highest similarity.

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

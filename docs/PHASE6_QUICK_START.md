# Phase 6 Quick Start Guide

This guide walks you through using the Phase 6 legal data ingestion system from start to finish.

## Prerequisites

1. Python 3.11+ installed
2. Dependencies installed: `pip install -r dev-requirements.txt`
3. Repository cloned and set up

## Step-by-Step Walkthrough

### 1. Explore Example Cases

The repository includes 5 example legal cases ready to use:

```bash
ls -lh data/cases/
```

You should see:
- `Miranda_v_Arizona.json`
- `Brown_v_Board_of_Education.json`
- `Gideon_v_Wainwright.json`
- `Roe_v_Wade.json`
- `USC_Title_42_Sec_1983.json`

### 2. Ingest Example Cases

Build embeddings from the example cases:

```bash
python -m syntechrev_polycodcal.legal_generator.cli ingest
```

Output:
```
Ingested 5 cases.
```

### 3. Query the Knowledge Base

Search for similar cases:

```bash
python -m syntechrev_polycodcal.legal_generator.cli query --text "right to counsel" --top-k 3
```

Expected output:
```
Gideon v. Wainwright                     similarity=0.856
Miranda v. Arizona                       similarity=0.742
Brown v. Board of Education              similarity=0.521
```

### 4. Add Your Own Data

#### Option A: Create Normalized JSON Directly

Create a file in `data/cases/`:

```bash
cat > data/cases/My_Case.json << 'EOF'
{
  "case_name": "My Test Case",
  "summary": "This is a test case about contract law and breach of duty.",
  "source": "custom",
  "citation": "123 Test 456",
  "date": "2024-01-15"
}
EOF
```

Then re-ingest:

```bash
python -m syntechrev_polycodcal.legal_generator.cli ingest
```

#### Option B: Use Normalization Adapters

Place raw legal data in the appropriate `data/sources/` subdirectory, then normalize:

**For SCOTUS opinions:**

```bash
# Place JSON/XML/TXT files in data/sources/scotus/
python -m syntechrev_polycodcal.legal_generator.cli normalize scotus
```

**For U.S. Code sections:**

```bash
# Place XML/TXT files in data/sources/uscode/
python -m syntechrev_polycodcal.legal_generator.cli normalize uscode
```

**For proprietary sources (if licensed):**

```bash
# Place licensed files in data/sources/private/
python -m syntechrev_polycodcal.legal_generator.cli normalize private
```

After normalization, run ingest:

```bash
python -m syntechrev_polycodcal.legal_generator.cli ingest
```

### 5. Advanced Queries

Try different query types:

**Search for due process violations:**
```bash
python -m syntechrev_polycodcal.legal_generator.cli query --text "due process violation" --top-k 5
```

**Search for civil rights cases:**
```bash
python -m syntechrev_polycodcal.legal_generator.cli query --text "civil rights equal protection" --top-k 3
```

**Search for statutory text:**
```bash
python -m syntechrev_polycodcal.legal_generator.cli query --text "color of law deprivation" --top-k 3
```

## Command Reference

### CLI Commands

```bash
# Get help
python -m syntechrev_polycodcal.legal_generator.cli --help

# Normalize data
python -m syntechrev_polycodcal.legal_generator.cli normalize --help
python -m syntechrev_polycodcal.legal_generator.cli normalize scotus
python -m syntechrev_polycodcal.legal_generator.cli normalize uscode
python -m syntechrev_polycodcal.legal_generator.cli normalize private

# Ingest cases
python -m syntechrev_polycodcal.legal_generator.cli ingest

# Query
python -m syntechrev_polycodcal.legal_generator.cli query --text "your query" --top-k 5
```

### Python API

Use the modules programmatically:

```python
from syntechrev_polycodcal.legal_generator.normalize import normalize_scotus
from syntechrev_polycodcal.legal_generator.ingest import ingest_cases
from syntechrev_polycodcal.legal_generator.retriever import search
from syntechrev_polycodcal.legal_generator.embedder import Embedder

# Normalize SCOTUS data
paths = normalize_scotus()
print(f"Normalized {len(paths)} cases")

# Ingest cases
names, embeddings = ingest_cases()
print(f"Ingested {len(names)} cases")

# Query
embedder = Embedder()
query_emb = embedder.encode_texts(["search warrant"])[0]
results = search(query_emb, top_k=3)

for case_name, similarity in results:
    print(f"{case_name}: {similarity:.3f}")
```

## Troubleshooting

### No results from query

**Problem**: `query` returns "No results found"

**Solution**: Make sure you ran `ingest` first:
```bash
python -m syntechrev_polycodcal.legal_generator.cli ingest
```

### Validation errors during normalization

**Problem**: "Validation errors: Missing required field: summary"

**Solution**: Ensure your source files contain the required data. Check the schema:
```python
from syntechrev_polycodcal.legal_generator.schema import validate_record

record = {"case_name": "Test", "summary": "Content"}
errors = validate_record(record)
print(errors)  # Should be []
```

### Source directory not found

**Problem**: "Source directory not found: data/sources/scotus"

**Solution**: Create the directory and add files:
```bash
mkdir -p data/sources/scotus
# Add your source files here
```

## Next Steps

- Read the [full ingestion guide](PHASE6_INGESTION.md) for details on data formats
- See the [README](../README.md) for project overview
- Check [CONTRIBUTING.md](../CONTRIBUTING.md) for development guidelines

## Example Workflow Script

Here's a complete script to normalize and ingest SCOTUS data:

```bash
#!/bin/bash
set -e

echo "Phase 6 Ingestion Workflow"
echo "=========================="

# Step 1: Check for source files
if [ ! -d "data/sources/scotus" ]; then
    echo "Creating sources directory..."
    mkdir -p data/sources/scotus
    echo "Add your SCOTUS files to data/sources/scotus/"
    exit 1
fi

# Step 2: Normalize SCOTUS data
echo "Normalizing SCOTUS data..."
python -m syntechrev_polycodcal.legal_generator.cli normalize scotus

# Step 3: Ingest all cases
echo "Ingesting cases..."
python -m syntechrev_polycodcal.legal_generator.cli ingest

# Step 4: Test query
echo "Testing query..."
python -m syntechrev_polycodcal.legal_generator.cli query --text "fourth amendment" --top-k 3

echo "Done!"
```

Save as `scripts/ingest_workflow.sh` and run with `bash scripts/ingest_workflow.sh`.

## Resources

- [PHASE6_INGESTION.md](PHASE6_INGESTION.md) - Detailed ingestion guide
- [Data Directory README](../data/README.md) - Data structure explanation
- Module documentation in `src/syntechrev_polycodcal/legal_generator/`

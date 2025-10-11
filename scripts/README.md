# Scripts Directory

This directory contains utility scripts for development, testing, and release management.

## Release Management Scripts

### create_release_tag.sh

**Purpose:** Automate the creation of release tags with proper validation and cleanup.

**Usage:**
```bash
./scripts/create_release_tag.sh <version> [message]
```

**Examples:**
```bash
# Create v0.1.0 tag with default message
./scripts/create_release_tag.sh v0.1.0

# Create tag with custom message
./scripts/create_release_tag.sh v0.1.0 "Release v0.1.0 - Initial stable release"
```

**Features:**
- ✅ Validates semantic versioning format (vX.Y.Z)
- ✅ Checks for existing tags (local and remote)
- ✅ Verifies working directory status
- ✅ Cleans build artifacts automatically
- ✅ Verifies CHANGELOG.md contains version entry
- ✅ Creates annotated Git tag
- ✅ Interactive push confirmation
- ✅ Helpful error messages with solutions
- ✅ Colored output for clarity

**See Also:** [TAGGING_GUIDE.md](../TAGGING_GUIDE.md) for detailed tagging documentation

---

### cleanup_repo.sh

**Purpose:** Safely remove Python build artifacts and caches without touching source code.

**Usage:**
```bash
./scripts/cleanup_repo.sh
```

**What It Removes:**
- Python bytecode cache (`__pycache__/`, `*.pyc`, `*.pyo`)
- Egg info directories (`*.egg-info/`)
- Build directories (`build/`, `dist/`)
- Test artifacts (`.pytest_cache/`, `.coverage`, `htmlcov/`)
- Linter caches (`.mypy_cache/`, `.ruff_cache/`)
- Editor files (`.DS_Store`, `Thumbs.db`)

**What It Preserves:**
- ✅ All source code
- ✅ Configuration files
- ✅ Virtual environments
- ✅ Git history
- ✅ Documentation

**Features:**
- ✅ Safe - only removes generated files
- ✅ Shows what was cleaned
- ✅ Displays git status after cleanup
- ✅ Works on all platforms
- ✅ Can be run anytime

---

## Application Scripts

### feedback_monitor.py

**Purpose:** Command-line interface for the FeedbackMonitor system.

**Usage:**
```bash
# Run with example data
PYTHONPATH=src python scripts/feedback_monitor.py

# Run with custom data
PYTHONPATH=src python scripts/feedback_monitor.py --input examples/events.jsonl
```

**See Also:** [README.md](../README.md#feedbackmonitor-usage) for usage details

---

### legal_data_report.py

**Purpose:** Generate reports from legal data with AI augmentation.

**Usage:**
```bash
PYTHONPATH=src python scripts/legal_data_report.py
```

**See Also:** [docs/AI_LEGAL_DATA_GENERATOR_OVERVIEW.md](../docs/AI_LEGAL_DATA_GENERATOR_OVERVIEW.md)

---

## Making Scripts Executable

If you need to make a script executable:

```bash
chmod +x scripts/script_name.sh
```

All shell scripts in this directory should already be executable.

## Common Workflows

### Before Creating a Release

```bash
# 1. Clean the repository
./scripts/cleanup_repo.sh

# 2. Run tests to ensure everything works
PYTHONPATH=src pytest -v

# 3. Create the release tag
./scripts/create_release_tag.sh v0.1.0 "Release description"
```

### Regular Maintenance

```bash
# Run cleanup periodically to remove accumulated artifacts
./scripts/cleanup_repo.sh

# Shows what was cleaned and current git status
```

### Testing the FeedbackMonitor

```bash
# Run the example script
PYTHONPATH=src python scripts/feedback_monitor.py

# Monitor the output for alerts
```

## Troubleshooting

### Script Won't Run (Permission Denied)

**Problem:** `bash: ./scripts/script.sh: Permission denied`

**Solution:**
```bash
chmod +x scripts/script.sh
```

### Python Scripts Can't Find Modules

**Problem:** `ModuleNotFoundError: No module named 'syntechrev_polycodcal'`

**Solution:**
```bash
# Add src to PYTHONPATH
PYTHONPATH=src python scripts/script.py

# Or in VS Code, it's automatically configured
```

### Cleanup Script Seems to Do Nothing

**Problem:** Script runs but shows "Repository is already clean!"

**Solution:** This is normal! It means there are no artifacts to clean. The repository is in a good state.

---

## Adding New Scripts

When adding new scripts to this directory:

1. **Name clearly:** Use descriptive names (e.g., `run_benchmarks.sh`)
2. **Add shebang:** Start with `#!/bin/bash` or `#!/usr/bin/env python3`
3. **Make executable:** `chmod +x scripts/new_script.sh`
4. **Document here:** Add entry to this README
5. **Add to .gitignore if needed:** Generated outputs should be ignored

### Example Shell Script Template

```bash
#!/bin/bash
# Description of what this script does

set -e  # Exit on error

# Your script here
echo "Running..."
```

### Example Python Script Template

```python
#!/usr/bin/env python3
"""Description of what this script does."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

def main():
    """Main function."""
    print("Running...")

if __name__ == "__main__":
    main()
```

---

## Script Dependencies

### Shell Scripts
- Bash 4.0+
- Git
- Standard Unix utilities (find, rm, etc.)

### Python Scripts
- Python 3.11+
- Project dependencies (install with `pip install -r dev-requirements.txt`)
- PYTHONPATH=src environment variable (or VS Code workspace)

---

For more information, see:
- [CONTRIBUTING.md](../CONTRIBUTING.md) - Contribution guidelines
- [TAGGING_GUIDE.md](../TAGGING_GUIDE.md) - Release tagging guide
- [README.md](../README.md) - Project overview

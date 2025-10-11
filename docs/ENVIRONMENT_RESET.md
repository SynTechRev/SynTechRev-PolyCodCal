# Environment Reset Guide

This guide helps you reset your development environment and resolve VSCode integration issues, especially after major PRs like PR #5 that include comprehensive configuration changes.

## When to Use This Guide

Use this guide if you experience:
- VSCode not recognizing the Python interpreter
- Import errors despite having dependencies installed
- Conflicts between local changes and GitHub repository state
- Testing or linting tools not working correctly
- GitHub Copilot integration issues

## Quick Reset (5 minutes)

### 1. Clean Up Local Environment

**Remove virtual environment:**
```bash
# On Windows (PowerShell)
Remove-Item -Recurse -Force .venv

# On macOS/Linux
rm -rf .venv
```

**Remove Python cache files:**
```bash
# On Windows (PowerShell)
Get-ChildItem -Path . -Include __pycache__,*.pyc,*.pyo -Recurse -Force | Remove-Item -Recurse -Force

# On macOS/Linux
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete
find . -type f -name "*.pyo" -delete
```

**Remove test and coverage cache:**
```bash
# Cross-platform
rm -rf .pytest_cache htmlcov .coverage coverage.xml .mypy_cache .ruff_cache
```

### 2. Sync with GitHub Repository

**Check current state:**
```bash
git status
git branch -a
```

**If you have uncommitted changes you want to keep:**
```bash
git stash save "backup before reset"
```

**Reset to match GitHub main branch:**
```bash
# Fetch latest from GitHub
git fetch origin

# If on a feature branch, update it
git checkout copilot/fix-vsc-environment-issue
git pull origin copilot/fix-vsc-environment-issue

# Or switch to main if available
git checkout main
git pull origin main
```

**If you stashed changes and want them back:**
```bash
git stash pop
```

**If you want to completely discard local changes:**
```bash
git reset --hard origin/main
# Or: git reset --hard origin/copilot/fix-vsc-environment-issue
```

### 3. Recreate Virtual Environment

**Create fresh virtual environment:**
```bash
# On Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# On macOS/Linux
python -m venv .venv
source .venv/bin/activate
```

**Upgrade pip:**
```bash
python -m pip install --upgrade pip
```

**Install dependencies:**
```bash
# Install development dependencies
pip install -r dev-requirements.txt

# Install project in editable mode
pip install -e .
```

### 4. Verify Installation

**Run tests:**
```bash
PYTHONPATH=src pytest -v
```

Expected output:
```
================ 15 passed in 0.04s ================
```

**Run linting:**
```bash
ruff check .
black --check src tests scripts
mypy src
```

### 5. Reload VSCode

**In VSCode:**
1. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
2. Type: "Reload Window"
3. Press Enter

**Or restart VSCode completely:**
- Close VSCode
- Reopen the project folder

### 6. Select Python Interpreter

**In VSCode:**
1. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
2. Type: "Python: Select Interpreter"
3. Choose the one showing `.venv` (e.g., `./venv/bin/python`)

**Verify interpreter:**
- Open a Python file
- Check bottom-right corner of VSCode shows: `Python 3.x.x ('.venv': venv)`

### 7. Verify VSCode Features

**Test integrated terminal:**
1. Open terminal in VSCode (`` Ctrl+` ``)
2. Verify virtual environment is activated (prompt shows `.venv` or `(venv)`)
3. Run: `python --version`

**Test testing integration:**
1. Open Testing panel (beaker icon in sidebar)
2. Click "Refresh Tests"
3. All 15 tests should appear
4. Run tests from panel

**Test formatting:**
1. Open any Python file
2. Make a formatting change
3. Save file (`Ctrl+S`)
4. Verify Black auto-formats the file

## Cross-Platform Compatibility

### Path Separators

VSCode settings use forward slashes (`/`) which work on all platforms:
```json
"python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python"
```

On Windows, this automatically translates to:
```
C:\path\to\project\.venv\Scripts\python.exe
```

### PYTHONPATH Configuration

The `.vscode/settings.json` sets PYTHONPATH for all platforms:
```json
"terminal.integrated.env.linux": {
  "PYTHONPATH": "${workspaceFolder}/src"
},
"terminal.integrated.env.osx": {
  "PYTHONPATH": "${workspaceFolder}/src"
},
"terminal.integrated.env.windows": {
  "PYTHONPATH": "${workspaceFolder}/src"
}
```

### Virtual Environment Activation

**Windows:**
- PowerShell: `.\.venv\Scripts\Activate.ps1`
- Command Prompt: `.\.venv\Scripts\activate.bat`

**macOS/Linux:**
- Bash/Zsh: `source .venv/bin/activate`

## GitHub Copilot Integration

### Verify Copilot Extensions

**Required extensions:**
- `GitHub.copilot`
- `GitHub.copilot-chat`

**Check if installed:**
1. Press `Ctrl+Shift+X` (Extensions panel)
2. Search for "GitHub Copilot"
3. Verify both extensions are installed and enabled

### Copilot Settings in VSCode

The project includes Copilot-specific settings in `.vscode/settings.json`:
```json
"github.copilot.enable": {
  "*": true,
  "yaml": true,
  "plaintext": true,
  "markdown": true,
  "python": true
},
"github.copilot.editor.enableAutoCompletions": true
```

### Copilot Instructions

The project includes `.github/copilot-instructions.md` which provides:
- Project architecture overview
- Code style guidelines
- Testing conventions
- Common patterns

This helps Copilot provide better suggestions specific to this project.

### Test Copilot

1. Open a Python file
2. Start typing a function
3. Copilot should suggest completions (gray text)
4. Press `Tab` to accept

## Troubleshooting

### Issue: "Module not found" errors

**Solution:**
```bash
# Verify PYTHONPATH includes src directory
echo $PYTHONPATH  # macOS/Linux
echo $env:PYTHONPATH  # Windows PowerShell

# Should show: /path/to/project/src

# If not set, reload VSCode or manually set:
export PYTHONPATH="${PWD}/src"  # macOS/Linux
$env:PYTHONPATH = "${PWD}\src"  # Windows PowerShell
```

### Issue: Tests not discovered in VSCode

**Solution:**
1. Open Command Palette (`Ctrl+Shift+P`)
2. Run: "Python: Configure Tests"
3. Select: "pytest"
4. Select: "tests" directory
5. Reload window

### Issue: Formatter not working

**Solution:**
1. Verify Black is installed: `pip show black`
2. Install if missing: `pip install black`
3. Open Command Palette
4. Run: "Format Document"
5. Select: "Black Formatter" as default

### Issue: Git shows unexpected changes

**Solution:**
```bash
# View what changed
git status
git diff

# Discard changes to specific file
git checkout -- filename

# Discard all local changes
git reset --hard HEAD
```

### Issue: Permission denied on scripts

**macOS/Linux:**
```bash
chmod +x scripts/*.py
```

### Issue: Import completions not working

**Solution:**
1. Check Pylance is installed
2. Verify settings in `.vscode/settings.json`:
   ```json
   "python.languageServer": "Pylance",
   "python.analysis.autoImportCompletions": true
   ```
3. Reload window

## Advanced Reset (Complete Rebuild)

For severe issues, perform a complete reset:

### 1. Backup Any Local Work

```bash
# Backup uncommitted changes
git diff > my-changes.patch

# Backup entire folder
cp -r /path/to/SynTechRev-PolyCodCal /path/to/backup
```

### 2. Delete and Reclone

```bash
# Delete local repository
cd ..
rm -rf SynTechRev-PolyCodCal

# Clone fresh from GitHub
git clone https://github.com/SynTechRev/SynTechRev-PolyCodCal.git
cd SynTechRev-PolyCodCal
```

### 3. Follow Quick Setup

Follow steps 3-7 from "Quick Reset" above.

### 4. Reapply Your Changes

```bash
# If you saved a patch
git apply my-changes.patch
```

## Verification Checklist

After reset, verify everything works:

- [ ] Virtual environment activates without errors
- [ ] `python --version` shows correct version (3.11+)
- [ ] `pytest -v` shows all 15 tests passing
- [ ] `black --check src tests scripts` shows no errors
- [ ] `ruff check .` shows no errors
- [ ] `mypy src` shows no errors
- [ ] VSCode shows correct Python interpreter in bottom-right
- [ ] VSCode Testing panel shows all 15 tests
- [ ] Auto-format on save works
- [ ] GitHub Copilot provides suggestions
- [ ] Import autocomplete works
- [ ] No git changes shown (unless you made intentional changes)

## Post-Reset Best Practices

### Keep Environment Clean

**Don't commit:**
- Virtual environment files (`.venv/`, `venv/`)
- Python cache (`__pycache__/`, `*.pyc`)
- Test cache (`.pytest_cache/`, `.coverage`)
- IDE-specific files (`.idea/`, user-specific VSCode files)

**Do commit:**
- Source code (`src/`, `tests/`, `scripts/`)
- Configuration (`.vscode/` workspace settings, `.pre-commit-config.yaml`)
- Documentation (`docs/`, `README.md`, etc.)
- Dependencies (`requirements.txt`, `dev-requirements.txt`)

### Regular Maintenance

**Weekly:**
```bash
# Update dependencies
pip install --upgrade pip
pip install --upgrade -r dev-requirements.txt

# Clean cache
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
```

**Before starting new work:**
```bash
git checkout main
git pull origin main
git checkout -b feature/my-new-feature
```

**After completing work:**
```bash
# Run all checks
black src tests scripts
ruff check .
mypy src
pytest -v

# Commit and push
git add .
git commit -m "feat: description of changes"
git push origin feature/my-new-feature
```

## Integration with PR #5

PR #5 introduced comprehensive documentation and VSCode configuration. After reset, you'll have:

- **Documentation**: Guides in `docs/`, `QUICKSTART.md`, `CONTRIBUTING.md`, etc.
- **VSCode Config**: Optimized settings in `.vscode/`
- **Quality Tools**: Pre-configured linters, formatters, type checkers
- **Testing**: Integrated pytest with coverage
- **Copilot**: Project-specific instructions

This reset ensures your local environment matches these configurations.

## Need Help?

If issues persist after following this guide:

1. **Check existing documentation:**
   - `QUICKSTART.md` - Basic setup
   - `CONTRIBUTING.md` - Development workflow
   - `docs/DEVELOPMENT_WORKFLOW.md` - Detailed processes
   - `.vscode/README.md` - VSCode-specific help

2. **Review recent changes:**
   - Check PR #5 for comprehensive setup details
   - Review commit messages for recent updates

3. **Get support:**
   - Open an issue on GitHub
   - Include error messages and steps tried
   - Mention you followed this reset guide

## Summary

This reset process ensures:
- Clean virtual environment matching project requirements
- VSCode properly configured for Python development
- All tests passing and quality checks working
- GitHub integration functioning correctly
- Cross-platform compatibility maintained
- GitHub Copilot providing project-specific assistance

Follow the **Quick Reset** for most issues. Use **Advanced Reset** only if problems persist after quick reset.

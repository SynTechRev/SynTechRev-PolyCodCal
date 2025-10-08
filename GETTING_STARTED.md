# Getting Started with SynTechRev-PolyCodCal

Welcome! This guide will help you set up your development environment and start contributing to SynTechRev-PolyCodCal in just a few minutes.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.11, 3.12, or 3.13**
- **Git**
- **VS Code** (recommended) or your preferred editor
- **GitHub Copilot** (optional but recommended for AI-assisted development)

## Quick Setup (5 Minutes)

### 1. Clone the Repository

```bash
git clone https://github.com/SynTechRev/SynTechRev-PolyCodCal.git
cd SynTechRev-PolyCodCal
```

### 2. Set Up Virtual Environment

**On Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**On macOS/Linux:**
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r dev-requirements.txt
```

**Note:** If you encounter `ModuleNotFoundError` during testing, the `src` directory is automatically added to `PYTHONPATH` in VS Code. For command-line testing, use:

```bash
PYTHONPATH=src pytest -v
```

### 4. Install Pre-commit Hooks

```bash
pre-commit install
```

### 5. Verify Setup

Run the test suite to ensure everything is working:

```bash
PYTHONPATH=src pytest -v
```

You should see:
```
================ 15 passed in 0.04s ================
```

✅ **You're ready to develop!**

## VS Code Setup (Recommended)

### Open in VS Code

```bash
code .
```

Or if you have the workspace file:

```bash
code SynTechRev-PolyCodCal.code-workspace
```

### Install Recommended Extensions

When VS Code opens, you'll see a notification about recommended extensions:

1. Click **"Install All"** to install:
   - Python
   - Pylance
   - Black Formatter
   - Ruff
   - Mypy
   - GitHub Copilot ✨
   - GitHub Copilot Chat ✨
   - Coverage Gutters
   - GitLens
   - And more...

2. Wait for all extensions to install

### Select Python Interpreter

1. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
2. Type **"Python: Select Interpreter"**
3. Choose the one that shows **`.venv`**

The PYTHONPATH is automatically configured to include the `src` directory, so imports will work correctly.

### Verify VS Code Setup

1. Open the **Testing** panel (flask icon in sidebar or `Ctrl+Shift+T`)
2. Click the **play button** to run all tests
3. See green checkmarks ✅

## GitHub Copilot Setup

If you have GitHub Copilot:

1. **Sign in**: Click the GitHub Copilot icon in the status bar and sign in
2. **Enable Copilot**: Ensure it's enabled for Python files (it's pre-configured in `.vscode/settings.json`)
3. **Start coding**: Copilot will provide intelligent suggestions as you type
4. **Use Copilot Chat**: Press `Ctrl+I` to open inline chat or use the chat panel for questions

For detailed Copilot workflows, see [COPILOT_INTEGRATION.md](COPILOT_INTEGRATION.md).

## Your First Contribution

### 1. Create a Branch

```bash
git checkout -b feature/my-first-contribution
```

### 2. Make a Small Change

Try editing `src/syntechrev_polycodcal/core.py` or add a new function.

### 3. Run Tests

**In VS Code:**
- Press `Ctrl+Shift+T` to run tests

**In Terminal:**
```bash
PYTHONPATH=src pytest -v
```

### 4. Format and Check Code Quality

**Run all checks:**
```bash
black src tests scripts
ruff check .
mypy src
```

**Or use VS Code shortcut:**
- Press `Ctrl+Shift+B` to run all quality checks

**Or run pre-commit:**
```bash
pre-commit run --all-files
```

### 5. Commit Your Changes

```bash
git add .
git commit -m "feat: describe your change"
```

### 6. Push and Create a Pull Request

```bash
git push -u origin feature/my-first-contribution
```

Then open a pull request on GitHub!

## Common Commands

### Testing
```bash
# Run all tests
PYTHONPATH=src pytest -v

# Run with coverage
PYTHONPATH=src pytest --cov=src/syntechrev_polycodcal --cov-report=term-missing

# Run specific test
PYTHONPATH=src pytest tests/test_feedback_monitor.py::test_no_alert_below_threshold -v
```

### Code Quality
```bash
# Format code
black src tests scripts

# Check linting
ruff check .

# Fix auto-fixable issues
ruff check . --fix

# Type checking
mypy src

# All pre-commit checks
pre-commit run --all-files
```

### VS Code Shortcuts
- `Ctrl+Shift+T` - Run tests
- `Ctrl+Shift+B` - Run quality checks
- `F5` - Debug current file
- `` Ctrl+` `` - Toggle terminal
- `Ctrl+Shift+P` - Command palette
- `Ctrl+I` - Copilot inline chat

## Project Structure

```
SynTechRev-PolyCodCal/
├── src/syntechrev_polycodcal/    # Source code (added to PYTHONPATH)
│   ├── __init__.py
│   ├── core.py
│   └── feedback_monitor.py       # Main monitoring module
├── tests/                         # Test files
│   ├── test_core.py
│   ├── test_feedback_monitor.py
│   └── test_feedback_monitor_extra.py
├── scripts/                       # Utility scripts
│   └── feedback_monitor.py       # CLI tool
├── examples/                      # Example data
│   └── events.jsonl
├── docs/                          # Documentation
│   ├── INDEX.md
│   └── DEVELOPMENT_WORKFLOW.md
├── .vscode/                       # VS Code configuration
│   ├── settings.json             # Includes PYTHONPATH setup
│   ├── extensions.json           # Recommended extensions
│   ├── launch.json               # Debug configurations
│   └── tasks.json                # Build tasks
├── GETTING_STARTED.md            # This file
├── COPILOT_INTEGRATION.md        # Copilot workflow guide
├── SOLUTION_SUMMARY.md           # Project architecture
├── CODE_REPAIR_STRATEGY.md       # Code quality guide
├── CONTRIBUTING.md                # Contribution guide
└── README.md                      # Main documentation
```

## Troubleshooting

### Tests Not Running?

**Problem:** `ModuleNotFoundError: No module named 'syntechrev_polycodcal'`

**Solution:**
- In VS Code: The settings.json already includes `python.analysis.extraPaths` and terminal `PYTHONPATH` configuration
- In Terminal: Use `PYTHONPATH=src pytest -v`
- Check that your Python interpreter is set to `.venv`
- Reload VS Code window (`Ctrl+Shift+P` → "Reload Window")

### Formatter Not Working?

**Problem:** Black doesn't format on save

**Solution:**
- Install Black: `pip install black`
- Check "Format on Save" is enabled in VS Code settings (it's pre-configured)
- Ensure the Black extension is installed
- Check the Python extension is active

### GitHub Copilot Not Working?

**Problem:** Copilot suggestions not appearing

**Solution:**
- Check you're signed in to GitHub in VS Code
- Verify Copilot extension is installed
- Check the Copilot status in the status bar (bottom right)
- Ensure Copilot is enabled for Python (pre-configured in settings.json)
- Try restarting VS Code

### Import Errors?

**Problem:** Pylance shows import errors

**Solution:**
- Ensure your Python interpreter is set to `.venv`
- The `src` directory is added to `python.analysis.extraPaths` in settings.json
- Reload VS Code window
- Check PYTHONPATH is set in the integrated terminal

## Next Steps

Now that you're set up, explore these resources:

- **[QUICKSTART.md](QUICKSTART.md)** - Alternative 5-minute guide
- **[README.md](README.md)** - Project overview and features
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Detailed contribution guidelines
- **[COPILOT_INTEGRATION.md](COPILOT_INTEGRATION.md)** - AI-assisted development workflow
- **[CODE_REPAIR_STRATEGY.md](CODE_REPAIR_STRATEGY.md)** - Code quality standards
- **[docs/DEVELOPMENT_WORKFLOW.md](docs/DEVELOPMENT_WORKFLOW.md)** - Detailed workflow guide
- **[.vscode/README.md](.vscode/README.md)** - VS Code configuration details

## Get Help

- **Documentation Issues**: Check [docs/INDEX.md](docs/INDEX.md) for all documentation
- **Build/Test Issues**: See troubleshooting section above
- **Questions**: Open a discussion on GitHub
- **Bugs**: Open an issue on GitHub
- **Copilot Help**: See [COPILOT_INTEGRATION.md](COPILOT_INTEGRATION.md)

---

**Happy coding! 🚀**

Remember: With GitHub Copilot, you have an AI pair programmer to help you every step of the way. Use it to learn, explore, and build faster!

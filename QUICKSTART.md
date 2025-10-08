# Quick Start Guide

Get started with SynTechRev-PolyCodCal development in 5 minutes!

## Prerequisites

- Python 3.11, 3.12, or 3.13
- Git
- VS Code (recommended) or your preferred editor

## Setup (5 minutes)

### 1. Clone and Navigate

```bash
git clone https://github.com/SynTechRev/SynTechRev-PolyCodCal.git
cd SynTechRev-PolyCodCal
```

### 2. Create Virtual Environment

**Windows:**
```powershell
python -m venv .venv
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r dev-requirements.txt
pip install -e .
```

### 4. Install Pre-commit Hooks

```bash
pre-commit install
```

### 5. Verify Installation

```bash
pytest -v
```

You should see:
```
================ 15 passed in 0.04s ================
```

✅ **You're ready to develop!**

## Using VS Code

### Open in VS Code

```bash
code .
```

### Install Recommended Extensions

1. When VS Code opens, you'll see a notification about recommended extensions
2. Click "Install All"
3. Wait for extensions to install

### Select Python Interpreter

1. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
2. Type "Python: Select Interpreter"
3. Choose the one that shows `.venv`

### Run Your First Test

1. Open the Testing panel (flask icon in sidebar)
2. Click the play button to run all tests
3. See green checkmarks ✅

## Try It Out

### Run the Example Script

```bash
python scripts/feedback_monitor.py examples/events.jsonl
```

### Use the Library

Create `test_script.py`:

```python
from syntechrev_polycodcal.feedback_monitor import FeedbackMonitor

# Create monitor
mon = FeedbackMonitor(window_seconds=60, threshold=0.3)

# Add some events
mon.ingest({"timestamp": None, "outcome": "ok"})
mon.ingest({"timestamp": None, "outcome": "error"})
mon.ingest({"timestamp": None, "outcome": "error"})

# Check for alerts
alert = mon.check()
if alert:
    print(f"Alert! Negative rate: {alert.metric_value:.2%}")
else:
    print("No alerts")
```

Run it:
```bash
python test_script.py
```

## Make Your First Change

### 1. Create a Branch

```bash
git checkout -b feature/my-first-change
```

### 2. Edit Code

Open `src/syntechrev_polycodcal/core.py` and make a small change

### 3. Run Tests

```bash
pytest -v
```

### 4. Format and Check

```bash
black src tests scripts
ruff check .
```

Or in VS Code: `Ctrl+Shift+B` (Run all quality checks)

### 5. Commit

```bash
git add .
git commit -m "feat: describe your change"
```

### 6. Push

```bash
git push -u origin feature/my-first-change
```

## Common Commands

### Testing
```bash
# Run all tests
pytest -v

# Run with coverage
pytest --cov=src/syntechrev_polycodcal --cov-report=term-missing

# Run specific test
pytest tests/test_feedback_monitor.py::test_no_alert_below_threshold -v
```

### Code Quality
```bash
# Format code
black src tests scripts

# Check linting
ruff check .

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

## Project Structure

```
SynTechRev-PolyCodCal/
├── src/syntechrev_polycodcal/    # Source code
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
│   └── DEVELOPMENT_WORKFLOW.md
├── .vscode/                       # VS Code settings
├── CODE_REPAIR_STRATEGY.md       # Code quality guide
├── CONTRIBUTING.md                # Contribution guide
└── README.md                      # Main documentation
```

## Next Steps

### Learn the Codebase
1. Read [README.md](README.md) for project overview
2. Explore `src/syntechrev_polycodcal/feedback_monitor.py`
3. Review tests in `tests/` directory

### Understand the Workflow
1. Read [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines
2. Check [docs/DEVELOPMENT_WORKFLOW.md](docs/DEVELOPMENT_WORKFLOW.md) for process diagrams
3. Review [CODE_REPAIR_STRATEGY.md](CODE_REPAIR_STRATEGY.md) for quality practices

### Start Contributing
1. Check open issues on GitHub
2. Look for "good first issue" labels
3. Ask questions in discussions
4. Submit your first PR!

## Need Help?

### Documentation
- **General**: [README.md](README.md)
- **Contributing**: [CONTRIBUTING.md](CONTRIBUTING.md)
- **Workflow**: [docs/DEVELOPMENT_WORKFLOW.md](docs/DEVELOPMENT_WORKFLOW.md)
- **VS Code**: [.vscode/README.md](.vscode/README.md)
- **Code Quality**: [CODE_REPAIR_STRATEGY.md](CODE_REPAIR_STRATEGY.md)

### Common Issues

**Tests not running?**
- Check Python interpreter is set to `.venv`
- Ensure pytest is installed: `pip install pytest`
- Reload VS Code window

**Formatter not working?**
- Install black: `pip install black`
- Check "Format on Save" is enabled in VS Code settings

**Import errors?**
- Ensure package is installed: `pip install -e .`
- Check PYTHONPATH includes `src` directory

### Get Support
- Open an issue on GitHub
- Ask in discussions
- Review existing documentation

## Summary

You now have:
- ✅ Working development environment
- ✅ All tests passing
- ✅ VS Code configured and ready
- ✅ Understanding of basic workflow
- ✅ Resources to learn more

**Happy coding!** 🎉

Ready to dive deeper? Check out:
- [CONTRIBUTING.md](CONTRIBUTING.md) - Detailed contribution guide
- [docs/DEVELOPMENT_WORKFLOW.md](docs/DEVELOPMENT_WORKFLOW.md) - Complete workflow
- [CODE_REPAIR_STRATEGY.md](CODE_REPAIR_STRATEGY.md) - Quality assurance

---

*Need more details? All commands and concepts are explained in depth in the full documentation.*

# SynTechRev-PolyCodCal

![CI](https://github.com/SynTechRev/SynTechRev-PolyCodCal/actions/workflows/ci.yml/badge.svg)
[![codecov](https://codecov.io/gh/SynTechRev/SynTechRev-PolyCodCal/branch/main/graph/badge.svg)](https://codecov.io/gh/SynTechRev/SynTechRev-PolyCodCal)

Polymathic CodCal - A feedback monitoring system with sliding-window aggregation and alerting.

## 🚀 Quick Start

**New to the project?** See [QUICKSTART.md](QUICKSTART.md) for a 5-minute setup guide!

### Quick Setup

Set up the workspace virtual environment (we use `.venv`):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r dev-requirements.txt
```

Run tests:

```powershell
pytest -q
```

Run pre-commit hooks locally:

```powershell
.venv\Scripts\pre-commit run --all-files
```

## FeedbackMonitor usage

The repository includes a small `FeedbackMonitor` utility in `src/syntechrev_polycodcal/feedback_monitor.py`.

Example (programmatic):

```python
from syntechrev_polycodcal.feedback_monitor import FeedbackMonitor

mon = FeedbackMonitor(window_seconds=60, threshold=0.2)
mon.ingest({"timestamp": None, "outcome": "ok"})
alert = mon.check()
if alert:
	print("Alert:", alert)
```

CLI example (one-off processing of newline-delimited JSON):

```powershell
python scripts\feedback_monitor.py examples\events.jsonl
```

## Development

### Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines on:
- Setting up your development environment
- Code standards and style guide
- Testing requirements
- Pull request process

### Code Quality

This project maintains high code quality standards:

- **Testing**: 100% code coverage with pytest
- **Linting**: Enforced with ruff and black
- **Type Checking**: Static analysis with mypy
- **CI/CD**: Automated testing on Python 3.11, 3.12, and 3.13

### Development Workflow

1. Clone the repository
2. Create a virtual environment
3. Install dependencies: `pip install -r dev-requirements.txt`
4. Install pre-commit hooks: `pre-commit install`
5. Make your changes
6. Run tests: `pytest -v`
7. Check code quality:
   ```bash
   black src tests scripts
   ruff check .
   mypy src
   ```
8. Submit a pull request

### Code Repair Strategy

For detailed information on our systematic approach to maintaining and repairing code quality, see [CODE_REPAIR_STRATEGY.md](CODE_REPAIR_STRATEGY.md). This document covers:
- Assessment and issue identification
- Prioritization methodology
- Systematic repair process
- Verification and testing
- Best practices and common solutions

## Project Structure

```
SynTechRev-PolyCodCal/
├── src/
│   └── syntechrev_polycodcal/
│       ├── __init__.py
│       ├── core.py
│       └── feedback_monitor.py
├── tests/
│   ├── test_core.py
│   ├── test_feedback_monitor.py
│   └── test_feedback_monitor_extra.py
├── scripts/
│   └── feedback_monitor.py
├── examples/
│   └── events.jsonl
├── .github/
│   └── workflows/
│       └── ci.yml
├── CODE_REPAIR_STRATEGY.md
├── CONTRIBUTING.md
└── README.md
```

## VS Code & GitHub Copilot Integration

This project includes comprehensive VS Code and GitHub Copilot integration:

**🤖 AI-Assisted Development**: GitHub Copilot integration with project-specific instructions
- Open `SynTechRev-PolyCodCal.code-workspace` for optimal setup
- Copilot understands project standards (100% coverage, type hints, Black formatting)
- Real-time type checking with Pylance (no mypy CLI required)

See [COPILOT_INTEGRATION.md](COPILOT_INTEGRATION.md) for complete setup and usage guide.

**⚙️ Pre-configured VS Code Settings**:
- Auto-format on save (Black)
- Integrated testing (pytest)
- Type checking (Pylance)
- One-click quality checks (`Ctrl+Shift+B`)

See [.vscode/README.md](.vscode/README.md) for VS Code configuration details.

## Resources

- [Copilot Integration Guide](COPILOT_INTEGRATION.md) - GitHub Copilot setup and usage
- [VS Code Setup](.vscode/README.md) - Editor configuration and shortcuts
- [Contributing Guide](CONTRIBUTING.md) - How to contribute to this project
- [Code Repair Strategy](CODE_REPAIR_STRATEGY.md) - Systematic approach to code quality
- [CI/CD Pipeline](.github/workflows/ci.yml) - Automated testing and quality checks

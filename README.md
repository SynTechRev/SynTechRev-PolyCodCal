# SynTechRev-PolyCodCal

![CI](https://github.com/SynTechRev/SynTechRev-PolyCodCal/actions/workflows/ci.yml/badge.svg)
[![codecov](https://codecov.io/gh/SynTechRev/SynTechRev-PolyCodCal/branch/main/graph/badge.svg)](https://codecov.io/gh/SynTechRev/SynTechRev-PolyCodCal)

Polymathic CodCal - A feedback monitoring system with sliding-window aggregation and alerting.

## 🚀 Quick Start

> **⚠️ Having VS Code sync issues?** See [Environment Reset Guide](docs/ENVIRONMENT_RESET.md) for restoring a clean local state aligned with `main`.

**New to the project?** Start here:
- **[GETTING_STARTED.md](GETTING_STARTED.md)** - Complete setup guide with VS Code & Copilot integration
- **[QUICKSTART.md](QUICKSTART.md)** - Alternative 5-minute setup guide

### Quick Setup

Set up the workspace virtual environment (we use `.venv`):

```bash
python -m venv .venv

# On Windows
.venv\Scripts\Activate.ps1

# On macOS/Linux
source .venv/bin/activate

pip install -r dev-requirements.txt
```

Run tests:

```bash
# The src directory is automatically added to PYTHONPATH in VS Code
# For command-line testing:
PYTHONPATH=src pytest -v
```

Run pre-commit hooks locally:

```bash
pre-commit run --all-files
```

### VS Code Setup (Recommended)

This project is fully configured for VS Code with GitHub Copilot:

1. **Open in VS Code**: `code .` or `code SynTechRev-PolyCodCal.code-workspace`
2. **Install Extensions**: Click "Install All" when prompted
3. **Select Interpreter**: Choose `.venv` interpreter
4. **Start Coding**: PYTHONPATH is automatically configured!

See [GETTING_STARTED.md](GETTING_STARTED.md) for detailed instructions.

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

## Phase 4: Legal Data Integration

The project now includes a structured legal data schema and ingestion pipeline for landmark U.S. Supreme Court cases.

### Features

- **Pydantic Schema Validation**: `LegalRecord` model ensures data integrity
- **Data Loader**: Simple function to load and validate JSON case files
- **Sample Dataset**: 10 landmark Supreme Court cases (1803-2013)
- **Full Test Coverage**: Comprehensive test suite for schema and loader

### Usage

```python
from syntechrev_polycodcal.data_loader import load_legal_records

# Load all case records from data/cases directory
records = load_legal_records("data/cases")

# Access case data
for record in records:
    print(f"{record.case_name} ({record.year})")
    print(f"  Doctrine: {record.doctrine}")
    print(f"  Holding: {record.holding}")
```

### Data Structure

Each legal record includes:
- Case name, year, and citation
- Court and jurisdiction
- Legal doctrine (Civil Rights, Constitutional Law, etc.)
- Case summary, holding, and significance
- Optional keywords for categorization

Data is organized in `/data/` directory and validated via Pydantic models. This foundation can be extended for AI-driven legal text generation in Phase 5.

See [docs/LEGAL_DATA_GENERATOR_OVERVIEW.md](docs/LEGAL_DATA_GENERATOR_OVERVIEW.md) for detailed documentation.

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

### Environment Reset

Having issues with your development environment or VSCode integration? See [docs/ENVIRONMENT_RESET.md](docs/ENVIRONMENT_RESET.md) for:
- Quick environment reset procedures
- VSCode integration troubleshooting
- Cross-platform compatibility fixes
- GitHub sync and merge conflict resolution
- GitHub Copilot setup verification

### Agent Collaboration

Working with multiple AI agents or coordinating automated tasks? See [docs/AGENT_COLLABORATION.md](docs/AGENT_COLLABORATION.md) for:
- Cross-platform communication protocols
- Task coordination between agents
- Quality standards and handoff procedures
- GitHub Copilot integration patterns
- Conflict resolution strategies

## Project Structure

```
SynTechRev-PolyCodCal/
├── src/
│   └── syntechrev_polycodcal/
│       ├── __init__.py
│       ├── core.py
│       ├── feedback_monitor.py
│       ├── data_loader.py
│       └── schemas/
│           ├── __init__.py
│           └── legal_record.py
├── tests/
│   ├── test_core.py
│   ├── test_feedback_monitor.py
│   ├── test_feedback_monitor_extra.py
│   └── test_data_loader.py
├── data/
│   └── cases/
│       └── *.json (10 landmark Supreme Court cases)
├── scripts/
│   └── feedback_monitor.py
├── examples/
│   └── events.jsonl
├── docs/
│   └── LEGAL_DATA_GENERATOR_OVERVIEW.md
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

## Roadmap
See the evolving project roadmap in [ROADMAP.md](ROADMAP.md) for phased enhancements (hysteresis thresholds, batched ingest, metrics extensibility, CLI tooling, and more).

# Contributing to SynTechRev-PolyCodCal

Thank you for your interest in contributing to SynTechRev-PolyCodCal! This guide will help you get started with development and ensure your contributions meet our quality standards.

## Table of Contents

- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Code Standards](#code-standards)
- [Testing Requirements](#testing-requirements)
- [Submitting Changes](#submitting-changes)
- [Code Review Process](#code-review-process)

## Getting Started

### Prerequisites

- Python 3.11, 3.12, or 3.13
- Git
- Virtual environment tool (venv, virtualenv, or conda)

### Initial Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/SynTechRev/SynTechRev-PolyCodCal.git
   cd SynTechRev-PolyCodCal
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   
   # On Windows
   .venv\Scripts\activate
   
   # On Unix or MacOS
   source .venv/bin/activate
   ```

3. **Install development dependencies**
   ```bash
   pip install -r dev-requirements.txt
   pip install -e .
   ```

4. **Install pre-commit hooks**
   ```bash
   pre-commit install
   ```

5. **Verify setup**
   ```bash
   pytest -v
   ```
   You should see all tests passing.

## Development Workflow

### 1. Create a Feature Branch

Always work on a feature branch, never directly on `main`:

```bash
git checkout -b feature/your-feature-name
```

Use descriptive branch names:
- `feature/add-email-notifications`
- `bugfix/fix-timestamp-parsing`
- `docs/update-api-documentation`

### 2. Make Your Changes

Follow these principles:
- **Make small, focused commits** - each commit should represent one logical change
- **Write clear commit messages** - follow [Conventional Commits](https://www.conventionalcommits.org/)
- **Test as you go** - run tests frequently to catch issues early

### 3. Run Quality Checks

Before committing, ensure your code meets quality standards:

```bash
# Format code
black src tests scripts

# Run linter
ruff check .

# Type checking
mypy src

# Run tests
pytest -v

# Check coverage
pytest --cov=src/syntechrev_polycodcal --cov-report=term-missing

# Run all pre-commit hooks
pre-commit run --all-files
```

### 4. Commit Your Changes

```bash
git add .
git commit -m "feat: add new feature description"
```

Commit message format:
```
<type>: <short summary>

<optional detailed description>

<optional footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Adding or updating tests
- `refactor`: Code refactoring
- `style`: Formatting changes
- `chore`: Maintenance tasks

### 5. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub with:
- Clear title describing the change
- Description following the PR template
- Link to related issues (if any)

## Code Standards

### Python Style Guide

We follow PEP 8 with some modifications:

- **Line length**: 88 characters (Black default)
- **Indentation**: 4 spaces
- **Quotes**: Double quotes for strings
- **Imports**: Organized and sorted
  ```python
  # Standard library
  from collections import Counter
  from datetime import datetime
  
  # Third-party
  import pytest
  
  # Local
  from syntechrev_polycodcal.feedback_monitor import FeedbackMonitor
  ```

### Type Hints

Always include type hints for function signatures:

```python
from typing import Optional, Dict, List

def process_events(
    events: List[Dict],
    threshold: float = 0.2
) -> Optional[Alert]:
    """Process events and return alert if threshold exceeded.
    
    Args:
        events: List of event dictionaries
        threshold: Alert threshold (0.0 to 1.0)
        
    Returns:
        Alert object if threshold exceeded, None otherwise
    """
    pass
```

### Documentation

1. **Module docstrings** at the top of each file
2. **Function docstrings** for all public functions
3. **Class docstrings** for all classes
4. **Inline comments** for complex logic

Format:
```python
def function_name(param: Type) -> ReturnType:
    """Short one-line description.
    
    Longer description if needed. Explain what the function does,
    any important details, and edge cases.
    
    Args:
        param: Description of parameter
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When input is invalid
    """
    pass
```

## Testing Requirements

### Writing Tests

1. **Location**: Tests go in the `tests/` directory
2. **Naming**: Test files must start with `test_`
3. **Structure**: Test functions must start with `test_`

Example:
```python
def test_monitor_detects_negative_spike():
    """Test that FeedbackMonitor detects negative feedback spikes."""
    mon = FeedbackMonitor(window_seconds=60, threshold=0.5)
    
    # Add events that should trigger alert
    for _ in range(6):
        mon.ingest({"timestamp": None, "outcome": "error"})
    for _ in range(4):
        mon.ingest({"timestamp": None, "outcome": "ok"})
    
    alert = mon.check()
    assert alert is not None
    assert alert.metric_value >= 0.5
```

### Test Coverage

- **Minimum coverage**: 90% (aim for 100%)
- **Test all code paths**: success, failure, edge cases
- **Test error handling**: exceptions, invalid inputs
- **Test boundary conditions**: empty inputs, maximum values

Check coverage:
```bash
pytest --cov=src/syntechrev_polycodcal --cov-report=html
# Open htmlcov/index.html to see detailed coverage report
```

### Running Tests

```bash
# Run all tests
pytest -v

# Run specific test file
pytest tests/test_feedback_monitor.py -v

# Run specific test function
pytest tests/test_feedback_monitor.py::test_no_alert_below_threshold -v

# Run with coverage
pytest --cov=src/syntechrev_polycodcal --cov-report=term-missing

# Run with verbose output
pytest -vv

# Stop on first failure
pytest -x
```

## Submitting Changes

### Pull Request Checklist

Before submitting your PR, ensure:

- [ ] All tests pass locally
- [ ] Code coverage meets or exceeds target (90%+)
- [ ] All linting checks pass (ruff, black)
- [ ] Type checking passes (mypy)
- [ ] Pre-commit hooks pass
- [ ] Documentation is updated (if applicable)
- [ ] Commit messages follow conventional commits
- [ ] PR description is complete and clear
- [ ] Related issues are linked

### Pull Request Template

When creating a PR, fill out the template:

```markdown
## Summary
Brief description of what this PR does and why.

## Changes
- Specific change 1
- Specific change 2
- ...

## Verification
How you tested these changes:
- [ ] Unit tests added/updated
- [ ] Manual testing performed
- [ ] CI pipeline passes

## Checklist
- [ ] Tests added / updated
- [ ] Documentation updated
- [ ] CI passes
```

## Code Review Process

### What Reviewers Look For

1. **Correctness**: Does the code do what it's supposed to?
2. **Tests**: Are there adequate tests?
3. **Clarity**: Is the code easy to understand?
4. **Consistency**: Does it follow project conventions?
5. **Performance**: Are there any obvious inefficiencies?
6. **Security**: Are there any security concerns?

### Responding to Reviews

- Be open to feedback and suggestions
- Ask questions if something is unclear
- Make requested changes promptly
- Push additional commits to the same branch
- Re-request review when ready

### Approval and Merge

- PRs require at least one approval
- All CI checks must pass
- Merge conflicts must be resolved
- Squash commits or merge as appropriate

## Tips for Success

### For New Contributors

1. **Start small** - begin with documentation or simple bug fixes
2. **Ask questions** - use issues or discussions for clarification
3. **Read existing code** - understand the project structure first
4. **Follow examples** - look at recent PRs for guidance

### For All Contributors

1. **Run tests frequently** - catch issues early
2. **Keep PRs focused** - one feature or fix per PR
3. **Write good commit messages** - they help reviewers understand changes
4. **Be responsive** - address review feedback promptly
5. **Update your branch** - rebase or merge from main regularly

### Common Mistakes to Avoid

❌ Don't commit directly to main  
❌ Don't include unrelated changes in one PR  
❌ Don't skip tests  
❌ Don't ignore linting errors  
❌ Don't leave commented-out code  
❌ Don't commit sensitive data or credentials  

## Development Tools

### Recommended IDE Setup

**VS Code**:
- Python extension
- Pylance for type checking
- Black formatter extension
- GitLens for git integration

Settings (`.vscode/settings.json`):
```json
{
  "python.linting.enabled": true,
  "python.linting.ruffEnabled": true,
  "python.formatting.provider": "black",
  "editor.formatOnSave": true,
  "python.testing.pytestEnabled": true
}
```

**PyCharm**:
- Configure Black as external tool
- Enable pytest as test runner
- Set up mypy integration
- Use Git integration

### Debugging

1. **Use pytest fixtures** for test setup
2. **Add print statements** or use debugger
3. **Run single tests** to isolate issues
4. **Check test output** for detailed error messages

```bash
# Run with print output
pytest -s tests/test_feedback_monitor.py::test_specific_test

# Use Python debugger
pytest --pdb tests/test_feedback_monitor.py::test_specific_test
```

## Getting Help

### Resources

- **Documentation**: See [README.md](README.md)
- **Code Repair Guide**: See [CODE_REPAIR_STRATEGY.md](CODE_REPAIR_STRATEGY.md)
- **Issues**: Search existing issues or create new ones
- **Discussions**: Use GitHub Discussions for questions

### Contact

- Open an issue for bugs or feature requests
- Use discussions for general questions
- Tag maintainers for urgent issues

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

---

Thank you for contributing to SynTechRev-PolyCodCal! 🎉

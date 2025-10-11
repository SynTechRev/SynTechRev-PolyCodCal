# GitHub Copilot Instructions for SynTechRev-PolyCodCal

## Project Overview

This is a Python project for building a Codical Calculus and Lattice Environment (PolyCodCal). The project maintains 100% test coverage and follows strict code quality standards.

## Code Standards

### Python Style
- **Python Version**: 3.11, 3.12, or 3.13
- **Line Length**: 88 characters (Black default)
- **Formatter**: Black
- **Linter**: Ruff
- **Type Checker**: Pylance (mypy configuration exists but CLI not required)
- **Testing**: pytest with 100% coverage requirement

### Import Organization
```python
# Standard library imports
from collections import Counter
from datetime import datetime

# Third-party imports
import pytest

# Local imports
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
    """Process events and return alert if threshold exceeded."""
    pass
```

## Project Structure

```
src/syntechrev_polycodcal/
├── __init__.py           # Package exports
├── core.py               # Core utilities (simple greeting function)
└── feedback_monitor.py   # Feedback monitoring with sliding window

tests/
├── test_core.py                    # Core module tests
├── test_feedback_monitor.py        # Basic FeedbackMonitor tests
└── test_feedback_monitor_extra.py  # Additional FeedbackMonitor tests
```

## Key Components

### FeedbackMonitor Class
- **Purpose**: Monitor feedback events and emit alerts when thresholds are hit
- **Window**: Sliding time window (default 60 seconds)
- **Threshold**: Negative feedback ratio (default 0.2)
- **Methods**:
  - `ingest(event: Dict)` - Add event to buffer
  - `check() -> Optional[Alert]` - Check if threshold exceeded
  - `summarize() -> Dict` - Get aggregated metrics

### Core Module
- Simple utility functions
- `greet(name: Optional[str]) -> str` - Returns greeting message

## Testing Requirements

- **Minimum Coverage**: 100% (strictly enforced)
- **Test Framework**: pytest
- **Test all code paths**: success, failure, edge cases
- **Test error handling**: exceptions, invalid inputs
- **Test boundary conditions**: empty inputs, maximum values

### Running Tests
```bash
# All tests
pytest -v

# With coverage
pytest --cov=src/syntechrev_polycodcal --cov-report=term-missing

# Specific test
pytest tests/test_feedback_monitor.py::test_no_alert_below_threshold -v
```

## Code Quality Commands

```bash
# Format code (always run before committing)
black src tests scripts

# Lint code
ruff check .

# Run all quality checks
# In VS Code: Ctrl+Shift+B (runs "Quality Checks (All)" task)
```

## When Suggesting Code

1. **Always include type hints** - This project uses strict typing
2. **Include docstrings** - Use Google style docstrings with Args, Returns, Raises
3. **Handle edge cases** - Check for None, empty collections, zero divisions
4. **Add tests** - Any new function needs corresponding tests with 100% coverage
5. **Follow Black formatting** - Code will be auto-formatted, but suggest properly formatted code
6. **Use descriptive variable names** - Prefer clarity over brevity

## Common Patterns

### Adding a New Function to FeedbackMonitor
```python
def new_method(self, param: SomeType) -> ReturnType:
    """Short description.
    
    Args:
        param: Description of parameter.
        
    Returns:
        Description of return value.
        
    Raises:
        ValueError: When parameter is invalid.
    """
    if not param:
        raise ValueError("param cannot be None or empty")
    
    # Implementation
    return result
```

### Writing Tests
```python
def test_descriptive_name():
    """Test that method handles specific scenario."""
    # Arrange
    monitor = FeedbackMonitor(window_seconds=60, threshold=0.2)
    
    # Act
    result = monitor.some_method()
    
    # Assert
    assert result is not None
    assert result.field == expected_value
```

## Error Prevention

### Common Issues to Avoid
1. **Missing outcome field**: Events must have 'outcome' key
2. **Type mismatches**: Use proper type hints and check types
3. **Division by zero**: Always check if total > 0 before dividing
4. **Timestamp handling**: Use `_to_ts()` helper to normalize timestamps
5. **Buffer expiration**: Always call `_expire_old()` after adding events

## VS Code Integration

This project has pre-configured VS Code settings:
- **Format on save** enabled with Black
- **Pylance** for type checking (basic mode)
- **pytest** for test discovery
- **Debug configurations** for current file and tests
- **Tasks** for common operations (Ctrl+Shift+B)

## Documentation Requirements

When adding new features:
1. Update docstrings in code
2. Add examples to documentation
3. Update CHANGELOG.md
4. Add tests that demonstrate usage
5. Update README.md if public API changes

## Commit Message Format

```
<type>: <short summary>

<optional detailed description>
```

Types: `feat`, `fix`, `docs`, `test`, `refactor`, `style`, `chore`

## Review Checklist

Before suggesting code is ready:
- [ ] Type hints on all functions
- [ ] Docstrings with Args/Returns/Raises
- [ ] Tests written with 100% coverage
- [ ] Edge cases handled
- [ ] Error messages are descriptive
- [ ] Code follows Black formatting
- [ ] No linting errors
- [ ] All tests pass

## Special Notes

- **No mypy CLI**: Pylance handles type checking in editor
- **Workspace settings**: Use `.vscode/settings.json` for project config
- **Virtual environment**: Code expects `.venv` directory for dependencies
- **Import paths**: Use `src/` in PYTHONPATH for imports

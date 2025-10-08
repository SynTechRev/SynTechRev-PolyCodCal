# GitHub Copilot Instructions for SynTechRev-PolyCodCal

This file provides context to GitHub Copilot for better code suggestions in this project.

## Project Overview

SynTechRev-PolyCodCal is a feedback monitoring system with sliding-window aggregation and alerting capabilities. The core component is `FeedbackMonitor`, which tracks event outcomes over time and triggers alerts when failure rates exceed thresholds.

## Architecture

- **Core Module** (`src/syntechrev_polycodcal/core.py`): Basic utilities and helpers
- **FeedbackMonitor** (`src/syntechrev_polycodcal/feedback_monitor.py`): Main monitoring logic
- **Tests** (`tests/`): Comprehensive test suite with 100% coverage
- **Scripts** (`scripts/`): CLI tools and utilities

## Code Style

### Python Version
- Target: Python 3.11, 3.12, 3.13
- Use modern Python features (type hints, dataclasses, f-strings)

### Formatting
- **Black** formatter with 88-character line length
- Format on save is enabled
- Follow PEP 8 with Black's modifications

### Type Hints
Always include comprehensive type hints:

```python
from typing import Dict, List, Optional, Deque
from datetime import datetime

def process_events(
    events: List[Dict],
    threshold: float = 0.2,
    window_size: int = 100
) -> Optional[Alert]:
    """Process events and return alert if threshold exceeded."""
    pass
```

### Imports
Organize imports in this order:
1. Future imports (`from __future__ import annotations`)
2. Standard library
3. Third-party packages
4. Local modules

Example:
```python
from __future__ import annotations

from collections import Counter, deque
from datetime import datetime, timezone
from typing import Dict, List, Optional

from syntechrev_polycodcal.core import greet
```

### Docstrings
Use Google-style docstrings:

```python
def calculate_failure_rate(events: List[Dict], window_size: int) -> float:
    """Calculate the failure rate over a sliding window of events.
    
    Args:
        events: List of event dictionaries with 'outcome' field
        window_size: Number of recent events to consider
        
    Returns:
        Failure rate as a float between 0.0 and 1.0
        
    Raises:
        ValueError: If window_size is less than 1
        
    Example:
        >>> events = [{"outcome": "success"}, {"outcome": "failure"}]
        >>> calculate_failure_rate(events, 2)
        0.5
    """
    pass
```

## Testing

### Test Framework
- **pytest** for all tests
- Tests located in `tests/` directory
- 100% code coverage target

### Test Naming
- Test files: `test_<module>.py`
- Test functions: `test_<feature>_<scenario>`

Example:
```python
def test_feedback_monitor_alerts_on_high_failure_rate():
    """Test that FeedbackMonitor triggers alert when failure rate exceeds threshold."""
    pass
```

### Test Structure
Follow Arrange-Act-Assert pattern:

```python
def test_window_size_limits_event_count():
    """Test that window size correctly limits the number of tracked events."""
    # Arrange
    monitor = FeedbackMonitor(window_size=5, failure_threshold=0.2)
    
    # Act
    for i in range(10):
        monitor.ingest({"timestamp": datetime.now(timezone.utc), "outcome": "success"})
    
    # Assert
    assert len(monitor.events) == 5
```

### Running Tests
- In terminal: `PYTHONPATH=src pytest -v`
- In VS Code: Use Testing panel or `Ctrl+Shift+T`
- With coverage: `PYTHONPATH=src pytest --cov=src/syntechrev_polycodcal --cov-report=term-missing`

## Common Patterns

### FeedbackMonitor Usage

```python
from datetime import datetime, timezone
from syntechrev_polycodcal.feedback_monitor import FeedbackMonitor

# Create monitor
monitor = FeedbackMonitor(
    window_size=100,
    failure_threshold=0.2
)

# Ingest events
event = {
    "timestamp": datetime.now(timezone.utc),
    "outcome": "success"  # or "failure"
}
monitor.ingest(event)

# Check for alerts
alert = monitor.check()
if alert:
    print(f"Alert! {alert.message}")
```

### Event Structure

Events must have:
- `timestamp`: datetime object (timezone-aware preferred)
- `outcome`: string, either "success" or "failure"

```python
{
    "timestamp": datetime(2024, 1, 15, 10, 30, 0, tzinfo=timezone.utc),
    "outcome": "failure"
}
```

### Alert Structure

```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Alert:
    message: str
    timestamp: datetime
    failure_rate: float
    threshold: float
```

## Code Quality Standards

### Linting
- **Ruff** for fast linting
- Fix auto-fixable issues: `ruff check . --fix`
- All code must pass linting

### Type Checking
- **mypy** with strict settings
- Run: `mypy src`
- All code must pass type checking

### Pre-commit Hooks
- Black formatting
- Flake8 linting
- Run before commit: `pre-commit run --all-files`

## Error Handling

Be explicit about error cases:

```python
def process_events(events: List[Dict]) -> float:
    """Process events and return failure rate.
    
    Raises:
        ValueError: If events list is empty
        KeyError: If event is missing required field
    """
    if not events:
        raise ValueError("Events list cannot be empty")
    
    for event in events:
        if "outcome" not in event:
            raise KeyError("Event missing 'outcome' field")
    
    # Process...
```

## Documentation

### README Updates
When adding features, update:
- Feature list
- Usage examples
- API documentation

### Inline Comments
Use comments for:
- Complex algorithms
- Non-obvious decisions
- Temporary workarounds (with TODO/FIXME)

Don't comment obvious code:

```python
# Bad
x = x + 1  # Increment x

# Good
# Adjust for zero-based indexing
x = x + 1
```

## Performance Considerations

### FeedbackMonitor Efficiency
- Uses `deque` with `maxlen` for O(1) window management
- Maintains Counter for O(1) failure rate calculation
- Avoid iterating over all events in hot paths

### Memory Management
- Events are automatically removed when window is full
- No need for manual cleanup

## Git Conventions

### Branch Names
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring

### Commit Messages
Follow Conventional Commits:

```
feat: add percentile tracking to FeedbackMonitor
fix: correct threshold comparison in check()
docs: update README with new examples
test: add edge case tests for empty events
refactor: extract validation logic to separate method
```

## VS Code Integration

### PYTHONPATH
The `src` directory is automatically added to PYTHONPATH in VS Code settings. For command-line work, use:

```bash
PYTHONPATH=src pytest -v
PYTHONPATH=src python scripts/feedback_monitor.py
```

### Keyboard Shortcuts
- `Ctrl+Shift+T` - Run tests
- `Ctrl+Shift+B` - Run quality checks
- `F5` - Debug
- `Ctrl+I` - Copilot inline chat

## Common Tasks

### Adding a New Feature

1. **Plan**: Describe the feature in comments
2. **Implement**: Write the code with type hints
3. **Test**: Write comprehensive tests
4. **Document**: Update docstrings and README
5. **Validate**: Run tests, linting, type checking
6. **Commit**: Use conventional commit message

### Debugging

1. **Write failing test**: Reproduce the bug
2. **Use debugger**: F5 in VS Code or `pytest --pdb`
3. **Fix**: Make minimal changes
4. **Verify**: Ensure test passes
5. **Check coverage**: No regressions

### Refactoring

1. **Ensure tests pass**: Green baseline
2. **Make changes**: One refactor at a time
3. **Run tests**: Should still pass
4. **Check quality**: Linting, type checking
5. **Commit**: Clear refactoring message

## Anti-Patterns to Avoid

❌ **Don't:**
- Remove existing tests
- Change working code unnecessarily
- Skip type hints
- Ignore linting errors
- Commit commented-out code
- Use mutable default arguments
- Catch bare `Exception` without re-raising

✅ **Do:**
- Write tests for new features
- Make minimal, focused changes
- Use type hints everywhere
- Fix linting errors
- Remove dead code completely
- Use immutable defaults or None
- Catch specific exceptions

## Resources

- [CODE_REPAIR_STRATEGY.md](../CODE_REPAIR_STRATEGY.md) - Quality guidelines
- [CONTRIBUTING.md](../CONTRIBUTING.md) - Contribution process
- [DEVELOPMENT_WORKFLOW.md](../docs/DEVELOPMENT_WORKFLOW.md) - Development process
- [COPILOT_INTEGRATION.md](../COPILOT_INTEGRATION.md) - Copilot usage guide

## Questions?

When generating code suggestions:
1. Follow the patterns in existing code
2. Prioritize readability over cleverness
3. Include comprehensive type hints
4. Add tests for new functionality
5. Update documentation as needed

---

These instructions help you, Copilot, provide better suggestions for this project. Follow these guidelines to maintain code quality and consistency!

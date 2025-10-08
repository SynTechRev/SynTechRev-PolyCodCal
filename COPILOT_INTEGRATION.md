# GitHub Copilot Integration Guide

This guide explains how to use GitHub Copilot effectively with SynTechRev-PolyCodCal for AI-assisted development.

## Overview

GitHub Copilot is an AI pair programmer that helps you write code faster and with fewer errors. This project is fully configured to work with Copilot, providing:

- ✅ Pre-configured Copilot settings in `.vscode/settings.json`
- ✅ Context-aware suggestions based on project structure
- ✅ Type-hint aware completions
- ✅ Test generation assistance
- ✅ Documentation generation support
- ✅ Code refactoring suggestions

## Setup

### Prerequisites

1. **GitHub Copilot Subscription**
   - Individual, Business, or Enterprise plan
   - Or free for verified students, teachers, and open source maintainers

2. **VS Code Extensions**
   - `github.copilot` - Core Copilot extension
   - `github.copilot-chat` - Copilot Chat interface

These extensions are already listed in `.vscode/extensions.json` and will be recommended when you open the project.

### Enabling Copilot

1. **Install Extensions**: Click "Install All" when prompted in VS Code
2. **Sign In**: Click the Copilot icon in the status bar and sign in with your GitHub account
3. **Verify**: Look for the Copilot icon in the status bar (should show as active)

Copilot is pre-configured in `.vscode/settings.json` to work with:
- Python files (enabled)
- Markdown files (enabled)
- YAML files (enabled)
- Plaintext (disabled by default)

## Using Copilot

### 1. Inline Suggestions (Ghost Text)

As you type, Copilot provides suggestions in gray text:

**Example: Writing a function**

```python
# Type this comment:
# Calculate the average of positive numbers in a list

# Copilot will suggest:
def average_positive(numbers: List[float]) -> float:
    """Calculate the average of positive numbers in a list."""
    positives = [n for n in numbers if n > 0]
    return sum(positives) / len(positives) if positives else 0.0
```

**Controls:**
- `Tab` - Accept suggestion
- `Esc` - Dismiss suggestion
- `Alt+]` - Next suggestion
- `Alt+[` - Previous suggestion

### 2. Copilot Chat (`Ctrl+I`)

Use inline chat for quick questions and code modifications:

**Example: Refactoring**

1. Select code
2. Press `Ctrl+I`
3. Type: "Add type hints and docstring"
4. Copilot generates the improved code
5. Accept or reject the changes

**Example: Explaining Code**

1. Select code
2. Press `Ctrl+I`
3. Type: "Explain this code"
4. Copilot provides a detailed explanation

### 3. Chat Panel

Open the chat panel for longer conversations:

**Use Cases:**
- Architecture discussions
- Debugging help
- Test strategy planning
- Code review assistance

**Example Session:**

```
You: How do I add a new feature to FeedbackMonitor that tracks response times?

Copilot: To add response time tracking to FeedbackMonitor, you'll need to:

1. Add a new field to store response times in the event data
2. Modify the ingest method to accept response time
3. Add aggregation logic for response time metrics
4. Update tests to cover the new functionality

Here's a suggested implementation:
[code example]
```

## Best Practices

### 1. Provide Context with Comments

**Good:**
```python
# Function to calculate moving average of failure rates over the last N events
def calculate_failure_rate(events: List[Dict], window_size: int) -> float:
```

Copilot will generate better suggestions when you provide clear intent.

**Bad:**
```python
def calc(e, w):
```

Vague names and no context result in poor suggestions.

### 2. Use Type Hints

The project uses comprehensive type hints, which help Copilot understand your intent:

```python
from typing import List, Dict, Optional, Deque
from datetime import datetime

def process_events(
    events: List[Dict],
    threshold: float = 0.2,
    window_size: int = 100
) -> Optional[Alert]:
    # Copilot now knows the types and can suggest accordingly
```

### 3. Write Tests with Copilot

**Pattern:**

1. Write the test name and docstring:
   ```python
   def test_feedback_monitor_alerts_on_high_failure_rate():
       """Test that FeedbackMonitor triggers alert when failure rate exceeds threshold."""
   ```

2. Copilot suggests the test implementation

3. Review and accept/modify

**Example:**

```python
def test_feedback_monitor_respects_window_size():
    """Test that FeedbackMonitor only considers events within window."""
    # Copilot will suggest:
    monitor = FeedbackMonitor(window_size=5, failure_threshold=0.5)
    
    # Add 3 failures
    for _ in range(3):
        monitor.ingest({"timestamp": datetime.now(timezone.utc), "outcome": "failure"})
    
    # Add 3 successes
    for _ in range(3):
        monitor.ingest({"timestamp": datetime.now(timezone.utc), "outcome": "success"})
    
    # Only last 5 events should be considered (3 success, 2 failure = 40% failure rate)
    alert = monitor.check()
    assert alert is None  # Below 50% threshold
```

### 4. Generate Documentation

**Pattern:**

1. Write the function signature
2. Type `"""` to start a docstring
3. Copilot suggests the full docstring

**Example:**

```python
def calculate_percentile(values: List[float], percentile: float) -> float:
    """
    # Copilot suggests:
    Calculate the specified percentile from a list of values.
    
    Args:
        values: List of numeric values
        percentile: Percentile to calculate (0.0 to 1.0)
        
    Returns:
        The value at the specified percentile
        
    Raises:
        ValueError: If percentile is not between 0.0 and 1.0
        ValueError: If values list is empty
        
    Example:
        >>> calculate_percentile([1, 2, 3, 4, 5], 0.5)
        3.0
    """
```

### 5. Code Review with Copilot

Use Copilot Chat to review code:

1. Select code block
2. Open chat
3. Ask: "Review this code for potential issues"
4. Copilot identifies:
   - Bugs
   - Performance issues
   - Style inconsistencies
   - Missing edge cases

## Project-Specific Workflows

### Adding a New Feature to FeedbackMonitor

1. **Plan with Copilot Chat:**
   ```
   You: I want to add percentile tracking to FeedbackMonitor. What's the best approach?
   
   Copilot: [Suggests architecture]
   ```

2. **Implement with inline suggestions:**
   - Add new fields
   - Update `ingest` method
   - Add calculation logic

3. **Generate tests:**
   - Write test names
   - Let Copilot suggest implementations
   - Review and adjust

4. **Update documentation:**
   - Add docstrings (Copilot helps)
   - Update README if needed

### Debugging with Copilot

1. **Describe the problem:**
   ```python
   # BUG: FeedbackMonitor is not triggering alerts even when failure rate exceeds threshold
   # The check() method returns None when it should return an Alert
   ```

2. **Copilot suggests potential fixes:**
   - Check threshold comparison logic
   - Verify window calculations
   - Inspect event data format

3. **Ask specific questions in chat:**
   ```
   You: Why would check() return None when failure_rate = 0.25 and threshold = 0.2?
   
   Copilot: The issue might be in the comparison operator. Check if you're using
   > instead of >=, or if the threshold is being compared correctly.
   ```

### Refactoring with Copilot

**Pattern:**

1. Select the code to refactor
2. Press `Ctrl+I`
3. Ask for specific changes:
   - "Extract this into a separate method"
   - "Add error handling"
   - "Make this more readable"
   - "Optimize this loop"

**Example:**

Before:
```python
def process(data):
    result = []
    for item in data:
        if item['value'] > 0:
            result.append(item['value'] * 2)
    return sum(result) / len(result) if result else 0
```

Ask: "Make this more Pythonic and add type hints"

After:
```python
def process(data: List[Dict[str, float]]) -> float:
    """Process data and return the average of doubled positive values."""
    doubled_positives = [item['value'] * 2 for item in data if item['value'] > 0]
    return sum(doubled_positives) / len(doubled_positives) if doubled_positives else 0.0
```

## Copilot + Project Tools

### Copilot + Black Formatter

Copilot suggestions are automatically formatted by Black when you save (format on save is enabled).

**Workflow:**
1. Accept Copilot suggestion
2. Save file (`Ctrl+S`)
3. Black formats automatically
4. Code matches project style

### Copilot + Ruff Linter

If Copilot suggests code that violates Ruff rules:

1. Ruff highlights the issue
2. Use `Ctrl+.` for quick fixes
3. Or ask Copilot: "Fix Ruff errors in this code"

### Copilot + Mypy Type Checker

Copilot is type-hint aware, but if type errors occur:

1. Run `mypy src` to see errors
2. Select the problematic code
3. Ask Copilot: "Fix mypy type errors"

### Copilot + Pytest

Generate comprehensive tests:

**Pattern:**
```python
# Test: FeedbackMonitor should handle empty events gracefully
def test_empty_events():
    # Copilot generates complete test
```

**Or ask in chat:**
```
You: Generate pytest cases for FeedbackMonitor edge cases

Copilot: Here are test cases for edge scenarios:
1. Empty event list
2. Events with missing fields
3. Events with invalid timestamps
4. Extreme threshold values
[generates code]
```

## Advanced Techniques

### 1. Context Files

Create a `.github/copilot-instructions.md` file (included in this repo) to provide project-wide context:

- Coding standards
- Architecture decisions
- Common patterns
- Project-specific conventions

### 2. Workspace Context

Copilot uses your entire workspace for context:
- Other open files
- Project structure
- Import statements
- Recent edits

**Tip:** Open related files in VS Code to give Copilot better context.

### 3. Multi-file Edits

Use Copilot Chat for changes spanning multiple files:

```
You: I need to add logging to FeedbackMonitor. Show me what files need to change.

Copilot: You'll need to modify:
1. src/syntechrev_polycodcal/feedback_monitor.py - Add logging calls
2. requirements.txt - Add logging library if needed
3. tests/test_feedback_monitor.py - Test logging behavior
[provides code for each]
```

## Troubleshooting

### Copilot Not Working

**Check:**
1. Copilot icon in status bar (bottom right)
2. Extension is installed and enabled
3. You're signed in to GitHub
4. Your subscription is active

**Fix:**
- Restart VS Code
- Sign out and sign back in
- Check extension output for errors

### Poor Suggestions

**Causes:**
- Insufficient context
- Vague variable names
- No type hints
- No comments

**Solutions:**
- Add descriptive comments
- Use clear variable names
- Add type hints
- Open related files for context

### Copilot Suggests Wrong Patterns

**Fix:**
- Reject the suggestion
- Provide a counter-example
- Add a comment explaining the correct pattern
- Use Copilot Chat to clarify: "Use this pattern instead: [example]"

## Privacy and Security

### What Copilot Sees

- Code in the current file
- Related code in open files
- File paths and names
- Comments and docstrings

### What Copilot Doesn't See

- Files not in the workspace
- Private repositories you don't have access to
- Credentials or secrets (shouldn't be in code anyway!)

### Best Practices

- ❌ Don't commit secrets or credentials
- ✅ Use environment variables for sensitive data
- ✅ Review Copilot suggestions before accepting
- ✅ Treat Copilot as a junior developer - review its work

## Learning Resources

### Official Documentation

- [GitHub Copilot Docs](https://docs.github.com/en/copilot)
- [Copilot in VS Code](https://code.visualstudio.com/docs/editor/artificial-intelligence)

### Project-Specific Resources

- [CODE_REPAIR_STRATEGY.md](CODE_REPAIR_STRATEGY.md) - Quality standards
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines
- [docs/DEVELOPMENT_WORKFLOW.md](docs/DEVELOPMENT_WORKFLOW.md) - Development process

## Tips for Success

1. **Start with comments** - Describe what you want, then let Copilot suggest
2. **Review everything** - Copilot is a tool, not a replacement for thinking
3. **Iterate** - If first suggestion isn't right, try rephrasing or adding context
4. **Learn from suggestions** - Copilot can teach you new patterns and APIs
5. **Combine tools** - Use Copilot with linters, formatters, and type checkers
6. **Ask questions** - Use chat to understand code, not just generate it
7. **Provide feedback** - Thumbs up/down help improve suggestions

## Example: Complete Feature Development

Here's a complete example of adding a new feature with Copilot:

**Goal:** Add response time percentile tracking to FeedbackMonitor

**Step 1: Plan with Chat**
```
You: How should I add p95 response time tracking to FeedbackMonitor?

Copilot: [Provides architecture suggestions]
```

**Step 2: Update Data Model**
```python
# Add response_time_ms field to event tracking
# Copilot suggests the implementation
```

**Step 3: Add Calculation Method**
```python
def calculate_p95_response_time(self) -> float:
    """Calculate the 95th percentile response time."""
    # Copilot completes the implementation
```

**Step 4: Write Tests**
```python
def test_p95_response_time_calculation():
    """Test that p95 response time is calculated correctly."""
    # Copilot generates comprehensive test
```

**Step 5: Update Documentation**
```python
# Update docstrings - Copilot helps
# Update README - Copilot suggests changes
```

**Step 6: Review and Commit**
```bash
# Review all Copilot-generated code
# Run tests: pytest -v
# Run linters: ruff check .
# Format: black src tests
# Commit with clear message
```

---

**Happy coding with Copilot! 🤖✨**

Remember: Copilot is your AI pair programmer, but you're still the driver. Review, test, and validate everything!

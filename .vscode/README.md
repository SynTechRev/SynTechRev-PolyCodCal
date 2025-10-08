# VS Code Development Configuration

This directory contains VS Code workspace settings optimized for Python development on this project.

## Quick Setup

1. **Install Recommended Extensions**
   - Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
   - Type "Extensions: Show Recommended Extensions"
   - Click "Install All"

2. **Set Up Virtual Environment**
   ```bash
   python -m venv .venv
   # On Windows: .venv\Scripts\activate
   # On Unix/Mac: source .venv/bin/activate
   pip install -r dev-requirements.txt
   ```

3. **Select Python Interpreter**
   - Press `Ctrl+Shift+P`
   - Type "Python: Select Interpreter"
   - Choose `.venv/bin/python`

## Files Overview

### `settings.json`
Workspace-level settings that configure:
- Python interpreter path
- Test framework (pytest)
- Linter (mypy)
- Formatter (black)
- Format on save
- File watchers and exclusions

### `extensions.json`
Recommended VS Code extensions for this project:
- **ms-python.python**: Core Python support
- **ms-python.vscode-pylance**: Advanced IntelliSense
- **ms-python.black-formatter**: Code formatting
- **charliermarsh.ruff**: Fast linting
- **matangover.mypy**: Type checking
- **ryanluker.vscode-coverage-gutters**: Coverage visualization
- **eamodio.gitlens**: Git integration

### `launch.json`
Debug configurations:
1. **Python: Current File** - Debug the currently open file
2. **Python: Debug Tests** - Debug all tests in current file
3. **Python: Debug Current Test** - Debug selected test function
4. **Python: Feedback Monitor CLI** - Debug the CLI script
5. **Python: All Tests with Coverage** - Run all tests with coverage

### `tasks.json`
Pre-configured tasks:
- **Run Tests** (default test task) - `Ctrl+Shift+T`
- **Run Tests with Coverage**
- **Format Code with Black**
- **Run Linter (Ruff)**
- **Run Type Checker (Mypy)**
- **Run Pre-commit Hooks**
- **Quality Checks (All)** (default build task) - `Ctrl+Shift+B`
- **Install Dependencies**
- **Install Pre-commit Hooks**

## Common Workflows

### Running Tests

**From Command Palette** (`Ctrl+Shift+P`):
- "Tasks: Run Test Task" → "Run Tests"

**From Terminal**:
```bash
pytest -v
```

**Using Debug Configuration**:
1. Open a test file
2. Press `F5`
3. Choose "Python: Debug Tests"

**With Test Explorer**:
- Open Testing view (flask icon in activity bar)
- Click play button next to test

### Debugging a Test

1. Set breakpoint in test or source code (click left of line number)
2. Open test file
3. Press `F5`
4. Choose "Python: Debug Tests"
5. Use debug controls (step over, step into, continue)

### Running Quality Checks

**All checks** (format, lint, type-check, test):
- Press `Ctrl+Shift+B`
- Or: `Ctrl+Shift+P` → "Tasks: Run Build Task"

**Individual checks**:
- `Ctrl+Shift+P` → "Tasks: Run Task"
- Choose desired task (format, lint, mypy, etc.)

### Formatting Code

**Automatic** (on save):
- Just save the file (`Ctrl+S`)

**Manual**:
- Right-click in editor → "Format Document"
- Or: `Shift+Alt+F` (Windows/Linux) / `Shift+Option+F` (Mac)

### Viewing Coverage

After running tests with coverage:
1. Install "Coverage Gutters" extension (if not already)
2. Press `Ctrl+Shift+P`
3. Type "Coverage Gutters: Display Coverage"
4. Green/red highlights show covered/uncovered lines

### Git Integration

**With GitLens** (installed):
- See inline blame annotations
- View file history
- Compare versions
- Track changes

**Basic Git**:
- Source Control view (`Ctrl+Shift+G`)
- Stage/unstage changes
- Commit with message
- Push/pull

## Keyboard Shortcuts

### Testing
- `Ctrl+Shift+T` - Run tests
- `F5` - Start debugging

### Code Navigation
- `F12` - Go to definition
- `Ctrl+F12` - Go to implementation
- `Shift+F12` - Find all references
- `Ctrl+T` - Go to symbol in workspace

### Editing
- `Ctrl+Space` - Trigger IntelliSense
- `Ctrl+.` - Quick fix
- `Shift+Alt+F` - Format document
- `Ctrl+/` - Toggle comment

### Terminal
- `` Ctrl+` `` - Toggle terminal
- `Ctrl+Shift+5` - Split terminal

### Tasks
- `Ctrl+Shift+B` - Run build task (Quality Checks)
- `Ctrl+Shift+T` - Run test task

## Tips and Tricks

### 1. Auto-format on Save
Already configured! Just save files and Black will format them.

### 2. Import Organization
Imports are automatically organized on save.

### 3. Type Hints IntelliSense
Pylance provides rich type information. Hover over variables/functions to see types.

### 4. Quick Test Run
Right-click on a test function → "Run Test" or "Debug Test"

### 5. Coverage in Editor
After running tests with coverage, use Coverage Gutters to see line-by-line coverage.

### 6. Multi-cursor Editing
- `Ctrl+D` - Select next occurrence
- `Ctrl+Shift+L` - Select all occurrences
- `Alt+Click` - Add cursor

### 7. Command Palette
`Ctrl+Shift+P` is your friend! Type what you want to do.

### 8. Integrated Terminal
Run commands without leaving VS Code. Toggle with `` Ctrl+` ``

## Troubleshooting

### Python Interpreter Not Found
1. Ensure virtual environment is created: `python -m venv .venv`
2. Press `Ctrl+Shift+P` → "Python: Select Interpreter"
3. Choose `.venv/bin/python` or `.venv/Scripts/python.exe`

### Tests Not Discovered
1. Check Python interpreter is set to `.venv`
2. Ensure pytest is installed: `pip install pytest`
3. Reload window: `Ctrl+Shift+P` → "Developer: Reload Window"

### Formatter Not Working
1. Install black-formatter extension
2. Check Python interpreter is correct
3. Ensure black is installed: `pip install black`

### Type Checking Not Working
1. Install mypy: `pip install mypy`
2. Check `mypy.ini` exists in workspace root
3. Reload window

### Coverage Not Displaying
1. Install Coverage Gutters extension
2. Run tests with coverage: `pytest --cov=src --cov-report=xml`
3. Press `Ctrl+Shift+P` → "Coverage Gutters: Display Coverage"

## Advanced Configuration

### Custom Python Path
If not using `.venv`, update in `settings.json`:
```json
"python.defaultInterpreterPath": "/path/to/your/python"
```

### Additional Pytest Arguments
Modify in `settings.json`:
```json
"python.testing.pytestArgs": [
  "tests",
  "-v",
  "--your-arg"
]
```

### Exclude Additional Files
Add to `settings.json`:
```json
"files.exclude": {
  "**/*.pyc": true,
  "your_pattern": true
}
```

## Resources

- [GitHub Integration Guide](GITHUB_INTEGRATION_GUIDE.md) - Set up GitHub authentication
- [VS Code Python Tutorial](https://code.visualstudio.com/docs/python/python-tutorial)
- [VS Code Testing](https://code.visualstudio.com/docs/python/testing)
- [VS Code Debugging](https://code.visualstudio.com/docs/editor/debugging)
- [Project CONTRIBUTING.md](../CONTRIBUTING.md)
- [Project CODE_REPAIR_STRATEGY.md](../CODE_REPAIR_STRATEGY.md)
- [Workspace Status Report](../WORKSPACE_STATUS.md) - Complete workspace verification

## Support

For issues with:
- **VS Code**: Check VS Code documentation
- **Extensions**: Check extension documentation
- **Project code**: See [CONTRIBUTING.md](../CONTRIBUTING.md)

---

Happy coding! 🚀

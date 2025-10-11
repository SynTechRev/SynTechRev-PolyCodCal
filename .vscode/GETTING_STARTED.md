# Getting Started with VS Code & GitHub Copilot

## Quick Start (2 Minutes)

### 1. Open the Workspace
```
File → Open Workspace from File
Select: SynTechRev-PolyCodCal.code-workspace
```

### 2. Install Extensions
When prompted, click **"Install All"** for recommended extensions.

Or manually:
```
Ctrl+Shift+P → "Extensions: Show Recommended Extensions" → Install All
```

### 3. Select Python Interpreter
```
Ctrl+Shift+P → "Python: Select Interpreter"
Choose: .venv/bin/python (or .venv\Scripts\python.exe on Windows)
```

### 4. Verify Copilot is Active
Look for the Copilot icon in the status bar (bottom-right).
Should show: **"Copilot: Ready"**

## First Steps with Copilot

### Try Code Completion
1. Open `src/syntechrev_polycodcal/core.py`
2. At the end, start typing:
   ```python
   # Function to reverse a string
   ```
3. Copilot will suggest a complete function!
4. Press `Tab` to accept, `Esc` to reject

### Try Copilot Chat
1. Press `Ctrl+Alt+I` (or click Copilot Chat icon)
2. Ask: "How do I add a new method to FeedbackMonitor?"
3. Get project-specific guidance!

### Generate Tests
1. Open `src/syntechrev_polycodcal/core.py`
2. Open Copilot Chat (`Ctrl+Alt+I`)
3. Ask: "Generate pytest tests for greet() with 100% coverage"
4. Copy suggested tests to `tests/test_core.py`

## Common Tasks

### Run Tests
- **Quick**: `Ctrl+Shift+B` → Choose "Run Tests"
- **Terminal**: `pytest -v`
- **Debug**: Open test file, press `F5`, choose "Python: Debug Tests"

### Format Code
- **Automatic**: Save file (`Ctrl+S`) - formats automatically
- **Manual**: `Shift+Alt+F`
- **Task**: `Ctrl+Shift+B` → "Format Code with Black"

### Check Code Quality
- **All Checks**: `Ctrl+Shift+B` → Choose "Quality Checks (All)"
- **Runs**: Black, Ruff, Tests with coverage

### View Type Errors
- Pylance shows errors in real-time (red underlines)
- Hover to see details
- Or: `Ctrl+Shift+M` to open Problems panel

## Keyboard Shortcuts

### Copilot
- `Tab` - Accept suggestion
- `Esc` - Reject suggestion
- `Alt+]` - Next suggestion
- `Alt+[` - Previous suggestion
- `Ctrl+Alt+I` - Open Copilot Chat

### Coding
- `Ctrl+Space` - IntelliSense
- `Ctrl+.` - Quick fix
- `F12` - Go to definition
- `Shift+F12` - Find references

### Testing & Debugging
- `F5` - Start debugging
- `F9` - Toggle breakpoint
- `F10` - Step over
- `F11` - Step into

### Navigation
- `Ctrl+P` - Quick open file
- `Ctrl+T` - Go to symbol
- `Ctrl+G` - Go to line

## Tips

### 1. Read Copilot Instructions
Copilot follows guidelines in `.vscode/copilot-instructions.md`.
Review it to understand what Copilot knows about the project.

### 2. Use Descriptive Comments
```python
# Good: "Calculate negative feedback rate from sliding window"
# Bad: "Calculate rate"
```

### 3. Ask Copilot Chat
When stuck, ask questions:
- "How do I test this function?"
- "What's the best way to handle None values?"
- "Explain this code"

### 4. Review Suggestions
Copilot is smart but always review:
- Check type hints are correct
- Verify error handling
- Ensure tests have 100% coverage

### 5. Run Quality Checks
Before committing:
```
Ctrl+Shift+B → "Quality Checks (All)"
```

## Troubleshooting

### Copilot Not Working?
1. Check status bar - should show "Copilot: Ready"
2. If not, click icon and sign in
3. Restart VS Code if needed

### Type Errors Everywhere?
1. Check Python interpreter is selected (.venv)
2. Reload window: `Ctrl+Shift+P` → "Developer: Reload Window"

### Imports Not Working?
1. Verify workspace file is open (not just folder)
2. Check status bar shows Python version
3. `src/` should be in Python path

### Format Not Working on Save?
1. Check settings: `editor.formatOnSave` should be `true`
2. Verify Black extension is installed
3. Reload window if needed

## Next Steps

1. ✅ **You're set up!** Start coding with Copilot
2. 📖 Read [COPILOT_INTEGRATION.md](../../COPILOT_INTEGRATION.md) for details
3. 📚 Check [.vscode/README.md](README.md) for advanced features
4. 🚀 Make your first contribution!

## Need Help?

- **Copilot Chat**: `Ctrl+Alt+I` - Ask questions!
- **Documentation**: See [docs/INDEX.md](../docs/INDEX.md)
- **VS Code Guide**: [.vscode/README.md](README.md)
- **Integration Guide**: [COPILOT_INTEGRATION.md](../../COPILOT_INTEGRATION.md)

---

**Remember**: Copilot is your AI pair programmer. Use it to learn, code faster, and maintain quality! 🚀

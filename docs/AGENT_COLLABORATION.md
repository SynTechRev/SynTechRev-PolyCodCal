# Agent Collaboration Guide

This guide explains how different AI agents and tools can work together effectively on this project, ensuring smooth cross-platform communication and task coordination.

## Overview

This project is designed to support multiple AI coding agents working together:
- **GitHub Copilot**: Inline code suggestions and completions
- **GitHub Copilot Chat**: Conversational assistance and explanations
- **Copilot Workspace Agents**: Pull request and issue automation
- **Other AI Tools**: Compatible with any AI tool respecting project conventions

## Project State Management

### Repository Structure

The repository maintains clear separation of concerns:

```
SynTechRev-PolyCodCal/
├── src/                      # Source code (all agents can modify)
├── tests/                    # Test suite (all agents can modify)
├── scripts/                  # CLI utilities (all agents can modify)
├── docs/                     # Documentation (all agents can modify)
├── .vscode/                  # VSCode settings (tracked, collaborative)
├── .github/                  # GitHub workflows and agent instructions
│   ├── copilot-instructions.md  # Instructions for Copilot
│   └── workflows/           # CI/CD configurations
└── examples/                # Example data files
```

### Files to Track vs Ignore

**Always tracked** (commit these):
- Source code: `src/`, `tests/`, `scripts/`
- Configuration: `.vscode/` workspace settings, `pyproject.toml`, `mypy.ini`
- Documentation: `docs/`, `README.md`, `CONTRIBUTING.md`, etc.
- Dependencies: `requirements.txt`, `dev-requirements.txt`
- CI/CD: `.github/workflows/`

**Never tracked** (`.gitignore` excludes these):
- Virtual environments: `.venv/`, `venv/`
- Python cache: `__pycache__/`, `*.pyc`
- Test artifacts: `.pytest_cache/`, `htmlcov/`, `.coverage`
- Build artifacts: `dist/`, `build/`, `*.egg-info/`
- IDE user settings: `.vscode/*.code-workspace` (workspace-specific)

### Branch Strategy

**Main branches:**
- `main`: Production-ready code, always stable
- `feature/*`: New feature development
- `fix/*`: Bug fixes
- `docs/*`: Documentation updates
- `copilot/*`: Copilot-generated branches

**Agent collaboration pattern:**
1. Create feature branch from `main`
2. Make changes in isolated commits
3. Push regularly for CI verification
4. Create PR when ready
5. Merge after approval and passing checks

## Communication Protocols

### 1. Code Comments for Context

Agents should use specific comment patterns for communication:

**Task handoff:**
```python
# TODO(agent-name): Task description
# Example: TODO(copilot): Implement error handling for edge case
```

**Design decisions:**
```python
# DESIGN: Why this approach was chosen
# Example: DESIGN: Using deque for O(1) window management
```

**Cross-agent notes:**
```python
# NOTE(to-next-agent): Context or warning
# Example: NOTE(to-next-agent): This function is used by CLI, don't change signature
```

**Issues requiring human input:**
```python
# FIXME(human-needed): Describe what needs human decision
# Example: FIXME(human-needed): Choose between approach A or B for performance
```

### 2. Commit Message Convention

All agents should follow Conventional Commits:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `test`: Adding or updating tests
- `refactor`: Code restructuring
- `style`: Formatting changes
- `chore`: Maintenance tasks

**Examples:**
```bash
feat(monitor): add percentile tracking to FeedbackMonitor
fix(core): correct timezone handling in timestamp conversion
docs(readme): update installation instructions
test(monitor): add edge case tests for empty window
```

### 3. PR Descriptions

Use this template for consistency:

```markdown
## Summary
Brief description of changes

## Changes Made
- [ ] Task 1
- [ ] Task 2
- [x] Task 3 (completed)

## Testing
- How changes were tested
- Test results

## Agent Notes
- Context for next agent or reviewer
- Dependencies or considerations
```

## Task Coordination

### Sequential Tasks (One Agent at a Time)

**Pattern:** Each agent completes a full task before next agent starts

**Example workflow:**
1. **Agent A**: Implements feature
   - Writes code
   - Writes tests
   - Updates docs
   - Commits: "feat: add new feature"

2. **Agent B**: Reviews and enhances
   - Adds edge case handling
   - Improves error messages
   - Commits: "refactor: improve error handling"

3. **Agent C**: Documentation
   - Updates user guide
   - Adds examples
   - Commits: "docs: add usage examples"

### Parallel Tasks (Multiple Agents)

**Pattern:** Different agents work on independent files/features

**Safe for parallel work:**
- Different modules in `src/`
- Different test files
- Different documentation files
- Independent scripts

**Requires coordination:**
- Same source file
- Shared configuration
- Test dependencies

**Merge strategy:**
```bash
# Agent A's work
git checkout -b feature/agent-a-task
# ... make changes ...
git commit -m "feat: implement feature A"

# Agent B's work (parallel)
git checkout -b feature/agent-b-task
# ... make changes ...
git commit -m "feat: implement feature B"

# Merge both
git checkout main
git merge feature/agent-a-task
git merge feature/agent-b-task
# Resolve conflicts if any
```

### Conflict Resolution Protocol

When changes conflict:

1. **Automatic resolution (if possible):**
   - Accept formatting changes from most recent agent
   - Merge non-overlapping changes
   - Preserve all functionality

2. **Human escalation (if needed):**
   ```python
   # CONFLICT: Agent A added X, Agent B added Y
   # HUMAN-DECISION: Which approach to use?
   # Option A: (show code)
   # Option B: (show code)
   ```

## Cross-Platform Compatibility

### Path Handling

**Always use forward slashes in config files:**
```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python"
}
```
This works on all platforms (VSCode translates on Windows).

**In Python code, use `pathlib`:**
```python
from pathlib import Path

# Good - cross-platform
project_root = Path(__file__).parent.parent
config_file = project_root / "config" / "settings.json"

# Avoid - platform-specific
config_file = "config\\settings.json"  # Windows only
```

### Command Examples

Provide cross-platform alternatives:

```markdown
**Windows (PowerShell):**
```powershell
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```
```

### Environment Variables

Set in platform-specific way:

```bash
# Linux/macOS
export PYTHONPATH="${PWD}/src"

# Windows PowerShell
$env:PYTHONPATH = "${PWD}\src"

# Windows Command Prompt
set PYTHONPATH=%CD%\src
```

VSCode settings handle this automatically:
```json
"terminal.integrated.env.linux": {"PYTHONPATH": "${workspaceFolder}/src"},
"terminal.integrated.env.osx": {"PYTHONPATH": "${workspaceFolder}/src"},
"terminal.integrated.env.windows": {"PYTHONPATH": "${workspaceFolder}/src"}
```

## Quality Standards

### All Agents Must

**Before committing:**
- [ ] Run tests: `pytest -v`
- [ ] Format code: `black src tests scripts`
- [ ] Check linting: `ruff check .`
- [ ] Type check: `mypy src`
- [ ] Update relevant docs

**Code standards:**
- Type hints on all functions
- Docstrings for public APIs
- Test coverage for new code
- No breaking changes to existing APIs

**Documentation standards:**
- Update README if adding features
- Add examples for new functionality
- Keep CHANGELOG.md current
- Cross-reference related docs

### CI/CD Integration

All changes are automatically verified:

```yaml
# .github/workflows/ci.yml
- Run tests on Python 3.11, 3.12, 3.13
- Check formatting with Black
- Lint with Ruff
- Type check with mypy
- Calculate coverage
- Report to Codecov
```

**Wait for CI before merging:**
- ✅ All checks must pass
- ✅ Coverage must not decrease
- ✅ No new linting errors

## Tool-Specific Guidelines

### GitHub Copilot

**Usage:**
- Read `.github/copilot-instructions.md` for project context
- Use inline suggestions for routine code
- Use Copilot Chat for explanations and refactoring
- Respect existing patterns and conventions

**Best practices:**
- Accept suggestions that match project style
- Modify suggestions to add type hints if missing
- Verify suggestions with tests
- Don't blindly accept - understand the code

### GitHub Copilot Workspace

**When creating PRs:**
- Use descriptive branch names: `copilot/feature-description`
- Include task checklist in PR description
- Reference related issues
- Add "Ready for Review" when complete

**When addressing reviews:**
- Create commits addressing each comment
- Use "fix(review): address feedback on X"
- Update PR description with progress

### Custom AI Tools

**Integration requirements:**
- Respect `.gitignore`
- Follow commit message convention
- Run quality checks before committing
- Update documentation with code changes

**Configuration:**
Read these files for context:
- `.github/copilot-instructions.md` - Code style and patterns
- `CONTRIBUTING.md` - Workflow and standards
- `CODE_REPAIR_STRATEGY.md` - Quality methodology
- `docs/ENVIRONMENT_RESET.md` - Setup procedures

## Handoff Procedures

### Completing Your Task

**Before passing to next agent:**

1. **Verify your changes:**
   ```bash
   pytest -v                    # All tests pass
   black --check src tests      # Formatting correct
   ruff check .                 # No linting errors
   mypy src                     # Type checking passes
   ```

2. **Update documentation:**
   - Code comments for complex logic
   - Docstrings for new functions
   - README if feature added
   - CHANGELOG with entry

3. **Commit with context:**
   ```bash
   git add .
   git commit -m "feat: description
   
   - Detail 1
   - Detail 2
   
   Next steps: [describe what's needed next]"
   ```

4. **Push and notify:**
   ```bash
   git push origin feature/your-branch
   ```

### Picking Up Someone's Work

**Before starting:**

1. **Understand context:**
   ```bash
   git log --oneline -10        # Recent commits
   git diff main...HEAD         # What changed
   ```

2. **Check for notes:**
   - Read commit messages
   - Look for TODO/NOTE comments
   - Review PR description

3. **Verify environment:**
   ```bash
   pytest -v                    # Tests pass
   python --version             # Python 3.11+
   pip list                     # Dependencies installed
   ```

4. **Continue work:**
   - Make incremental changes
   - Test frequently
   - Commit regularly
   - Document as you go

## Common Scenarios

### Scenario 1: Feature Implementation

**Agent workflow:**
1. Create branch: `feature/add-percentile-tracking`
2. Implement feature in `src/`
3. Add tests in `tests/`
4. Update docstring and README
5. Run quality checks
6. Commit: `feat(monitor): add percentile tracking`
7. Push and create PR

### Scenario 2: Bug Fix

**Agent workflow:**
1. Create branch: `fix/timezone-handling`
2. Add failing test demonstrating bug
3. Fix the bug
4. Verify test passes
5. Run full test suite
6. Commit: `fix(core): correct timezone handling`
7. Push and create PR

### Scenario 3: Documentation Update

**Agent workflow:**
1. Create branch: `docs/improve-quickstart`
2. Update documentation files
3. Verify examples still work
4. Check links and formatting
5. Commit: `docs: improve quickstart guide`
6. Push and create PR

### Scenario 4: Refactoring

**Agent workflow:**
1. Create branch: `refactor/extract-validation`
2. Write tests for current behavior
3. Refactor code
4. Verify all tests still pass
5. Check no API changes
6. Commit: `refactor(monitor): extract validation logic`
7. Push and create PR

## Emergency Procedures

### Critical Bug in Main

1. Create hotfix branch: `fix/critical-bug`
2. Minimal fix only
3. Add test for bug
4. Fast-track review
5. Merge immediately after CI passes

### Merge Conflict

1. Fetch latest: `git fetch origin main`
2. Attempt merge: `git merge origin/main`
3. If conflicts, mark for human:
   ```python
   # MERGE-CONFLICT: Description
   # HUMAN-NEEDED: Resolve conflict between X and Y
   ```
4. Create issue with details
5. Wait for human resolution

### CI Failure

1. Check failure logs in GitHub Actions
2. Reproduce locally: `pytest -v` or `ruff check .`
3. Fix issue
4. Commit: `fix(ci): resolve test failure`
5. Push for re-verification

## Best Practices Summary

**Do:**
- ✅ Follow existing patterns and conventions
- ✅ Write comprehensive tests
- ✅ Update documentation with code
- ✅ Use type hints consistently
- ✅ Run quality checks before committing
- ✅ Make small, focused commits
- ✅ Provide context in commit messages
- ✅ Test cross-platform compatibility

**Don't:**
- ❌ Commit generated files (.venv, __pycache__, etc.)
- ❌ Make breaking changes without discussion
- ❌ Skip tests or quality checks
- ❌ Remove working code without justification
- ❌ Mix multiple unrelated changes in one commit
- ❌ Leave TODO comments without context
- ❌ Assume Windows-only or Linux-only

## Resources

- **Setup**: `QUICKSTART.md`, `GETTING_STARTED.md`
- **Contributing**: `CONTRIBUTING.md`
- **Workflow**: `docs/DEVELOPMENT_WORKFLOW.md`
- **Quality**: `CODE_REPAIR_STRATEGY.md`
- **Environment**: `docs/ENVIRONMENT_RESET.md`
- **VSCode**: `.vscode/README.md`
- **Copilot**: `.github/copilot-instructions.md`

## Getting Help

**For agents:**
- Read relevant documentation files
- Check commit history for context
- Look for TODO/NOTE comments
- Review PR descriptions

**For humans:**
- Open an issue with "agent-question" label
- Tag "agent-coordination" for workflow questions
- Provide context: what agent, what task, what error

---

This collaboration framework ensures smooth coordination between AI agents, maintainers, and contributors while maintaining code quality and project consistency across all platforms.

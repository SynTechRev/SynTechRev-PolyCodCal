# Development Workflow

This document provides a visual and step-by-step guide to the development workflow for SynTechRev-PolyCodCal.

## Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Development Lifecycle                     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │  1. Setup        │
                    │  Environment     │
                    └──────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │  2. Create       │
                    │  Feature Branch  │
                    └──────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │  3. Develop      │
                    │  & Test          │◄──┐
                    └──────────────────┘   │
                              │            │
                              ▼            │
                    ┌──────────────────┐   │
                    │  4. Quality      │   │
                    │  Checks          │   │
                    └──────────────────┘   │
                              │            │
                              ▼            │
                    ┌──────────────────┐   │
                    │  5. Commit       │   │
                    │  Changes         │───┘
                    └──────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │  6. Push &       │
                    │  Create PR       │
                    └──────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │  7. Code Review  │
                    │  & CI/CD         │
                    └──────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │  8. Merge to     │
                    │  Main            │
                    └──────────────────┘
```

## Detailed Steps

### Step 1: Setup Environment

**First time only:**

```bash
# Clone repository
git clone https://github.com/SynTechRev/SynTechRev-PolyCodCal.git
cd SynTechRev-PolyCodCal

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On Unix/Mac:
source .venv/bin/activate

# Install dependencies
pip install -r dev-requirements.txt
pip install -e .

# Install pre-commit hooks
pre-commit install

# Verify setup
pytest -v
```

**Result:** Development environment ready ✅

### Step 2: Create Feature Branch

```bash
# Ensure you're on main and up to date
git checkout main
git pull origin main

# Create and switch to feature branch
git checkout -b feature/your-feature-name
```

**Branch naming conventions:**
- `feature/add-notification-system`
- `bugfix/fix-timestamp-parsing`
- `docs/update-api-guide`
- `refactor/simplify-monitor-logic`
- `test/add-edge-case-tests`

**Result:** Working on isolated feature branch ✅

### Step 3: Develop & Test

This is an iterative cycle:

```
┌────────────────────────────────────────┐
│        Development Cycle               │
│                                        │
│  1. Write Code                         │
│      ↓                                 │
│  2. Write/Update Tests                 │
│      ↓                                 │
│  3. Run Tests Locally                  │
│      ↓                                 │
│  4. Debug if Failed  ──────────┐       │
│      ↓                         │       │
│  5. Tests Pass? ───NO──────────┘       │
│      │                                 │
│      YES                               │
│      ↓                                 │
│  Continue Development or Move to       │
│  Quality Checks                        │
└────────────────────────────────────────┘
```

**Commands:**

```bash
# Run tests
pytest -v

# Run specific test file
pytest tests/test_feedback_monitor.py -v

# Run with coverage
pytest --cov=src/syntechrev_polycodcal --cov-report=term-missing

# Debug mode (stop on first failure)
pytest -x -v

# Verbose output
pytest -vv -s
```

**VS Code shortcuts:**
- `Ctrl+Shift+T` - Run tests
- `F5` - Debug tests

**Result:** Feature implemented with passing tests ✅

### Step 4: Quality Checks

Before committing, run all quality checks:

```bash
# Format code
black src tests scripts

# Run linter
ruff check .

# Type checking
mypy src

# All checks (or use pre-commit)
pre-commit run --all-files
```

**VS Code shortcut:**
- `Ctrl+Shift+B` - Run all quality checks

**Expected output:**
```
✓ black - passed
✓ ruff - passed  
✓ mypy - passed
✓ pytest - 15 passed
```

**Result:** Code meets quality standards ✅

### Step 5: Commit Changes

```bash
# Stage changes
git add .

# Or stage specific files
git add src/syntechrev_polycodcal/feedback_monitor.py
git add tests/test_feedback_monitor.py

# Commit with conventional commit message
git commit -m "feat: add email notification support"

# Or with detailed description
git commit -m "feat: add email notification support

- Implement EmailNotifier class
- Add SMTP configuration
- Update FeedbackMonitor to use notifier
- Add tests for email notifications"
```

**Commit message format:**
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `test`: Tests
- `refactor`: Code refactoring
- `style`: Formatting
- `chore`: Maintenance

**Result:** Changes committed locally ✅

### Step 6: Push & Create Pull Request

```bash
# Push feature branch
git push origin feature/your-feature-name

# If first push of this branch
git push -u origin feature/your-feature-name
```

**On GitHub:**

1. Navigate to repository
2. Click "Compare & pull request"
3. Fill out PR template:
   - Clear title
   - Summary of changes
   - How you tested
   - Check all checklist items
4. Link related issues (if any)
5. Submit PR

**PR Template checklist:**
```markdown
## Summary
Brief description of changes

## Changes
- Change 1
- Change 2

## Verification
- [x] Unit tests added/updated
- [x] Manual testing performed
- [x] CI pipeline passes

## Checklist
- [x] Tests added / updated
- [x] Documentation updated
- [x] CI passes
```

**Result:** PR created and ready for review ✅

### Step 7: Code Review & CI/CD

**Automated CI/CD checks:**

```
┌──────────────────────────────────────┐
│         CI/CD Pipeline               │
├──────────────────────────────────────┤
│  1. Checkout Code                    │
│  2. Setup Python (3.11, 3.12, 3.13)  │
│  3. Install Dependencies             │
│  4. Run Ruff Linting                 │
│  5. Run Mypy Type Checking           │
│  6. Run Pre-commit Hooks             │
│  7. Run Pytest Tests                 │
│  8. Generate Coverage Report         │
│  9. Upload to Codecov                │
└──────────────────────────────────────┘
```

**What happens:**
- GitHub Actions runs automatically on push
- Tests run on multiple Python versions
- Coverage report generated
- Status checks appear on PR

**Code review process:**

1. **Reviewer assigned** (or self-assign)
2. **Reviewer checks:**
   - Code correctness
   - Test coverage
   - Code style and clarity
   - Documentation
   - Potential issues
3. **Reviewer provides feedback**
   - Comments on specific lines
   - Suggests changes
   - Approves or requests changes

**Responding to feedback:**

```bash
# Make requested changes
# ... edit files ...

# Run quality checks again
pre-commit run --all-files

# Commit changes
git add .
git commit -m "fix: address review feedback"

# Push updates
git push origin feature/your-feature-name
```

**Result:** PR approved and CI passes ✅

### Step 8: Merge to Main

**When ready to merge:**

1. Ensure all CI checks pass ✅
2. Ensure PR is approved ✅
3. Resolve any merge conflicts
4. Choose merge strategy:
   - **Squash and merge** (recommended for feature branches)
   - **Merge commit** (for collaborative branches)
   - **Rebase and merge** (for clean history)

5. Click "Merge pull request"
6. Delete feature branch (optional but recommended)

```bash
# After merge, update local main
git checkout main
git pull origin main

# Delete local feature branch
git branch -d feature/your-feature-name
```

**Result:** Changes merged to main ✅

## Code Repair Workflow

Special workflow for fixing issues:

```
┌────────────────────────────────────────┐
│        Code Repair Process             │
├────────────────────────────────────────┤
│  1. Identify Issue                     │
│     - Run tests to see failures        │
│     - Check linting errors             │
│     - Review type checking issues      │
│                                        │
│  2. Prioritize Repairs                 │
│     - Critical: Test failures          │
│     - High: Import/syntax errors       │
│     - Medium: Type checking            │
│     - Low: Formatting                  │
│                                        │
│  3. Fix Systematically                 │
│     - One category at a time           │
│     - Test after each fix              │
│     - Commit incrementally             │
│                                        │
│  4. Verify Comprehensively             │
│     - All tests pass                   │
│     - Coverage maintained/improved     │
│     - No linting violations            │
│     - Type checking passes             │
│                                        │
│  5. Document Changes                   │
│     - Update CHANGELOG.md              │
│     - Add comments if needed           │
│     - Update documentation             │
└────────────────────────────────────────┘
```

See [CODE_REPAIR_STRATEGY.md](../CODE_REPAIR_STRATEGY.md) for complete details.

## Common Scenarios

### Scenario 1: Adding a New Feature

```bash
# 1. Create branch
git checkout -b feature/add-webhooks

# 2. Implement feature
# ... write code ...

# 3. Add tests
# ... write tests ...

# 4. Run tests
pytest -v

# 5. Format and lint
black src tests
ruff check .

# 6. Commit
git commit -m "feat: add webhook notification support"

# 7. Push and create PR
git push -u origin feature/add-webhooks
```

### Scenario 2: Fixing a Bug

```bash
# 1. Create branch
git checkout -b bugfix/fix-timestamp-tz

# 2. Write failing test first (TDD)
# ... add test that demonstrates bug ...

# 3. Verify test fails
pytest tests/test_feedback_monitor.py::test_timestamp_tz -v

# 4. Fix the bug
# ... fix code ...

# 5. Verify test passes
pytest tests/test_feedback_monitor.py::test_timestamp_tz -v

# 6. Run all tests
pytest -v

# 7. Commit
git commit -m "fix: handle timezone correctly in timestamps"

# 8. Push and create PR
git push -u origin bugfix/fix-timestamp-tz
```

### Scenario 3: Updating Documentation

```bash
# 1. Create branch
git checkout -b docs/update-api-docs

# 2. Update documentation
# ... edit .md files or docstrings ...

# 3. Preview changes (for markdown)
# Open in VS Code markdown preview

# 4. Commit
git commit -m "docs: update API documentation with examples"

# 5. Push and create PR
git push -u origin docs/update-api-docs
```

## Best Practices

### Do's ✅

1. **Run tests frequently** - catch issues early
2. **Commit small, logical changes** - easier to review
3. **Write descriptive commit messages** - helps reviewers
4. **Keep branches up to date** - merge main regularly
5. **Test edge cases** - improve robustness
6. **Document as you go** - easier than later
7. **Ask for help** - use issues/discussions

### Don'ts ❌

1. **Don't commit directly to main** - always use branches
2. **Don't skip tests** - they catch bugs
3. **Don't ignore linting errors** - maintain quality
4. **Don't mix unrelated changes** - keep PRs focused
5. **Don't commit secrets** - use environment variables
6. **Don't force push** - can lose history
7. **Don't leave TODOs** - finish or create issues

## Troubleshooting

### Tests Failing

```bash
# Run with verbose output
pytest -vv -s

# Run specific test
pytest tests/test_file.py::test_function -v

# Use debugger
pytest --pdb

# Check for environment issues
python --version
pip list
```

### Linting Errors

```bash
# See all errors
ruff check .

# Auto-fix when possible
ruff check --fix .

# Format code
black src tests scripts
```

### Merge Conflicts

```bash
# Update your branch with main
git checkout main
git pull origin main
git checkout feature/your-branch
git merge main

# Resolve conflicts in files
# Edit conflicted files, remove markers
# git add resolved-file

# Complete merge
git commit

# Or use rebase instead
git rebase main
```

## Resources

- [CONTRIBUTING.md](../CONTRIBUTING.md) - Detailed contribution guide
- [CODE_REPAIR_STRATEGY.md](../CODE_REPAIR_STRATEGY.md) - Code quality guide
- [.vscode/README.md](../.vscode/README.md) - VS Code setup
- [Git Basics](https://git-scm.com/book/en/v2/Getting-Started-Git-Basics)
- [Python Testing](https://docs.pytest.org/)

## Summary

The development workflow ensures:
- ✅ High code quality
- ✅ Comprehensive testing
- ✅ Clear documentation
- ✅ Effective collaboration
- ✅ Reliable CI/CD

Follow this workflow for successful contributions! 🚀

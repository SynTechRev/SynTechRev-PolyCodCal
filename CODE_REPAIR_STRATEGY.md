# Code Repair Strategy

This document outlines the systematic approach used to identify, diagnose, and repair code quality issues in the SynTechRev-PolyCodCal repository.

## Overview

The code repair process follows a structured methodology that ensures:
- Minimal disruption to working code
- Comprehensive testing at each stage
- Consistent code quality standards
- Documented changes for future reference

## Repair Methodology

### Phase 1: Assessment

#### 1.1 Initial Analysis
- **Run existing tests** to establish baseline
  ```bash
  pytest -v
  pytest --cov=src/syntechrev_polycodcal --cov-report=xml -q
  ```
- **Check code formatting** with configured tools
  ```bash
  ruff check .
  black --check .
  ```
- **Type checking** with mypy
  ```bash
  mypy src
  ```
- **Review CI/CD pipeline** status

#### 1.2 Issue Identification
Document all issues found:
- Test failures (with error messages)
- Linting violations (by category)
- Type checking errors
- Import problems
- Formatting inconsistencies

### Phase 2: Prioritization

Order repairs by:
1. **Critical**: Test failures blocking functionality
2. **High**: Import errors, syntax errors
3. **Medium**: Type checking issues, linting violations
4. **Low**: Formatting issues, documentation gaps

### Phase 3: Systematic Repair

#### 3.1 Fix Test Failures First
- Analyze test error messages
- Verify expected vs. actual behavior
- Fix implementation or update test expectations
- Re-run tests after each fix
- Ensure no regression in passing tests

#### 3.2 Resolve Import and Syntax Issues
- Check module structure
- Verify all required dependencies
- Fix circular imports
- Ensure proper `__init__.py` files

#### 3.3 Address Type Checking
- Add missing type hints
- Fix type inconsistencies
- Use `Optional`, `Union`, etc. appropriately
- Maintain backward compatibility

#### 3.4 Fix Linting Violations
- Address errors (E-series)
- Address warnings (W-series)
- Consider code complexity (C-series)
- Maintain consistent style

#### 3.5 Format Code Consistently
- Apply black formatter
- Ensure line length compliance
- Fix indentation issues
- Remove trailing whitespace

### Phase 4: Verification

#### 4.1 Comprehensive Testing
```bash
# Run full test suite
pytest -v

# Check coverage
pytest --cov=src/syntechrev_polycodcal --cov-report=html

# Run specific test categories
pytest tests/test_feedback_monitor.py -v
pytest tests/test_feedback_monitor_extra.py -v
```

#### 4.2 Quality Checks
```bash
# Formatting
black --check .

# Linting
ruff check .

# Type checking
mypy src

# Pre-commit hooks
pre-commit run --all-files
```

#### 4.3 CI/CD Validation
- Push to feature branch
- Verify CI pipeline passes
- Check all matrix configurations
- Review coverage reports

### Phase 5: Documentation

#### 5.1 Update Code Comments
- Document complex logic
- Add docstrings to public APIs
- Include usage examples

#### 5.2 Update Project Documentation
- README.md with changes
- CHANGELOG.md entries
- API documentation

#### 5.3 Commit Messages
Follow conventional commits:
```
fix: restore feedback_monitor.py and align formatting

- Resolved indentation issues
- Fixed import statements
- Updated type hints
- Ensured 100% test coverage
```

## Tools and Configuration

### Essential Tools
- **pytest**: Testing framework
- **pytest-cov**: Coverage reporting
- **black**: Code formatting
- **ruff**: Fast linting
- **mypy**: Static type checking
- **pre-commit**: Git hook management

### Configuration Files
- `pyproject.toml`: Black, tool settings
- `setup.cfg`: pytest, coverage, flake8
- `mypy.ini`: Type checking rules
- `.pre-commit-config.yaml`: Pre-commit hooks
- `.github/workflows/ci.yml`: CI/CD pipeline

## Common Issues and Solutions

### Issue: Missing Imports
**Solution**: Add proper imports and check module structure
```python
from __future__ import annotations
from typing import Optional, Dict, List
```

### Issue: Type Errors
**Solution**: Add explicit type hints
```python
def process(data: Dict) -> Optional[Alert]:
    """Process data and return alert if threshold met."""
    pass
```

### Issue: Test Failures
**Solution**: Debug step by step
1. Read error message carefully
2. Add print statements or use debugger
3. Verify test data and expectations
4. Check for side effects between tests

### Issue: Formatting Inconsistencies
**Solution**: Use automated formatters
```bash
black src tests scripts
```

### Issue: Coverage Gaps
**Solution**: Add targeted tests
- Test edge cases
- Test error conditions
- Test all code paths

## Best Practices

### Code Changes
1. ✅ Make minimal changes to fix specific issues
2. ✅ Test after each change
3. ✅ Commit frequently with clear messages
4. ✅ Keep working code working
5. ❌ Don't refactor while repairing
6. ❌ Don't change unrelated code

### Testing Strategy
1. ✅ Run tests before making changes (baseline)
2. ✅ Run tests after each fix
3. ✅ Add tests for new edge cases discovered
4. ✅ Maintain or improve coverage
5. ❌ Don't remove existing tests without justification

### Git Workflow
1. Create feature branch from main
2. Make incremental commits
3. Push regularly to trigger CI
4. Review CI results
5. Update PR description with progress
6. Request review when ready

## Success Criteria

A repair is complete when:
- ✅ All tests pass (100% success rate)
- ✅ Code coverage meets or exceeds target (e.g., 90%+)
- ✅ No linting violations
- ✅ Type checking passes with no errors
- ✅ CI/CD pipeline succeeds on all platforms
- ✅ Documentation is updated
- ✅ Changes are reviewed and approved

## Example: feedback_monitor.py Repair

### Problem Identified
- Module had formatting issues
- Missing or incorrect imports
- Type hints inconsistent
- Tests not running

### Solution Applied
1. **Restored proper imports**
   ```python
   from __future__ import annotations
   from collections import deque, Counter
   from dataclasses import dataclass
   from datetime import datetime, timezone
   from typing import Callable, Deque, Dict, Iterable, List, Optional
   ```

2. **Fixed indentation and formatting**
   - Applied black formatter
   - Ensured consistent line length

3. **Added comprehensive type hints**
   ```python
   def ingest(self, event: Dict) -> None:
       """Ingest a single event dict with 'timestamp' and 'outcome'."""
   ```

4. **Verified all tests pass**
   ```
   15 passed in 0.04s
   ```

5. **Updated CI/CD configuration**
   - Added ruff, mypy, pre-commit checks
   - Configured codecov integration

### Result
- All tests passing
- 100% code coverage
- Clean CI/CD pipeline
- Ready for production

## Maintenance

### Regular Reviews
- Run linters weekly
- Review test coverage monthly
- Update dependencies quarterly
- Audit code quality annually

### Continuous Improvement
- Add new test cases as bugs are found
- Refactor after repair is stable
- Update documentation with lessons learned
- Share knowledge with team

## Resources

- [pytest documentation](https://docs.pytest.org/)
- [black code style](https://black.readthedocs.io/)
- [ruff linter](https://github.com/astral-sh/ruff)
- [mypy type checking](https://mypy.readthedocs.io/)
- [pre-commit hooks](https://pre-commit.com/)

## Conclusion

This systematic approach ensures reliable, maintainable code repairs that:
- Minimize risk of introducing new bugs
- Maintain code quality standards
- Provide clear documentation
- Enable team collaboration
- Support long-term project health

For questions or improvements to this strategy, please open an issue or submit a pull request.

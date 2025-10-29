# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Begin Phase 9 development cycle (0.3.0): bump package version to `0.3.0.dev0`.
- Scaffold for Ethical AI & Transparency work: initial manifesto document template and roadmap alignment.

## [0.2.1] - 2025-10-17

### Fixed
- Windows-safe filename sanitization in legal generator normalization to prevent case writes from failing on Windows (affects USC and SCOTUS normalization; ensures ingest picks up files)

### Changed
- Release workflow: add version guard against tags, fetch tags (fetch-depth: 0), use twine `--skip-existing --verbose`, and add post-publish verification step that installs from TestPyPI and runs smoke checks

## [0.2.0] - 2025-10-17

Final release of Phase 7. No changes from 0.2.0rc1.

## [0.2.0rc1] - 2025-10-17

Pre-release to exercise packaging and TestPyPI publishing pipeline.

### Added
- Legal data normalization/ingestion/retrieval pipeline (Phase 6)
- New CLIs: `genesis-gateway` and `legal-generator`
- MkDocs documentation site and homepage
- GitHub Actions workflows: CI matrix, release (TestPyPI/PyPI), docs deploy

### Changed
- Switched to setuptools src-layout with PEP 621 metadata
- Updated README with Install & CLI Quickstart

### Fixed
- Windows Python 3.13 NumPy DLL issue documented with workaround (use 3.12)

### Added - Phase 6 Complete
- Legal Generator module with comprehensive data ingestion capabilities
- Genesis Gateway module with CLI interface and processing pipeline
- Legal data normalization for multiple sources (SCOTUS, USC, Black's Law, Am Jur)
- Vector embeddings for legal case data (numpy/npz format)
- Data validation framework for legal documents
- Retrieval system for querying legal case embeddings
- 36 new tests covering legal generator and genesis gateway functionality

### Added - Phase 7 Preparation
- PEP 621 compliant project metadata in pyproject.toml
- Console script entry points: syntech-monitor, genesis-gateway, legal-generator
- Comprehensive dependency specification with optional dev dependencies
- Project URLs for homepage, documentation, issues, and changelog
- Enhanced project classifiers and keywords for PyPI readiness

### Changed
- Migrated from Poetry-style to PEP 621 [project] metadata
- Fixed requirements.txt encoding from UTF-16LE to UTF-8
- Enhanced pyproject.toml with complete packaging information
- Added main() entry point to feedback_monitor module for CLI usage

### Fixed
- Requirements.txt file encoding issue (UTF-16LE → UTF-8)

## [0.1.0] - 2025-10-08

### Added
- Comprehensive CODE_REPAIR_STRATEGY.md documenting systematic approach to code quality
- CONTRIBUTING.md guide for new and existing contributors
- CHANGELOG.md for tracking project changes
- Enhanced README.md with development workflow and resources section
- Project structure documentation
- Project roadmap document (ROADMAP.md) outlining phased enhancement plan
- Hysteresis thresholds (trigger/clear) with spike and recovery alerts

### Changed
- Updated documentation to reflect current best practices
- Improved onboarding process for new contributors

## [0.0.0] - 2025-10-08

### Added
- Initial project structure
- FeedbackMonitor implementation with sliding-window aggregation
- Alert system for negative feedback spike detection
- Comprehensive test suite (15 tests, 100% coverage)
- CI/CD pipeline with GitHub Actions
  - Testing on Python 3.11, 3.12, and 3.13
  - Code coverage reporting with Codecov
  - Automated linting with ruff
  - Type checking with mypy
  - Pre-commit hooks integration
- Development dependencies configuration
- Example scripts and data files
- Core module with basic greeting functionality

### Fixed
- Restored feedback_monitor.py with proper formatting
- Aligned code with Black/Flake8 formatting standards
- Resolved indentation issues
- Fixed import statements
- Removed unused imports

### Changed
- Updated CI workflow for idempotent operation
- Configured Codecov integration with XML coverage output
- Finalized development dependencies list

## Development Process

### Repair and Quality Improvement
The initial release represents a successful code repair process that:

1. **Established Baseline**
   - Identified formatting and linting issues
   - Documented test coverage gaps
   - Reviewed CI/CD configuration

2. **Systematic Fixes**
   - Applied Black formatter for consistent code style
   - Fixed import statements and module structure
   - Added comprehensive type hints
   - Ensured all tests pass

3. **Quality Assurance**
   - Achieved 100% test coverage (15/15 tests passing)
   - Zero linting violations
   - Clean type checking results
   - Successful CI/CD pipeline

4. **Documentation**
   - Created comprehensive contribution guide
   - Documented code repair strategy
   - Updated README with development workflow
   - Added inline code documentation

### Testing
All tests pass with 100% coverage:
- `test_core.py`: 5 tests for core functionality
- `test_feedback_monitor.py`: 3 tests for basic monitoring
- `test_feedback_monitor_extra.py`: 7 tests for advanced features

### CI/CD
GitHub Actions workflow includes:
- Multi-version Python testing (3.11, 3.12, 3.13)
- Automated linting and formatting checks
- Type checking with mypy
- Pre-commit hook validation
- Code coverage reporting to Codecov

---

## Release Notes Format

### Version Format
`MAJOR.MINOR.PATCH`

- **MAJOR**: Incompatible API changes
- **MINOR**: New functionality, backward compatible
- **PATCH**: Bug fixes, backward compatible

### Change Categories

- **Added**: New features
- **Changed**: Changes in existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Vulnerability fixes

### Example Entry

```markdown
## [1.0.0] - YYYY-MM-DD

### Added
- New feature description

### Changed
- Change description

### Fixed
- Bug fix description
```

---

## Contributing

When making changes:

1. Update this CHANGELOG.md under `[Unreleased]` section
2. Use appropriate category (Added, Changed, Fixed, etc.)
3. Write clear, concise descriptions
4. Include issue/PR numbers when applicable
5. Move entries to new version section when releasing

For more details, see [CONTRIBUTING.md](CONTRIBUTING.md).

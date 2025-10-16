# Phase 7 Kickoff: Packaging & Distribution

This document outlines scope, deliverables, and acceptance criteria to initiate Phase 7.

## 🎯 Goal
Prepare the project for distribution: consistent packaging, console entry points, and publish pipeline. Keep dependencies minimal and preserve current APIs.

## 📦 Scope
- Adopt PEP 621 `[project]` metadata in `pyproject.toml` (or choose and standardize Poetry workflow) — pick one path and make it consistent.
- Add a console script entry point for CLI (e.g., `syntech-monitor`).
- Set up PyPI publish workflow via GitHub Actions (tag-driven release).
- Generate API/docs site (mkdocs or pdoc) and publish to GitHub Pages.
- Update README with install + usage; link to docs site.

## 🧪 Acceptance Criteria
- `pip install syntechrev-polycodcal` works locally from a built wheel.
- `syntech-monitor --help` runs the CLI entry point successfully.
- GitHub Action builds sdist/wheel on tag push, uploads to PyPI (or TestPyPI) with secrets configured.
- Docs site builds and deploys to GitHub Pages; README links to it.
- Lint, type check, and tests pass; coverage does not regress.

## 📋 Tasks
1. Packaging
   - Normalize `pyproject.toml` with `[project]` metadata (name, version, description, authors, license, classifiers).
   - Ensure `src` layout is correctly included; verify package data if needed.
2. CLI Entry Point
   - Define console script in `pyproject.toml`.
   - Ensure CLI module maps to entry point (`scripts/feedback_monitor.py` or better: `syntechrev_polycodcal.__main__`).
3. CI: Build & Publish
   - Add GitHub Action to build sdist/wheel on tag.
   - Add publish step to PyPI/TestPyPI with repository secrets.
4. Docs
   - Choose mkdocs-material or pdoc.
   - Add basic nav (Overview, Usage, API, Development Guides).
   - Configure Pages deploy.
5. Documentation Updates
   - README: install, quick start, link to docs site.
   - CHANGELOG: Unreleased → add Phase 7 tasks.

## 🔧 Constraints
- Keep dependencies minimal; avoid heavy doc build plugins unless necessary.
- Do not break existing APIs; changes to CLI should be additive.

## 🧭 Risks / Mitigations
- Packaging drift: lock on one tool (PEP 621 or Poetry) and document it.
- Secret management: use GitHub Encrypted Secrets; provide TestPyPI as default.
- Doc deployment failures: add action retry and validate build locally.

## ▶️ How to Start
- Create a feature branch: `feature/phase7-packaging`.
- Implement packaging and entry point; add CI workflow in `.github/workflows/release.yml`.
- Open PR with full quality checks.

## ✅ Definition of Done
- Publish to TestPyPI from a tag
- Docs site live on GitHub Pages
- README updated
- CI green across matrix

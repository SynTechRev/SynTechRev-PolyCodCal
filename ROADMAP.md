# ROADMAP — SynTechRev-PolyCodCal

Notes:
- Optional Cython / Rust micro-optimization exploration (E)

## Phase 7 – Packaging & Distribution (P1)
Status: COMPLETE (2025-10-18)

✅ Delivered:
- PEP 621 compliant package metadata in pyproject.toml
- Console script entry points: `syntech-monitor`, `genesis-gateway`, `legal-generator`
- Tag-driven PyPI/TestPyPI publish workflow with version guard
- MkDocs documentation + GitHub Pages deployment workflow
- Package builds successfully (sdist + wheel)
- All quality gates passing (51/51 tests, linting, type checking)
- Version 0.2.1 ready for TestPyPI publication

Exit Criteria:
- ✅ Package metadata migrated to PEP 621
- ✅ Console scripts configured and tested
- ✅ Release workflow with version guard
- ✅ Documentation builds successfully
- ✅ All quality checks passing
- ⏳ TestPyPI upload pending (ready)

Delivered:
- PEP 621 `[project]` packaging with src-layout and console scripts (`syntech-monitor`, `genesis-gateway`, `legal-generator`)
- Tag-driven release workflow with version guard, TestPyPI publish, and post-install verification
- Docs site build and deploy to GitHub Pages

Notes:
- Release v0.2.1 finalized; workflow hardened for future releases

## Phase 8 – Quality & Governance (P2)
Goal: Enhance project security, community engagement, and maintenance automation.
Status: COMPLETE (2025-10-18)

Planned Items:
1. Security documentation (`SECURITY.md`)
   - Vulnerability reporting process
   - Security policy
   - Supported versions

2. Community guidelines (`CODE_OF_CONDUCT.md`)
   - Expected behavior standards
   - Enforcement procedures
   - Contact information

3. Issue templates (`.github/ISSUE_TEMPLATE/`)
   - Bug report template
   - Feature request template
   - Performance issue template

4. Pull request template (`.github/pull_request_template.md`)
   - Checklist for contributors
   - Testing requirements
   - Documentation updates

5. Dependabot configuration (`.github/dependabot.yml`)
   - Automated dependency updates
   - Version monitoring
   - Security vulnerability alerts

6. CodeQL security scanning (`.github/workflows/codeql.yml`)
   - Automated code analysis
   - Security vulnerability detection
   - Scheduled scans

Delivered:
- `SECURITY.md`, `CODE_OF_CONDUCT.md`, `LICENSE_COMPLIANCE.md`, `GOVERNANCE.md`
- `.github/dependabot.yml` configured for pip and GitHub Actions (weekly)
- `.github/workflows/codeql.yml` for CodeQL analysis on push/PR

Acceptance:
- All governance documents in place
- Templates functional and helpful
- Dependabot monitoring dependencies
- CodeQL scanning on schedule
- No new security issues introduced

Notes:
- Dependabot and CodeQL pipelines enabled; governance and conduct aligned with project’s ethical-theological orientation

## Phase 9 – Ethical AI & Transparency Manifesto Integration (P1)
Goal: Establish explicit ethical AI principles, transparency commitments, and provenance practices for SynTechRev-PolyCodCal.
Status: IN PROGRESS (2025-10-29)

Planned Items:
1. Ethical AI & Transparency Manifesto (docs/ETHICAL_AI_TRANSPARENCY.md)
   - Purpose, scope, and values (aligned with project’s ethical-theological orientation)
   - Acceptable use and prohibited misuse
   - Safety, fairness, and harm minimization posture
   - Governance and escalation pathways

2. Transparency & Provenance
   - Data usage and provenance statement
   - Model and dataset cards (templates, if applicable)
   - Auditability commitments and review cadence

3. Operationalization
   - Link manifesto in README and docs index
   - Add CI check to ensure manifesto presence (later)
   - Document process for periodic review and updates

Acceptance:
- Manifesto present, reviewed, and linked from README/docs
- Clear statements on acceptable use, safety, and provenance
- Roadmap updated and CHANGELOG includes Unreleased entry for Phase 9

---
Last updated: 2025-10-29

# Project Roadmap

This roadmap outlines prioritized upcoming improvements for SynTechRev-PolyCodCal.
It is intentionally incremental: each phase can be delivered and reviewed independently.

## Legend
- P0: Highest impact / unblockers
- P1: Important, near-term value
- P2: Nice to have / longer-term
- (E) Experimental / subject to change

## Phase 1 – Stabilize & Plan (P0)
Status: COMPLETE (2025-10-11)
- ✅ Baseline code + tests green
- ✅ Documentation consolidation
- ✅ Tooling: Ruff, mypy, pytest, coverage, pre-commit
- ✅ Tagging and release process documented (TAGGING_GUIDE.md)
- ✅ Cleanup automation scripts created
- ✅ Merge cleanup PR to `main`
- ✅ Tag initial release (v0.1.0)

Deliverable Exit Criteria:
- PR merged, branch deleted
- Roadmap published (this file)
- Release tagged and documented

## Phase 2 – Core Monitoring Enhancements (P0)
Goal: Improve robustness and flexibility of the `FeedbackMonitor`.

Planned Items:
1. Hysteresis thresholds (trigger vs clear) to reduce alert flapping
2. Batched ingest: `ingest_many(events: Iterable[Event])` for efficiency
3. Time-based window option (last N seconds) alongside count-based (if introduced)
4. Configurable max top sources param (expose constant currently hard-coded at 5)
5. Structured Event type (TypedDict) and stricter validation path
6. Alert cooldown (min separation window between identical alert types)

Acceptance:
- 100% test coverage retained
- Backward compatibility for existing API
- Comprehensive docstrings + README examples updated

## Phase 3 – Metrics & Extensibility (P1)
Goal: Allow pluggable derived metrics beyond negative rate.

Features:
- Register custom metric functions returning (name, value)
- Include all active metrics in `summarize()` and `check()` details
- Optional metric-specific thresholds / alert types

Risks / Mitigations:
- Complexity: keep metric functions pure & side-effect free
- Performance: cache per-window computations where possible

## Phase 4 – Observability & Instrumentation (P1)
- Structured logging hook (callback interface or stdlib logging integration)
- Prometheus-style metrics adapter (export counters/gauges)
- Debug inspection: introspect current buffer & expiration stats

## Phase 5 – CLI & Usability (P1)
Status: COMPLETE (2025-10-11)

Delivered:
- Comprehensive tagging and cleanup automation
- VS Code tagging documentation and troubleshooting
- Repository hygiene scripts (safe cleanup) and guidelines
- Documentation refresh and resources indexing

Notes:
- CLI subcommands are slated for a future iteration; Phase 5 scoped to reliability, docs, and release readiness.

## Phase 6 – Performance & Scale (P2)
- Benchmark harness (events/sec at various window sizes)
- Memory profiling & optimization (consider ring buffer specialization)
- Optional Cython / Rust micro-optimization exploration (E)

## Phase 7 – Packaging & Distribution (P1)
- Normalize packaging: migrate from `[tool.poetry]` to PEP 621 `[project]` or adopt full Poetry workflow consistently
- Add console script entry point (`syntech-monitor`)
- Prepare PyPI publish workflow (tag-driven GitHub Action)
- Generate API docs (mkdocs or pdoc) + GitHub Pages deployment

## Phase 8 – Quality & Governance (P2)
- Add `SECURITY.md`, `CODE_OF_CONDUCT.md`
- Issue / PR templates for feature, bug, performance
- Dependabot configuration for dependency update PRs
- CodeQL security scanning workflow

## Phase 9 – Advanced Features (P2 / E)
- Sliding percentile latency tracking (if latency incorporated into events)
- Multi-window multi-resolution summaries (e.g., 1m / 5m / 15m)
- Pluggable persistence (SQLite or in-memory only toggle)
- Streaming API / async variant (async ingest & alert streaming)

## Cross-Cutting Requirements
- Maintain >= 95% coverage (stretch: 100%)
- Zero mypy errors (`strict` mode candidate after Phase 2)
- Ruff clean; avoid disabling rules unless justified
- Each feature lands with docs + tests + CHANGELOG updates

## Open Questions
- Do we enforce thread-safety? (Likely document as non-thread-safe initially)
- Do we support user-defined outcome classification precedence? (Future)
- Is time-based expiration sufficient vs count-based window? (Monitor feedback)

## Sequencing Recommendation (Short Term)
1. Merge current cleanup PR
2. Implement hysteresis + batched ingest (Phase 2 subset)
3. Expose configurable max top sources parameter
4. Introduce metric registration hook
5. Add CLI simulation command

## Contribution Guide Alignment
Each feature PR must include:
- Tests (happy path + edge cases + failure modes)
- CHANGELOG Unreleased entry
- Updated README or usage docs
- No drop in coverage

---
Last updated: 2025-10-11

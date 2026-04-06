# Changelog

All notable changes to `spec-driven-advanced` are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
This project adheres to [Semantic Versioning](https://semver.org/).

## [1.1.0] — 2026-04-06

### Added
- **`references/parallel-agents.md`** — full dispatch protocol for parallel sub-agents at the analytical phases (1, 3, 8) and the safety checklist for the rare cases parallelism is safe in Phase 6.
- **Parallelism Strategy** section in `SKILL.md` — concise table of where to parallelize and where not to, with mandatory rules for any parallel dispatch.
- **Phase 1 (Research)** is now **parallel by default** — dispatch 4 fresh-context sub-agents (file-locator, pattern-detector, dependency-mapper, constraint-finder) in a single message, then a sequential synthesizer consolidates them into `research.md`. Expected gain: 3–5× wall-clock on big brownfield investigations.
- **Phase 3 (Plan)** gains an optional **`--explore` mode** that dispatches 2–3 sub-agents drafting alternative architectures (conservative / idiomatic / forward-looking biases), then a synthesizer picks one and documents the rejected alternatives.
- **Phase 8 (Code Review)** is now a **multi-critic panel by default** — 4 fresh-context critic agents (security, performance, maintainability, ac-coverage) dispatched in parallel via Task tool, then a sequential review-synthesizer consolidates them into the unified `review.md`. Expected gain: 2–3× catch rate.
- `Task` added to `allowed-tools` in `SKILL.md` frontmatter to enable parallel sub-agent dispatch.

### Changed
- **Phase 6 (Implement)** documentation now explicitly states sequential is the default and almost always correct, with a strict safety checklist for the rare cases parallel implementation is acceptable (mechanical refactors on disjoint files with zero shared state).
- **Critical Rule #6** (writer/reviewer separation) updated to reference the new multi-critic panel as the default protocol.
- `metadata.version` bumped to `1.1.0`.
- `metadata.domains` adds `parallel-agents`.

### Notes
- This is an additive release. No script signatures changed. No artifact templates changed. Existing `.sdd/` projects continue to work without modification.
- Parallelism multiplies token cost roughly linearly with the number of sub-agents. The ROI is highest on Phase 1 (research) and Phase 8 (review). For trivial features, single-agent mode remains acceptable.

## [1.0.0] — 2026-04-06

### Added
- Initial release.
- Lean `SKILL.md` (~180 lines) implementing the complete 10-phase SDD+RPI workflow with progressive disclosure to `references/`.
- `references/phases.md` — full description of every phase.
- `references/templates.md` — copy-paste templates for all 8 artifacts + status dashboard.
- `references/review-system.md` — error classification (P0/P1/P2), iteration protocol, writer/reviewer separation, validator behavior.
- `scripts/init_sdd_project.py`, `scripts/new_feature.py`, `scripts/validate_phase.py` — Python 3 stdlib only, with shared `Result` dataclass pattern, exit codes (0/1/10), and self-verification.
- Two human gates (Phases 4 and 8) mechanically enforced by `validate_phase.py`.
- `install.sh` / `--uninstall` / `--force`.
- Bilingual `README.md` (English + Português).
- `LICENSE` (MIT), `.gitignore`, `.skillignore`.

[1.1.0]: https://github.com/eduardodotai/spec-driven-advanced/releases/tag/v1.1.0
[1.0.0]: https://github.com/eduardodotai/spec-driven-advanced/releases/tag/v1.0.0

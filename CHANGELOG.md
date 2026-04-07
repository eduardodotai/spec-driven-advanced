# Changelog

All notable changes to `spec-driven-advanced` are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
This project adheres to [Semantic Versioning](https://semver.org/).

## [1.2.1] — 2026-04-07

### Changed
- **Phase -1 interview is now fully multilingual.** The agent's first message in `/sdd-vision` (and any other interactive phase) asks **in English** which language the user wants to use for the interview, then adapts every subsequent question. The final `product-vision.md` is still always written in English regardless of interview language. Previously the interview was hardcoded to PT-BR → EN.
- **Canonical question bank is now in English** in `references/vision.md`. PT-BR examples remain as illustrative translations (alongside Español, Français, Italiano, Deutsch) showing how the agent adapts questions per language.
- The agent records `interview_language: <code>` in the output document's frontmatter for auditability.
- Default language is **English** when the user does not specify, skips, or says "default".
- Mid-interview language switches are supported — answers are preserved.
- `references/guided-mode.md` clarifies that the PT-BR translation tables are illustrative; the agent adapts jargon translations to whichever language the user selected.
- `metadata.version` bumped to `1.2.1`.

### Notes
- This is a refinement of v1.2.0, not a new feature. Existing v1.2.0 behavior (defaulting to PT-BR) is replaced by the more universal default-to-English-with-explicit-choice flow.
- No script changes. No template changes. No artifact format changes.

## [1.2.0] — 2026-04-07

### Added
- **Phase -1: PRODUCT VISION** — a new phase that runs *before* the Constitution on greenfield projects. Captures the high-level product story (overview, problem, goals, target users, core capabilities, tech stack preference, out-of-scope, success metrics) so every downstream phase has the "why" and "for whom" available without re-litigation.
- **`/sdd-vision`** slash command — bilingual interview that asks questions in PT-BR (user's native language) and writes the artifact in English. Optional for brownfield (can reverse-engineer from codebase + interview).
- **`references/vision.md`** — full Phase -1 deep doc: bilingual question bank (12 questions in 6 blocks), output protocol, brownfield reverse-engineering flow.
- **Guided Mode (`--guided` flag)** — accessibility layer for non-engineers (or engineers wanting lower friction on side projects). Translates technical jargon into plain-language questions, infers smart defaults from product type, accepts vague answers. Available on `/sdd-init`, `/sdd-vision`, `/sdd-spec`, `/sdd-plan`. The output artifacts and quality bars are **identical** to default mode — only the conversation is friendlier.
- **`references/guided-mode.md`** — full translation table for Phases 0/2/3, smart defaults by product type (web app, mobile, CLI, API, prototype), auto-detection rules (2+ vague answers → offer to switch).
- **product-vision.md template** added to `references/templates.md`.
- **`scripts/init_sdd_project.py --with-vision-stub`** — new flag that also creates a `.sdd/product-vision.md` stub. Self-verification updated.
- **Plain English summary banner** — when guided mode is active, every artifact gets a "In plain English:" callout at the top so non-technical stakeholders can review without reading the structured doc.

### Changed
- **Phase 0 (Constitution)** is now **vision-aware**: if `.sdd/product-vision.md` exists, the agent loads it first and pre-fills Constitution articles (especially Article 2 Tech Stack and Article 8 Security). A 12-question Constitution interview can collapse to ~3 questions when guided mode + vision are both active.
- **Phase 2 (Spec)** loads `.sdd/product-vision.md` automatically so feature specs stay anchored in the product story.
- **Routing logic** in SKILL.md updated: greenfield → Phase -1 → Phase 0 → Phase 2; brownfield → Phase -1 (optional) → Phase 0 → Phase 1 → Phase 2.
- **Quick Start** in SKILL.md now includes a 4th question about technical comfort (engineer vs non-engineer / `--guided`).
- `metadata.version` bumped to `1.2.0`.
- `metadata.domains` adds `product-vision` and `guided-mode`.

### Notes
- This is an additive release. Existing `.sdd/` projects from v1.0.0 / v1.1.0 continue to work — Phase -1 and `--guided` are opt-in.
- `scripts/new_feature.py` and `scripts/validate_phase.py` are unchanged. Phase -1 is interactive (run by the agent), so it does not need a script — only the optional stub creator.
- Audit score from v1.1.0 (92/100) is preserved; the additions follow the same patterns (lean SKILL.md, lazy-loaded references, no jargon escaping into the main file).

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

[1.2.1]: https://github.com/eduardodotai/spec-driven-advanced/releases/tag/v1.2.1
[1.2.0]: https://github.com/eduardodotai/spec-driven-advanced/releases/tag/v1.2.0
[1.1.0]: https://github.com/eduardodotai/spec-driven-advanced/releases/tag/v1.1.0
[1.0.0]: https://github.com/eduardodotai/spec-driven-advanced/releases/tag/v1.0.0

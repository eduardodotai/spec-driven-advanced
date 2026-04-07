---
name: spec-driven-advanced
description: >
  Complete Spec-Driven Development + Research-Plan-Implement (SDD+RPI) workflow
  for AI-assisted software engineering. Guides any project through 10 structured
  phases: Constitution, Research, Spec, Plan, Plan Review, Tasks, Implement,
  Verify, Code Review, Iterate, Ship. Use this skill whenever the user mentions
  SDD, RPI, spec-driven, spec first, research plan implement, constitution,
  structured workflow, agentic workflow, plan before code, no vibe coding,
  build properly, build the right way, plan first, dumb zone, writer reviewer
  separation, plan gate, code review gate, two human gates, brownfield,
  greenfield, or asks to add a feature with discipline, refactor with a plan,
  migrate technologies, set up engineering rigor for AI coding agents, or
  even just says "help me build X properly" or "do this the right way".
license: MIT
model: claude-opus-4-6
user-invocable: true
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Edit
  - Bash
  - Task
metadata:
  version: 1.2.0
  author: eduardodotai
  domains: [meta-skill, software-engineering, sdd, rpi, workflow, planning, agentic, parallel-agents, product-vision, guided-mode]
  type: workflow-orchestrator
---

# Spec-Driven Advanced — SDD + RPI in 10 Phases

A production-grade workflow that fuses **Spec-Driven Development** (specs are the source of truth) with **Research-Plan-Implement** (research before plan, plan before code, fresh context per phase). It exists to eliminate "vibe coding" on serious projects by forcing thinking *upstream* of code.

**Three core principles:**
1. **Specs are the source of truth.** Code serves specs, not the reverse.
2. **You cannot outsource the thinking.** AI amplifies thinking you have already done.
3. **Context is a scarce resource.** Each phase resets context with compacted artifacts to stay out of the "Dumb Zone".

## Quick Start

When invoked, ask the user these questions in order:

1. **Greenfield or brownfield?** New project from scratch, or existing codebase?
   - Greenfield → run Phase -1 (Vision) → Phase 0 (Constitution) → Phase 2 (Spec). Skip Phase 1 (Research).
   - Brownfield → Phase 1 (Research) is **mandatory**. Phase -1 (Vision) is optional but recommended if no vision doc exists.
2. **What do you want to build or change?** One-paragraph problem statement.
3. **Do you already have `.sdd/product-vision.md` and `.sdd/constitution.md`?** Load whichever exist; run the missing phases.
4. **Technical comfort?** Engineer (default) or non-engineer / want lower friction (`--guided` mode). Guided mode translates jargon and infers smart defaults — same output quality, friendlier interview.

Then run `scripts/init_sdd_project.py` (if no `.sdd/` exists) and `scripts/new_feature.py <name>` for the new feature scaffold.

## The Phases (Compact Reference)

| # | Phase | When | Output | Mode | Gate |
|---|-------|------|--------|------|------|
| -1 | **Vision** | Greenfield init, before Constitution | `.sdd/product-vision.md` | Bilingual interview (PT→EN) | — |
| 0 | **Constitution** | Project init, one time | `.sdd/constitution.md` | Interactive interview, vision-aware | — |
| 1 | **Research** | Brownfield only, before each feature | `research.md` | Agent autonomous (read-only) | — |
| 2 | **Spec** | After Research (or Constitution if greenfield) | `spec.md` | Collaborative draft | — |
| 3 | **Plan** | After Spec | `plan.md` | Agent drafts | — |
| 4 | **Plan Review** | After Plan, before any code | `plan-review.md` | Human + critic agent | **Human Gate #1** |
| 5 | **Tasks** | After plan approved | `tasks.md` | Agent decomposes | — |
| 6 | **Implement** | One task at a time | code + tests | Agent, fresh context per task | — |
| 7 | **Verify** | After each task and after all tasks | `verify.md` | Automated (build/test/lint/types) | — |
| 8 | **Code Review** | After Verify passes | `review.md` | **Fresh-context** critic agent + human | **Human Gate #2** |
| 9 | **Iterate** | If review found issues | updated code + review | Agent fixes (max 3 cycles) | — |
| 10 | **Ship** | After review approved | `ship.md` + changelog | Agent prepares delivery | — |

> Read `references/phases.md` for the deep description of each phase, and `references/templates.md` for the artifact templates.

## Routing Logic (Phases -1 → 0 Branching)

```
on_invoke:
  if no .sdd/ at project root:
    → run scripts/init_sdd_project.py [--with-vision-stub if greenfield]

  ask: greenfield or brownfield?

  if greenfield:
    if no .sdd/product-vision.md (or it's a stub):
      → run Phase -1 (Vision interview)  ← bilingual, may use --guided
    if no .sdd/constitution.md (or it's a stub):
      → run Phase 0 (Constitution interview), pre-filled from product-vision.md
    skip Phase 1 (Research)
    next_phase = Spec

  if brownfield:
    if no .sdd/product-vision.md:
      → offer Phase -1 (Vision) — optional, agent can reverse-engineer from codebase
    if no .sdd/constitution.md:
      → run Phase 0 — agent infers from existing codebase, presents for confirmation
    Phase 1 (Research) is MANDATORY for every feature
    next_phase = Research

  if user says "I'm in the middle of feature NNN":
    scan .sdd/features/NNN-*/ for the latest non-empty artifact
    resume from the next phase after that
    run scripts/validate_phase.py to confirm readiness
```

Never auto-skip a phase that produced no artifact unless the project is greenfield and the phase is Research.

## Directory Structure

```
.sdd/
├── product-vision.md           # Phase -1 — product story (greenfield) — v1.2.0+
├── constitution.md             # Phase 0 — permanent project governance
├── changelog.md                # Running log of all shipped features
└── features/
    └── NNN-feature-name/       # one folder per feature
        ├── research.md         # Phase 1 (brownfield only)
        ├── spec.md             # Phase 2 (loads product-vision.md as context)
        ├── plan.md             # Phase 3
        ├── plan-review.md      # Phase 4 — Human Gate #1
        ├── tasks.md            # Phase 5
        ├── verify.md           # Phase 7
        ├── review.md           # Phase 8 — Human Gate #2
        └── ship.md             # Phase 10
```

## Slash Commands

When running inside Claude Code, expose these commands. Each one loads only the artifacts it needs (context engineering).

| Command | Phase | Purpose |
|---------|-------|---------|
| `/sdd-vision` | -1 | Bilingual interview (PT→EN) — produces `product-vision.md`. Greenfield only. |
| `/sdd-init [--with-vision-stub] [--guided]` | 0 | Bootstrap `.sdd/` and walk the user through the constitution interview |
| `/sdd-research <feature>` | 1 | Brownfield codebase investigation, no code, no opinions |
| `/sdd-spec <feature>` | 2 | Draft the spec (problem, goals, ACs, edge cases) |
| `/sdd-plan <feature>` | 3 | Draft the technical plan (architecture, data, contracts) |
| `/sdd-review-plan <feature>` | 4 | Present plan to human + run critic agent — Gate #1 |
| `/sdd-tasks <feature>` | 5 | Decompose plan into atomic, testable tasks |
| `/sdd-implement <feature> [task]` | 6 | Implement one task with fresh context |
| `/sdd-verify <feature>` | 7 | Run build, tests, lint, types — write `verify.md` |
| `/sdd-review-code <feature>` | 8 | Fresh-context critic reviews vs spec — Gate #2 |
| `/sdd-iterate <feature>` | 9 | Apply review fixes; re-runs verify + review (max 3 cycles) |
| `/sdd-ship <feature>` | 10 | Produce `ship.md` + update changelog |
| `/sdd-status [feature]` | * | Show progress across all features and current phase |

## Scripts

All scripts are Python 3 stdlib only. Run from project root.

| Script | Usage | Purpose |
|--------|-------|---------|
| `scripts/init_sdd_project.py` | `python scripts/init_sdd_project.py [--path .] [--force]` | Bootstrap `.sdd/` with constitution stub, empty `features/`, and changelog stub. Exit codes: 0 ok, 10 already exists, 1 error. |
| `scripts/new_feature.py` | `python scripts/new_feature.py <feature-name> [--number N] [--path .]` | Create `.sdd/features/NNN-slug/` with all 8 artifact stubs. Auto-numbers if `--number` omitted. Refuses if constitution still has `[TO BE FILLED]` markers. |
| `scripts/validate_phase.py` | `python scripts/validate_phase.py <feature_path> <target_phase>` | Verify the feature is ready to advance to `target_phase`. Checks prior artifacts exist, contain required sections, have no stub markers, and (for plan-review/review) carry an APPROVED decision. Exit 0 ready, 10 not ready, 1 error. |

## Parallelism Strategy

Parallelize **analysis**, not **execution**. The bottleneck of AI-assisted engineering is upstream thinking, not keystroke speed. Dispatch parallel sub-agents (single message, multiple Task tool calls) at the analytical phases; keep implementation sequential.

| Phase | Default | Parallel mode | Gain |
|---|---|---|---|
| **1 — Research** | Parallel by default | 4 sub-agents: file-locator, pattern-detector, dependency-mapper, constraint-finder + sequential synthesizer | 🔥 Large (3–5× wall-clock on big brownfield) |
| **3 — Plan** | Sequential | Optional `--explore`: 2–3 sub-agents draft conservative / idiomatic / forward-looking alternatives + synthesizer picks one | 🔥 Medium (catches trade-offs) |
| **8 — Code Review** | Multi-critic by default | 4 fresh-context critics (security, performance, maintainability, ac-coverage) in parallel + synthesizer | 🔥 Large (2–3× catch rate) |
| 6 — Implement | **Sequential, always** | Allowed only for mechanical refactors on disjoint files with zero shared state | ⚠ Risky — when in doubt, sequential |

**Mandatory rules for any parallel dispatch:**
- All sub-agents in a single message (multiple Task tool calls), never serialized
- Each sub-agent gets a fresh context with disjoint scope
- A sequential **synthesizer** consolidates outputs into the canonical artifact — raw parallel outputs are never the artifact
- The writer/reviewer separation rule still holds in Phase 8 (4× — every critic is fresh)

> Read `references/parallel-agents.md` for the full dispatch protocol, sub-agent briefing templates, and Phase 6 safety checklist.

## Guided Mode (Accessibility — v1.2.0)

The interactive phases (-1, 0, 2, 3) accept an optional `--guided` flag that translates technical jargon into plain-language questions and infers smart defaults from product type. The output artifacts and quality bars are **identical** to default mode — only the conversation is friendlier.

| Activation | Effect |
|---|---|
| `/sdd-init --guided` (or any other slash command) | Enables guided mode for that phase |
| `guided_mode: true` in `.sdd/constitution.md` frontmatter | Project-wide persistent activation |
| Auto-detect: 2+ vague answers in a row | Agent offers to switch to guided mode |

**Examples of translation:**

| Default mode | Guided mode (PT-BR) |
|---|---|
| "What's your error handling strategy?" | "Como o sistema deve reagir quando algo dá errado?" |
| "Acceptance Criteria (testable)" | "Me dá 3 exemplos do que o usuário deveria conseguir fazer no fim" |
| "Forbidden patterns?" | "Tem alguma coisa que você NÃO quer ver no código? Pode pular se não souber." |
| "Data model entities" | "Que tipos de informação o sistema precisa guardar?" |

When activated, guided mode also adds a **"In plain English"** banner at the top of every artifact so non-technical stakeholders can understand the work without reading the full structured doc.

> Read `references/guided-mode.md` for the full translation table, smart defaults by product type, and auto-detection rules.

## Critical Rules

1. **Never skip phases.** Each phase consumes artifacts the previous phase produced. Skipping = vibe coding with extra steps.
2. **Context resets between phases.** Start each phase by loading only the prior artifacts you need, not the conversation history. This keeps you out of the Dumb Zone.
3. **Two human gates: Phase 4 and Phase 8.** Both are *binary* decisions (approve / iterate / reject). Never pretend a gate happened.
4. **Constitution is permanent.** It is NOT updated mid-feature. Updates happen between features, deliberately, and bump its version.
5. **Brownfield differs from greenfield only at Phase 1.** Everything else is identical. Greenfield projects MAY revisit Phase 1 if they grow into a brownfield-like state.
6. **Writer/Reviewer separation in Phase 8.** The agent that wrote the code MUST NOT be the same context that reviews it. Default protocol is the **multi-critic panel**: 4 fresh-context sub-agents (security / performance / maintainability / ac-coverage) dispatched in parallel via Task tool, plus a sequential synthesizer. Each critic loads only spec + plan + constitution + diff — never the implementation history. See `references/parallel-agents.md`.
7. **Max 3 iterations in Phase 9.** If still failing after iteration 3, escalate to a human and consider rejecting back to Plan or Spec.
8. **One task at a time in Phase 6.** Each task starts fresh: load constitution + plan + that single task. Update `tasks.md` checkboxes as you go so you can resume after a context compaction.
9. **Research is read-only.** No code, no opinions, no suggestions in Phase 1. File paths + line numbers + a one-sentence "why" for everything found.
10. **Specs are technology-agnostic; plans are not.** Keep WHAT (spec) strictly separate from HOW (plan). The same spec must be implementable in two stacks via two different plans.

## Anti-Patterns

| Anti-pattern | Why it fails | Correct move |
|--------------|--------------|--------------|
| Vibe coding ("just build it") | No spec → AI fills gaps with hallucinated assumptions | Phase 0–5 first |
| Skipping Research on brownfield | Plan ends up referencing files that don't exist or violating real patterns | Phase 1 mandatory |
| Monolithic plan (no task decomposition) | Single context window can't hold the whole change | Phase 5 always |
| Same agent reviewing its own code | Confirmation bias, misses real issues | Fresh-context reviewer |
| No constitution | Every feature re-litigates basic standards | Phase 0 once |
| Spec contains code/tech choices | Couples WHAT to HOW, blocks alternative plans | Move to plan |
| Iterating forever | No clear failure signal | Cap at 3, then escalate |
| Loading full conversation history into next phase | Pushes tokens into the Dumb Zone | Load only artifacts |

## Deeper References (lazy load)

- `references/phases.md` — full description of every phase, when/output/mode/required sections/quality check/anti-patterns
- `references/templates.md` — copy-paste templates for all 9 artifacts (incl. product-vision.md) + status dashboard
- `references/review-system.md` — error classification, iteration protocol, writer/reviewer separation, domain checklists
- `references/parallel-agents.md` — when and how to dispatch parallel sub-agents (Phases 1, 3, 8) and the safety checklist for the rare cases parallelism is safe in Phase 6
- `references/vision.md` — Phase -1 deep doc: bilingual question bank, output protocol, brownfield reverse-engineering
- `references/guided-mode.md` — `--guided` flag: jargon translation table, smart defaults by product type, auto-detection rules

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
metadata:
  version: 1.0.0
  author: eduardodotai
  domains: [meta-skill, software-engineering, sdd, rpi, workflow, planning, agentic]
  type: workflow-orchestrator
---

# Spec-Driven Advanced — SDD + RPI in 10 Phases

A production-grade workflow that fuses **Spec-Driven Development** (specs are the source of truth) with **Research-Plan-Implement** (research before plan, plan before code, fresh context per phase). It exists to eliminate "vibe coding" on serious projects by forcing thinking *upstream* of code.

**Three core principles:**
1. **Specs are the source of truth.** Code serves specs, not the reverse.
2. **You cannot outsource the thinking.** AI amplifies thinking you have already done.
3. **Context is a scarce resource.** Each phase resets context with compacted artifacts to stay out of the "Dumb Zone".

## Quick Start

When invoked, ask the user these three questions in order:

1. **Greenfield or brownfield?** New project from scratch, or existing codebase?
   - Greenfield → skip Phase 1 (Research), go Constitution → Spec.
   - Brownfield → Phase 1 (Research) is **mandatory**.
2. **What do you want to build or change?** One-paragraph problem statement.
3. **Do you already have a `.sdd/constitution.md`?** If yes, load it. If no, run Phase 0 first.

Then run `scripts/init_sdd_project.py` (if no `.sdd/` exists) and `scripts/new_feature.py <name>` for the new feature scaffold.

## The 10 Phases (Compact Reference)

| # | Phase | When | Output | Mode | Gate |
|---|-------|------|--------|------|------|
| 0 | **Constitution** | Project init, one time | `.sdd/constitution.md` | Interactive interview | — |
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

## Routing Logic (Phase 0 Branching)

```
on_invoke:
  if no .sdd/ at project root:
    → run scripts/init_sdd_project.py
    → run Phase 0 (Constitution interview)
  else:
    → load .sdd/constitution.md

  ask: greenfield or brownfield?

  if greenfield:
    skip Phase 1 (Research)
    next_phase = Spec

  if brownfield:
    Phase 1 (Research) is MANDATORY
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
├── constitution.md             # Phase 0 — permanent project governance
├── changelog.md                # Running log of all shipped features
└── features/
    └── NNN-feature-name/       # one folder per feature
        ├── research.md         # Phase 1 (brownfield only)
        ├── spec.md             # Phase 2
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
| `/sdd-init` | 0 | Bootstrap `.sdd/` and walk the user through the constitution interview |
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

## Critical Rules

1. **Never skip phases.** Each phase consumes artifacts the previous phase produced. Skipping = vibe coding with extra steps.
2. **Context resets between phases.** Start each phase by loading only the prior artifacts you need, not the conversation history. This keeps you out of the Dumb Zone.
3. **Two human gates: Phase 4 and Phase 8.** Both are *binary* decisions (approve / iterate / reject). Never pretend a gate happened.
4. **Constitution is permanent.** It is NOT updated mid-feature. Updates happen between features, deliberately, and bump its version.
5. **Brownfield differs from greenfield only at Phase 1.** Everything else is identical. Greenfield projects MAY revisit Phase 1 if they grow into a brownfield-like state.
6. **Writer/Reviewer separation in Phase 8.** The agent that wrote the code MUST NOT be the same context that reviews it. In Claude Code, achieve this by starting a fresh session loaded with spec + constitution + diff only — NOT the implementation history.
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
- `references/templates.md` — copy-paste templates for all 8 artifacts + status dashboard
- `references/review-system.md` — error classification, iteration protocol, writer/reviewer separation, domain checklists

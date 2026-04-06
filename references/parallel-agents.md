# Parallel Agents — Where Concurrency Actually Helps

> **Added in v1.1.0.** This file is the deep reference for the *Parallelism Strategy* section in `SKILL.md`.

## The principle

Parallelism in SDD+RPI is **not** about implementing faster. It is about **analyzing wider in the same wall-clock time**. The bottleneck of AI-assisted engineering is rarely keystroke speed; it is the quality of thinking *upstream* of code.

Therefore: **parallelize the analytical phases, keep execution sequential.**

## Where to parallelize

| Phase | Sequential default | Parallel opportunity | Expected gain | Risk |
|---|---|---|---|---|
| **1 — Research** | 1 agent reads codebase | 3–4 fresh-context Explore sub-agents with disjoint scopes | 🔥 Large (3–5× wall-clock for big brownfield) | Low — read-only |
| **3 — Plan** (optional) | 1 agent drafts 1 plan | 2–3 sub-agents draft alternative architectures, then synthesize | 🔥 Medium (catches trade-offs a single agent misses) | Low — text only |
| **8 — Code Review** | 1 critic agent | Multi-critic panel: 3–4 fresh-context agents with distinct lenses, then synthesize | 🔥 Large (catch-rate up 2–3×) | Low — read-only |
| 6 — Implement | 1 task at a time | Safe **only** for mechanical refactors with zero shared state | ⚠ Often illusory | High — merge conflicts, broken builds |

## Phase 1 — Parallel Research

Dispatch 3–4 sub-agents in a **single message** (one Task tool call per agent, all in parallel) with disjoint scopes:

| Sub-agent | Scope | Output goes into research.md section |
|---|---|---|
| **file-locator** | Find every file relevant to the planned change. Return path + 1-line purpose. | "Relevant Files" table |
| **pattern-detector** | Identify how similar things are done today (auth, data access, error handling, validation). Return file:line citations. | "Existing Patterns" |
| **dependency-mapper** | Map who-imports-what for the touched modules. Identify blast radius. | "Dependencies & Impact" |
| **constraint-finder** | Surface tech debt, perf budgets, regulatory notes, version locks. | "Constraints & Risks" |

**Synthesis step (must be sequential, single agent):**
After all 4 agents return, a synthesizer reads all 4 outputs and produces the unified `research.md` with proper deduplication and the "Open Questions" section.

**Anti-patterns:**
- Letting sub-agents propose solutions (Research is read-only — no opinions)
- Overlapping scopes (file-locator and pattern-detector both citing the same files = wasted tokens)
- Skipping the synthesis step (4 raw outputs ≠ a research document)

## Phase 3 — Parallel Plan Exploration (optional `--explore` mode)

Use this when the architecture is genuinely ambiguous and you want to compare alternatives before committing.

Dispatch 2–3 sub-agents, each told to draft a complete plan from the same spec but with a different architectural bias:

| Sub-agent | Bias |
|---|---|
| **conservative** | Minimal change, reuse existing patterns, lowest risk |
| **idiomatic** | Best-fit for the constitution's preferred patterns, even if it requires moderate refactoring |
| **forward-looking** | Optimize for future extension points, accept higher upfront cost |

**Synthesis step:** A single agent reads all 2–3 plans + the spec + the constitution and produces a final `plan.md` that picks one approach (or a hybrid) with explicit trade-off documentation. The losing alternatives are listed under "Alternatives Considered" so reviewers see what was rejected and why.

**When NOT to use `--explore`:**
- Trivial features (1 endpoint, no schema change)
- Constitution dictates the answer (no real choice exists)
- You already know the answer and just want it written down

## Phase 8 — Multi-Critic Review Panel

This is the highest-value parallelism in the workflow. Dispatch **4 fresh-context** sub-agents in parallel, each loaded with `spec.md` + `constitution.md` + the diff/changed files (NOT the implementation history):

| Critic | Lens | Looks for |
|---|---|---|
| **security-critic** | OWASP Top 10, secrets handling, input validation, auth/authz, injection vectors | Critical (P0) findings |
| **performance-critic** | N+1 queries, blocking I/O, memory leaks, missing indexes, perf budget violations from constitution | Important (P1) findings |
| **maintainability-critic** | Naming, dead code, abstraction quality, test quality, comment-to-code ratio, complexity hotspots | Minor (P2) findings |
| **ac-coverage-critic** | Walks every Acceptance Criterion in `spec.md` and verifies each is testable + covered + passing | Critical (P0) — any AC not covered is a P0 |

**Synthesis step (sequential):** A 5th agent — the **review-synthesizer** — reads all 4 critic reports + spec + constitution and produces the unified `review.md` with:
- Deduplicated issue list (P0/P1/P2)
- Iteration history (if iter ≥ 2)
- Final binary decision: APPROVED / ITERATE / REJECT
- Per-AC coverage table

**Critical rule:** All 4 critic agents MUST start fresh — no implementation history. The synthesizer also starts fresh, loaded only with the 4 critic outputs + spec + constitution. This is the writer/reviewer separation rule, applied 4 times in parallel.

## Phase 6 — When (and only when) parallel implementation is safe

Default: sequential. Always.

You may dispatch tasks in parallel **only if all** of the following hold:

- [ ] The tasks are mechanical: rename, format, import reorder, codemod
- [ ] The tasks operate on **disjoint files** (no two tasks touch the same file)
- [ ] The tasks have **zero shared state** (no shared types, no schema changes, no config edits)
- [ ] Each task can be verified independently
- [ ] You can revert any single task without affecting the others

If you cannot check every box, run sequential. The few minutes you save in parallel will cost you an hour of debugging "which agent broke the build?".

**Concrete safe examples:**
- Renaming a function across 30 unrelated files
- Adding a missing copyright header to every file
- Running a codemod (e.g., `var → const`) on each file
- Bumping an import path across modules

**Concrete unsafe examples (always sequential):**
- Adding 5 endpoints that share a router file
- Implementing 3 features that share a database migration
- Refactoring an interface used by multiple consumers
- Anything that touches `package.json`, `tsconfig.json`, or other shared config

## Synthesis is mandatory

Every time you dispatch parallel sub-agents, a **single sequential synthesizer** must consolidate their outputs into the canonical artifact (`research.md`, `plan.md`, `review.md`). Raw parallel outputs are intermediate work — never commit them as the artifact.

## Claude Code mechanics

Use the **Task tool** with `subagent_type` matching the agent best suited to the scope:

| Scope | subagent_type |
|---|---|
| Codebase exploration (Phase 1) | `Explore` (or `general-purpose` if Explore unavailable) |
| Plan drafting (Phase 3 `--explore`) | `general-purpose` |
| Code review critic (Phase 8) | `general-purpose` |

Dispatch all parallel agents in a **single message with multiple Task tool calls** — sending them in separate messages serializes them and defeats the purpose.

Each sub-agent gets a fresh context. Brief them like a smart colleague who just walked into the room: full task description, scope boundaries, expected output format, and what NOT to do (e.g., "no opinions" for research agents).

## Cost note

Parallelism multiplies token cost roughly linearly with the number of sub-agents (4 agents in Phase 8 ≈ 4× the tokens of a single review). The ROI is highest when:

- The work was going to be done anyway, just slower
- The catch-rate improvement matters (security/AC critics are the obvious wins)
- You are blocked waiting for the review and the wall-clock matters more than the cost

For solo dev experimentation, run multi-critic Phase 8 on important features only and stick with single-critic for trivial ones.

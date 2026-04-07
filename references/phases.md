# SDD+RPI — The 10 Phases in Depth (now 11 with Phase -1)

This is the deep reference for `SKILL.md`. Each phase entry contains:
**When** · **Output** · **Mode** · **Required sections** · **Quality check** · **Anti-patterns**.

The phases form a strict pipeline. Each phase consumes the previous artifact and produces a new one. The two **Human Gates** (Phase 4 and Phase 8) are binary: approve, iterate, or reject.

> **Guided mode (v1.2.0+):** every interactive phase (-1, 0, 2, 3) accepts the optional `--guided` flag. When active, the agent translates technical jargon into plain-language questions, infers smart defaults from product type, and accepts vague answers. The output artifacts and quality bars are unchanged. See [`guided-mode.md`](guided-mode.md) for the full translation table and activation rules.

---

## Phase -1 — PRODUCT VISION (Foundation Before Foundation)

**When:** Greenfield projects only, before Phase 0. Optional but recommended for brownfield (run once to reverse-engineer the vision from the codebase + product owner interview).

**Output:** `.sdd/product-vision.md`

**Mode:** **Bilingual interactive interview** — agent asks questions in PT-BR (user's native language), writes the artifact in EN. The Constitution and every feature spec downstream will load this file as context, so the product story is never re-litigated.

**Required sections:**
- **Overview** — one paragraph elevator pitch
- **Problem Statement** — what, who, why now, alternatives
- **Goals** — 3–5 measurable outcomes
- **Target Users** — table of role / description / capabilities
- **Core Capabilities** — 5–10 high-level features (verbs, not implementation)
- **Technical Considerations** — auth, privacy, scale, regulatory, perf
- **Tech Stack Preference** — high-level only; exact versions go in Constitution
- **Out of Scope** — at least 3 explicit non-goals
- **Success Metrics** — how we know it's working

**Quality check:**
- A stranger reads it in under 5 minutes and understands the product
- Goals use numbers, not adjectives
- At least 3 out-of-scope items
- Tech stack lists at least language + framework
- Constitution can directly reference this file

**Anti-patterns:**
- Vision contains feature-level details (move to feature spec)
- Vision changes per feature (it's stable; update only between major pivots)
- Vague goals ("make it good") — use measurable ones
- Skipping it because "the team knows" — agents do not know
- Missing Out of Scope section — invites scope creep

> Read [`vision.md`](vision.md) for the full bilingual question bank, output protocol, and brownfield reverse-engineering flow.

---

## Phase 0 — CONSTITUTION (Foundation)

**When:** Once per project, at initialization. The constitution is permanent and reused across every feature. It is updated only deliberately, between features, with a version bump.

**Output:** `.sdd/constitution.md`

**Mode:** Interactive interview. The agent asks the user about standards and writes the document collaboratively. For brownfield projects, the agent first analyzes the existing codebase to *infer* conventions, then presents findings to the user for confirmation.

**Vision-aware (v1.2.0+):** if `.sdd/product-vision.md` exists, the agent loads it first and **pre-fills** Constitution articles from the vision (especially Article 2 Tech Stack and Article 8 Security). Many questions become confirmations instead of open prompts.

**Guided mode (v1.2.0+):** with `--guided`, jargon is translated and smart defaults by product type are applied. A 12-question Constitution interview can collapse to ~3 questions when guided mode + vision are both active. See [`guided-mode.md`](guided-mode.md).

**Required sections (9 articles):**
1. Immutable Principles — non-negotiable rules
2. Tech Stack — approved languages, frameworks, runtimes, versions
3. Architecture — style, layers, boundaries
4. Quality Gates — coverage %, lint, types, review requirements
5. Conventions — naming, file structure, imports
6. Forbidden Patterns — what must NOT appear
7. Required Patterns — what MUST appear
8. Security — auth, secrets, OWASP, compliance
9. Documentation — what to document and where

**Quality check:**
- No `[TO BE FILLED]` markers remain
- Every article has at least one concrete rule
- Tech stack lists exact versions
- Forbidden + Required patterns are explicit, not vague

**Anti-patterns:**
- Generic boilerplate ("write good code") — be specific
- Including feature requirements (those go in specs)
- Updating it mid-feature (do it deliberately, between features)
- Skipping it because "the team knows the rules" — agents don't

---

## Phase 1 — RESEARCH (Compressing Truth)

**When:** Brownfield projects only. Before every feature in an existing codebase. Greenfield projects skip this phase entirely (there is nothing to research).

**Output:** `.sdd/features/NNN-feature-name/research.md`

**Mode:** Agent autonomous, **read-only**. The agent investigates the codebase and writes a compact report. **Zero opinions. Zero code. Zero suggestions.**

**Parallel by default (v1.1.0+):** dispatch 4 fresh-context sub-agents in a single message — `file-locator`, `pattern-detector`, `dependency-mapper`, `constraint-finder` — each with a disjoint scope. Then a single sequential synthesizer consolidates their outputs into `research.md`. See [`parallel-agents.md`](parallel-agents.md#phase-1--parallel-research) for the full dispatch protocol. For trivial features (single file, no real investigation), a single agent is fine.

**Required sections:**
- **Summary** — 3–5 sentences of facts, no opinions
- **Relevant Files** — table of `path | purpose | relevance`
- **Existing Patterns** — how similar things are done today, with file:line citations
- **Dependencies & Impact** — what could break if this area is changed
- **Constraints & Risks** — technical debt, compatibility, perf, regulatory
- **Open Questions** — items that need human clarification before Spec

Every claim must include `path/to/file.ext:line` citations.

**Quality check:**
- Reading this document (and nothing else) tells you enough to write a spec
- All claims have file:line citations
- Document is 1–3 pages — neither bloated nor anemic
- Contains no opinions, no recommendations, no code edits

**Anti-patterns:**
- 10-page research for adding a button (over-research / paralysis)
- 3-line research for a database migration (under-research / sub-compaction)
- Including suggestions or fixes (that's Plan phase)
- Doing research without citations
- Letting the agent "think out loud" instead of producing the structured doc

---

## Phase 2 — SPEC (Defining the WHAT)

**When:** After Research (brownfield) or directly after Constitution (greenfield).

**Output:** `.sdd/features/NNN-feature-name/spec.md`

**Mode:** Collaborative. Agent drafts, human iterates. The spec is technology-agnostic — it says WHAT to build, never HOW.

**Vision-aware (v1.2.0+):** the agent loads `.sdd/product-vision.md` first so the spec is anchored in the product story.

**Guided mode (v1.2.0+):** with `--guided`, "Acceptance Criteria" becomes "me dá 3 exemplos do que o usuário deveria conseguir fazer", "Edge Cases" becomes "o que pode dar errado?", and so on. Translation is in [`guided-mode.md`](guided-mode.md). The output `spec.md` is identical to default mode.

**Required sections:**
- **Problem Statement** — what problem, for whom, why now
- **Goals** — measurable outcomes (numbers when possible)
- **Non-Goals** — explicit out-of-scope items
- **User Stories** — As a / I want to / so that
- **Acceptance Criteria** — testable conditions, numbered AC-1, AC-2…
- **Edge Cases** — boundary conditions and expected behavior
- **Constraints** — business rules, regulatory, performance budgets

**Quality check:**
- The Golden Rule: a *fresh* agent session can implement this spec without asking clarifying questions
- ACs are testable (someone could write a test case for each)
- Non-goals are explicit (you can list 3+ things the feature does NOT do)
- No mention of frameworks, libraries, file paths, or APIs (those belong in the plan)

**Anti-patterns:**
- Spec contains code or pseudocode → move to plan
- Spec lists endpoints or schemas → move to plan
- Vague ACs ("works well", "fast") → make them measurable
- Missing non-goals → forces scope creep later
- Skipping edge cases → bugs in production

---

## Phase 3 — PLAN (Defining the HOW)

**When:** After Spec is written.

**Output:** `.sdd/features/NNN-feature-name/plan.md`

**Mode:** Agent drafts the technical design from the spec + research + constitution. The plan turns spec ACs into a sequenced engineering blueprint.

**Guided mode (v1.2.0+):** with `--guided`, the agent proposes data models, API contracts, implementation order, and rollback plan **as suggestions** instead of asking the user to design them. The user confirms or tweaks. Constitution Compliance check runs silently and only surfaces violations. See [`guided-mode.md`](guided-mode.md).

**Optional `--explore` mode (v1.1.0+):** when the architecture is genuinely ambiguous, dispatch 2–3 sub-agents in parallel to draft alternative plans (conservative / idiomatic / forward-looking biases), then a single synthesizer picks one (or hybridizes) and documents the rejected alternatives under "Alternatives Considered". See [`parallel-agents.md`](parallel-agents.md#phase-3--parallel-plan-exploration-optional---explore-mode). Skip `--explore` for trivial features or when the constitution dictates the answer.

**Required sections:**
- **Architecture Approach** — how this fits the existing system, with a Mermaid diagram if helpful
- **Data Model** — entities, fields, migrations
- **API / Interface Contracts** — endpoints, payloads, responses
- **Implementation Phases** — ordered chunks with dependencies
- **Testing Strategy** — unit, integration, e2e per layer
- **Rollback Plan** — how to undo if it goes wrong
- **Constitution Compliance** — checklist against each constitution article

**Quality check:**
- Every spec AC is addressed somewhere in the plan
- Constitution checklist is fully checked (or has documented justified exceptions)
- A reviewer can spot a logic error from reading the plan alone
- Plan references actual files from `research.md` (brownfield) or proposed file paths (greenfield)

**Anti-patterns:**
- Plan introduces tech not approved in constitution → fix or amend constitution
- Plan ignores findings in research → re-read research
- Plan is a wall of prose → use sections, tables, diagrams
- No rollback plan → blocked by quality gate

---

## Phase 4 — PLAN REVIEW (Human Gate #1)

**When:** After Plan is written. **Before any code is written.** This is the highest-leverage review point in the entire workflow.

**Output:** `.sdd/features/NNN-feature-name/plan-review.md`

**Mode:** Human reviews + an optional fresh-context critic agent validates plan against spec and constitution. The decision is binary.

**Required sections:**
- **Summary** — what will be built, in 5 lines
- **Risks** — top risks the human should consider
- **Constitution Checklist** — pasted from plan, re-verified
- **Critic Agent Findings** (optional) — what a fresh-context agent flagged
- **Decision** — `APPROVED` / `APPROVED-WITH-CHANGES` / `REJECTED`
- **Required Changes** (if APPROVED-WITH-CHANGES) — explicit edit list
- **Rejection Reason** (if REJECTED) — return-to-phase pointer

**Quality check:**
- Decision field is filled with one of three exact values
- If APPROVED-WITH-CHANGES, the plan was actually updated and a v2 of plan-review created
- Reviewing markdown took minutes, not hours

**Anti-patterns:**
- Skipping the gate "to save time" — this is the cheapest review you'll ever do (10x cheaper than reviewing code)
- Marking APPROVED without actually reading
- Approving over an unchecked constitution box
- Letting the same agent that wrote the plan also approve it

---

## Phase 5 — TASKS (Atomic Decomposition)

**When:** After Plan is APPROVED in Phase 4.

**Output:** `.sdd/features/NNN-feature-name/tasks.md`

**Mode:** Agent decomposes the plan into atomic tasks; user confirms.

**Required per task:**
- Status checkbox `[ ]` / `[x]` / `[!]`
- Title and short description
- `Depends on:` task numbers (if any)
- `Files to modify:` exact paths
- `Verification:` how to know it works (unit test, integration test, manual check)
- `Estimated complexity:` Low / Medium / High

**Quality check:**
- Each task is implementable in a single fresh context window
- Each task is reviewable as a single commit/PR
- Dependencies form a DAG (no cycles)
- Together, the tasks fully cover the plan

**Anti-patterns:**
- One mega-task ("implement the feature") → decompose
- Tasks that depend on tasks that don't exist
- Tasks without verification criteria
- Tasks that cross unrelated layers (e.g., DB + UI in one task)

---

## Phase 6 — IMPLEMENT (Execution with Clean Context)

**When:** After Tasks are confirmed.

**Output:** Working code + tests, committed task by task.

**Mode:** Agent implements one task at a time. **Each task starts with a fresh context** loaded with: constitution.md + plan.md + that single task block. NOT the implementation history of previous tasks.

**Sequential is the default and almost always correct.** Parallel implementation is allowed **only** for purely mechanical refactors that operate on disjoint files with zero shared state (e.g., codemods, mass renames, header insertion). See the safety checklist in [`parallel-agents.md`](parallel-agents.md#phase-6--when-and-only-when-parallel-implementation-is-safe). When in doubt: sequential. The few minutes saved in parallel will cost you an hour of "which agent broke the build?".

**Per-task loop:**
1. Load constitution + plan + current task only
2. Write tests first (TDD when feasible)
3. Implement the change
4. Run Phase 7 (Verify) for this task
5. Update the checkbox in `tasks.md`
6. Commit with message `feat(NNN): task K — <title>`
7. If context fills, compact to checkboxes and continue

**Quality check:**
- All tests for the task pass locally
- The task checkbox in `tasks.md` is updated
- Commit exists for the task

**Anti-patterns:**
- Implementing multiple tasks in one context (loses the Dumb Zone protection)
- Skipping tests "to come back later" (you won't)
- Refactoring unrelated code mid-task (scope creep)
- Forgetting to update `tasks.md` (resume becomes impossible)

---

## Phase 7 — VERIFY (Automated Checks)

**When:** After every implemented task, and once more after the final task.

**Output:** `.sdd/features/NNN-feature-name/verify.md` (append-only — one report per task)

**Mode:** Automated. Agent runs the project's build/test/lint/typecheck commands and writes a structured report.

**Required per report:**
- Date + task ID
- Build: pass/fail with details
- Tests: count passed, count failed, failure details
- Lint: pass / N warnings / M errors
- Types: pass/fail with details
- Verdict: `PASS → proceed` or `FAIL → iterate`

**Quality check:**
- All four checks ran (don't skip lint or types because they're "noisy")
- Failures include enough detail to reproduce
- Verdict matches the data

**Anti-patterns:**
- Marking PASS over a known failure
- Running only tests, skipping lint/types
- Not capturing the actual command output

---

## Phase 8 — CODE REVIEW (Human Gate #2 + Critic Agent)

**When:** After all tasks complete and Phase 7 verify is green.

**Output:** `.sdd/features/NNN-feature-name/review.md`

**Mode:** **Multi-critic panel + human** (v1.1.0+). The reviewer agents MUST be different context sessions than the writer. Default protocol: dispatch **4 fresh-context sub-agents in parallel** in a single message — `security-critic`, `performance-critic`, `maintainability-critic`, `ac-coverage-critic` — each loaded with `spec.md` + `plan.md` + `constitution.md` + the diff (NOT the implementation history). Then a 5th sequential **review-synthesizer** agent consolidates the 4 outputs into the unified `review.md`. See [`parallel-agents.md`](parallel-agents.md#phase-8--multi-critic-review-panel) for the dispatch protocol. For trivial features, a single fresh-context critic is acceptable — the writer/reviewer separation rule still holds.

**Required sections:**
- **Acceptance Criteria Validation** — table mapping each AC to ✅/❌ + evidence (file:line or test name)
- **Constitution Compliance** — table per article ✅/❌
- **Issues Found** — grouped by severity P0/P1/P2 (see `review-system.md`)
- **Quality Scores** — readability, maintainability, test coverage, error handling, performance (1–5 each)
- **Iteration History** — appended each cycle
- **Decision** — `APPROVED` / `ITERATE` / `REJECT`

**Quality check:**
- Reviewer is provably a fresh context (no implementation history)
- Every AC was actually checked
- Each issue has file:line and a suggested fix
- Decision matches the issues (you cannot APPROVE with open P0s)

**Anti-patterns:**
- Same agent that wrote the code reviews it (confirmation bias)
- "LGTM" without filling the AC table
- Approving over open P0s
- Treating P2 issues as blockers (they're not)

---

## Phase 9 — ITERATE (Correction Loop)

**When:** Phase 8 returned `ITERATE`.

**Output:** Updated code + appended iteration entry in `review.md`.

**Mode:** Writer agent fixes only the issues listed in the review. Re-runs Phase 7 (Verify), then Phase 8 (Review) again with a fresh critic context.

**Decision framework:**
| Symptom | Action |
|---------|--------|
| Edge cases / minor gaps / incomplete error handling | ITERATE (fix in place) |
| Architecture mismatch with mental model | REJECT → return to Phase 3 (Plan) |
| Requirements were misunderstood | REJECT → return to Phase 2 (Spec) |
| Research was incomplete | REJECT → return to Phase 1 (Research) |

**Hard limit:** **3 iteration cycles maximum.** If not approved by iteration 3, escalate to a human and consider rejecting back to an earlier phase.

**Quality check:**
- Iteration history table is updated each cycle
- Only issues from the previous review are addressed (no scope creep)
- Re-verify ran and passed before re-review

**Anti-patterns:**
- Iterating forever — cap at 3
- Refactoring unrelated code while fixing
- Skipping re-verify between iterations
- Not appending to the iteration history table

---

## Phase 10 — SHIP (Delivery + Documentation)

**When:** Phase 8 returned `APPROVED`.

**Output:** `.sdd/features/NNN-feature-name/ship.md` + an entry in `.sdd/changelog.md`.

**Mode:** Agent prepares delivery artifacts. Human merges.

**Required sections:**
- **Summary** — 1–2 sentences on what shipped
- **Delivery Checklist** — tasks ✅, verify ✅, review APPROVED, commit/PR created, README updated, changelog updated, spec marked SHIPPED
- **Changes Made** — table of files (Added/Modified/Deleted)
- **Known Limitations** — anything deferred or incomplete by design
- **Lessons Learned** — what went well, what was painful, **constitution updates suggested?**

**Quality check:**
- Every checklist item is checked
- Changelog has a new dated entry
- Lessons-learned section is filled (this drives the feedback loop)

**Anti-patterns:**
- Empty lessons-learned (you lose the feedback loop)
- No changelog entry
- Shipping with a `[!]` failed task still in `tasks.md`
- Skipping the "constitution update?" question — this is how the system improves itself

---

## The Feedback Loop

Lessons from `ship.md` feed back into the constitution between features:

```
Ship → Lessons Learned
        ├─ "Pattern X worked well" → constitution Article 7 (Required)
        ├─ "Library Y caused pain" → constitution Article 6 (Forbidden)
        ├─ "Review missed bug class Z" → review-system.md domain checklist
        └─ "We always forget rule W" → constitution Article 1 (Immutable)
```

Each shipped feature should make the next feature's quality higher. That is the entire point of the system.

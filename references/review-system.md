# Review & Iteration System

## Philosophy

The review system has **two human gates** and **one automated checkpoint**:

| # | Gate | Phase | What it catches |
|---|------|-------|-----------------|
| 1 | **Plan Review** | 4 | Bad architecture, missing requirements, constitution violations — *before any code exists* |
| — | Verify | 7 | Build/test/lint/type failures, regressions |
| 2 | **Code Review** | 8 | Spec mismatches, AC failures, quality issues — *after code exists* |

The deep insight: **reviewing a 200-line markdown plan is 10x cheaper and 100x more valuable than reviewing 2,000 lines of generated code.** Catch the bad idea before the code exists. Most production failures of AI-assisted development trace back to skipping Gate #1.

---

## CORE RULE — Writer/Reviewer Separation

The agent that **writes** code MUST NOT be the same context session that **reviews** it. This rule eliminates confirmation bias. The reviewer has no attachment to the code and will surface real issues.

**How to achieve fresh-context review in Claude Code:**

1. End the implementation conversation (or use a separate Task agent).
2. Open a new conversation / new agent session.
3. Load **only** these files:
   - `.sdd/constitution.md`
   - `.sdd/features/NNN-name/spec.md`
   - `.sdd/features/NNN-name/plan.md`
   - The diff (or the changed files)
4. Do **NOT** load the implementation conversation history.
5. Ask the reviewer to produce `review.md` following the template.

If you can prove the reviewer never saw the implementation history, you have writer/reviewer separation. If you cannot, you don't.

---

## Error Classification

Every issue found during review carries a severity. Severity drives the iterate/approve/reject decision.

### 🔴 P0 — Critical (must fix before ship)
- Acceptance criterion not met
- Security vulnerability
- Data corruption risk
- Constitution Article 1 (immutable principles) violation
- Breaking change to existing functionality not flagged in plan

### 🟡 P1 — Important (should fix before ship)
- Missing error handling for plausible scenarios
- Performance regression beyond budget
- Missing tests for core logic
- Convention violation that hurts maintainability
- Incomplete implementation (works for happy path, missing edge cases)

### 🔵 P2 — Minor (fix if time permits)
- Style inconsistencies
- Missing comments / docstrings
- Naming improvements
- Non-critical test gaps
- Cosmetic UI issues

### ⚪ Observation — No action required
- Suggestions for future improvement
- Alternative approaches to consider
- Backlog items / tech debt to track

**Approval rule:** You cannot approve while any P0 is open. P1s must either be fixed or explicitly accepted by the human reviewer with a justification appended.

---

## Iteration Protocol

### Decision Tree

```
Review complete
│
├─ Only P2 / Observations? ────────► APPROVE (track P2s in backlog)
│
├─ Any open P0 or P1 issues?
│   │
│   ├─ Issues are local fixes (edge cases, error handling, gaps)
│   │     ──► ITERATE
│   │         (max 3 cycles)
│   │
│   ├─ Architecture is wrong ────► REJECT → return to Phase 3 (Plan)
│   ├─ Requirements are wrong ──► REJECT → return to Phase 2 (Spec)
│   └─ Research was incomplete ─► REJECT → return to Phase 1 (Research)
│
└─ Iteration count == 3 and still failing? ─► ESCALATE to human
```

### Iteration Cycle (Phase 9)

1. Writer agent reads `review.md` (only the open issues section)
2. Writer fixes **only** the listed issues — no scope creep
3. Re-run Phase 7 (Verify) — must pass before re-review
4. Re-run Phase 8 (Code Review) with a fresh critic context
5. Append a new iteration entry to `review.md`

### Hard Limits
- **Max 3 iterations.** After iteration 3, escalate to a human and consider rejecting back to an earlier phase.
- **No new scope.** Iterations fix listed issues only. New ideas become a follow-up feature.
- **Always re-verify before re-review.** Skipping Phase 7 between iterations is forbidden.

---

## Iteration Tracking

Each iteration appends a section to `review.md`:

```markdown
## Iteration 2 — YYYY-MM-DD

### Issues from previous review
1. 🔴 [FIXED] AC-3 not implemented — Fix: added findByEmail link in callback.ts:88
2. 🟡 [FIXED] Response envelope missing — Fix: wrapped via envelope helper
3. 🟡 [OPEN] Coverage 78% → 79% — Reason: ran out of time, P1 accepted by reviewer

### New issues found
1. 🔵 [NEW] Magic string introduced in callback.ts:91 — extract constant

### Verdict
- [ ] APPROVED
- [x] ITERATE → cycle 3/3
- [ ] REJECT
```

The iteration history table at the top of `review.md` is also updated:

```markdown
| # | Date | Issues | Fixed | Remaining |
|---|------|--------|-------|-----------|
| 1 | YYYY-MM-DD | 5 | 0 | 5 |
| 2 | YYYY-MM-DD | 1 | 4 | 2 |
| 3 | YYYY-MM-DD | 0 | 2 | 0 |
```

---

## Domain Checklists

Reviewers should run the relevant checklist for the kind of code they're reviewing. These supplement (do not replace) the AC and constitution checks.

### Backend / API
- [ ] All endpoints return the project's standard response envelope
- [ ] Error responses use appropriate HTTP status codes and machine-readable error codes
- [ ] Input validation present on every user-facing endpoint
- [ ] Auth + authorization checks present where required
- [ ] Rate limiting considered for public endpoints
- [ ] DB queries optimized (no N+1, indexes on filter columns)
- [ ] Transactions wrap multi-step mutations
- [ ] Logging at correct levels with structured fields
- [ ] No secrets logged, no PII logged

### Frontend
- [ ] Component handles all states: loading, error, empty, populated
- [ ] Accessibility: keyboard navigation, focus, ARIA, screen reader
- [ ] Responsive: mobile, tablet, desktop
- [ ] Error boundaries in place
- [ ] No memory leaks (`useEffect` cleanup, listeners removed)
- [ ] Form validation gives clear, actionable feedback
- [ ] Loading states prevent duplicate submission
- [ ] No hydration mismatches

### Database
- [ ] Migrations are reversible (or explicitly additive-only)
- [ ] Indexes exist for frequent query patterns
- [ ] Foreign key constraints in place
- [ ] No nullable columns without justification
- [ ] Sensitive data encrypted at rest
- [ ] Seed/fixture data updated if needed
- [ ] Backward-compatible for the rollout window

### Testing
- [ ] Happy path covered
- [ ] Error and edge cases covered
- [ ] Tests are independent (no shared mutable state)
- [ ] Tests are deterministic (no flakiness, no time/network reliance without mocks)
- [ ] Test names describe the behavior, not the implementation
- [ ] Mocks are minimal and justified
- [ ] Coverage meets the constitution gate

---

## Brownfield-Specific Extra Checks

For existing codebases, additionally verify:

- [ ] No regressions in existing functionality (full existing test suite passes unmodified)
- [ ] Existing tests not deleted or weakened to make new code pass
- [ ] New code follows existing patterns from `research.md` (or constitution explicitly overrides)
- [ ] Database migrations are backward-compatible for the rollout window
- [ ] API changes are backward-compatible OR properly versioned
- [ ] No orphaned/dead code left from refactoring
- [ ] Imports follow existing module boundaries

---

## The Feedback Loop → Constitution Updates

After each ship, the lessons-learned section of `ship.md` should feed back into the constitution between features:

```
Ship (Phase 10)
  └── Lessons Learned
      ├── "We keep forgetting X"  ──► Constitution Article 1 (Immutable)
      ├── "Pattern Y worked great" ──► Constitution Article 7 (Required)
      ├── "Library Z caused problems" ──► Constitution Article 6 (Forbidden)
      └── "Review missed bug class W" ──► Add check to this file's domain list
```

This makes the system self-improving: every shipped feature raises the quality floor for the next one. If you skip the lessons-learned step, you lose the entire reason for running the framework.

---

## Validator Behavior (`scripts/validate_phase.py`)

The phase validator mechanically enforces the two human gates by inspecting decision strings inside `plan-review.md` and `review.md`. It treats only one decision as a passing gate:

| Decision string | Validator verdict | What to do |
|-----------------|------------------|------------|
| `[x] ✅ APPROVED` | **PASS** — gate cleared | Proceed to next phase |
| `[x] APPROVED-WITH-CHANGES` | **FAIL** — gate not cleared | Apply the requested changes, then write a **new** review with a plain `[x] APPROVED` |
| `[ ]` (unchecked) | **FAIL** | Make the decision first |
| `[x] ❌ REJECTED` | **FAIL** | Return to the indicated upstream phase |

**Why APPROVED-WITH-CHANGES is treated as FAIL:** the gate's job is to be binary — either the plan is good enough to build, or it isn't. "Approved with changes" is really "not yet approved, fix and re-review". Forcing a clean second review keeps the audit trail honest.

**Prerequisite chains enforced by the validator:**

| Target phase | Required artifacts |
|--------------|-------------------|
| `plan` | spec |
| `plan-review` | spec, plan |
| `tasks` | spec, plan, plan-review (APPROVED) |
| `implement` | spec, plan, plan-review (APPROVED), tasks |
| `verify` | spec, plan, plan-review (APPROVED), tasks |
| `review` | spec, plan, plan-review (APPROVED), tasks, verify |
| `ship` | spec, plan, plan-review (APPROVED), tasks, verify, review (APPROVED) |

`research` is **never** in a prerequisite list — the validator is greenfield-friendly. The caller (slash command or agent) is responsible for knowing whether the project is brownfield and refusing to skip Phase 1 in that case.

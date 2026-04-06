# Review & Error Documentation System

## Philosophy

The review system has two gates and one automated checkpoint:

1. **Plan Review (Phase 4)** — Catch bad architecture BEFORE code exists
2. **Verify (Phase 7)** — Automated checks after each task
3. **Code Review (Phase 8)** — Validate implementation against spec AFTER code exists

This is based on the principle that reviewing a 200-line markdown plan is 10x faster
and 100x more valuable than reviewing 2,000 lines of generated code.

## The Writer/Reviewer Separation

Critical rule: the agent that WRITES code must NOT be the same context session
that REVIEWS it. This eliminates confirmation bias.

**Implementation:**
- Writer agent: has plan + task context, generates code
- Reviewer agent: has spec + constitution context, evaluates code
- The reviewer has no attachment to the code and will flag issues objectively

In Claude Code, achieve this by:
- Starting a fresh conversation for the review
- Loading only: spec.md, plan.md, constitution.md, and the changed files
- NOT loading the implementation conversation history

## Error Classification

All issues found during review follow a severity taxonomy:

### 🔴 Critical (P0) — Must fix before ship
- Acceptance criteria not met
- Security vulnerability
- Data corruption risk
- Constitution violation (immutable principles)
- Breaking change to existing functionality

### 🟡 Important (P1) — Should fix before ship
- Missing error handling for likely scenarios
- Performance degradation beyond acceptable bounds
- Missing tests for core logic
- Convention violations that affect maintainability
- Incomplete implementation (works but missing edge cases)

### 🔵 Minor (P2) — Fix if time permits
- Style inconsistencies
- Missing documentation/comments
- Minor naming improvements
- Non-critical test gaps
- Cosmetic issues

### ⚪ Observation — No action needed
- Suggestions for future improvement
- Alternative approaches worth considering
- Technical debt to track in backlog

## Iteration Protocol

When review finds issues:

### Iteration Decision Tree
```
Issues found?
├── Only Minor/Observations → APPROVE (fix minors in follow-up)
├── Important issues (< 5) → ITERATE
│   ├── Iteration 1: Fix issues
│   ├── Re-verify (Phase 7)
│   ├── Re-review (Phase 8)
│   └── Still has issues?
│       ├── Iteration 2: Fix remaining
│       ├── Re-verify → Re-review
│       └── Still has issues?
│           ├── Iteration 3: Final attempt
│           └── Still failing? → ESCALATE to human
│       └── Clean → APPROVE
│   └── Clean → APPROVE
├── Critical issues → ITERATE (same flow, max 3)
├── Architecture is wrong → REJECT → return to Plan (Phase 3)
├── Requirements are wrong → REJECT → return to Spec (Phase 2)
└── Research was incomplete → REJECT → return to Research (Phase 1)
```

### Iteration Tracking
Each iteration appends to review.md:

```markdown
## Iteration 2 — YYYY-MM-DD
### Issues from previous review
1. 🔴 [FIXED] Description — Fix: [what was changed]
2. 🟡 [FIXED] Description — Fix: [what was changed]
3. 🟡 [OPEN] Description — Reason: [why not fixed / needs more info]

### New issues found
1. 🔵 [NEW] Description — [introduced during fix]

### Verdict: ITERATE / APPROVE / REJECT
```

## Review Checklist by Domain

### Backend API Review
- [ ] All endpoints return consistent response envelope
- [ ] Error responses include appropriate status codes and messages
- [ ] Input validation on all user-facing endpoints
- [ ] Authentication/authorization checks present
- [ ] Rate limiting considered
- [ ] Database queries optimized (no N+1, proper indexing)
- [ ] Transactions used for multi-step mutations
- [ ] Logging at appropriate levels

### Frontend Review
- [ ] Component renders correctly in all states (loading, error, empty, data)
- [ ] Accessibility: keyboard navigation, screen reader, aria labels
- [ ] Responsive: works on mobile, tablet, desktop
- [ ] Error boundaries in place
- [ ] No memory leaks (useEffect cleanup)
- [ ] Form validation provides clear user feedback
- [ ] Loading states prevent duplicate submissions

### Database Review
- [ ] Migrations are reversible
- [ ] Indexes exist for frequent query patterns
- [ ] Foreign key constraints in place
- [ ] No nullable fields without justification
- [ ] Sensitive data encrypted at rest
- [ ] Seed data updated if needed

### Testing Review
- [ ] Happy path covered
- [ ] Error/edge cases covered
- [ ] Tests are independent (no shared mutable state)
- [ ] Tests are deterministic (no flaky behavior)
- [ ] Test names describe the behavior being tested
- [ ] Mocks are minimal and justified

## Brownfield-Specific Review

For existing codebases, additionally check:
- [ ] No regressions in existing functionality
- [ ] Existing tests still pass without modification (unless intentional)
- [ ] New code follows existing patterns (or constitution explicitly overrides them)
- [ ] Database migration is backward-compatible
- [ ] API changes are backward-compatible (or versioned)
- [ ] No orphaned code from refactoring

## The Feedback Loop

After shipping, lessons learned feed back into the constitution:

```
Ship (Phase 10)
  └── Lessons Learned
      ├── "We keep forgetting X" → Add to Constitution Article N
      ├── "Pattern Y worked great" → Add to Required Patterns
      ├── "Library Z caused problems" → Add to Forbidden Patterns
      └── "Review missed this class of bug" → Add to Review Checklist
```

This makes the system self-improving: every shipped feature makes
the next feature's quality higher.

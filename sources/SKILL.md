---
name: sdd-rpi
description: >
  Complete Spec-Driven Development + Research-Plan-Implement workflow for AI-assisted software engineering.
  Guides projects through 10 structured phases: Constitution, Research, Spec, Plan, Plan Review, Tasks,
  Implement, Verify, Code Review, and Ship. Works for both greenfield (new) and brownfield (existing) projects.
  Use this skill whenever the user mentions: SDD, RPI, spec-driven, spec first, research plan implement,
  constitution, "structured workflow", "agentic workflow", "plan before code", "no vibe coding",
  or wants to build a feature with proper planning, review gates, and quality assurance.
  Also trigger when the user wants to: start a new project with structure, add a feature to an existing codebase,
  refactor with a plan, migrate technologies, or set up engineering discipline for AI-assisted development.
  Even if the user just says "help me build X properly" or "I want to build X the right way", use this skill.
---

# SDD+RPI: Complete Spec-Driven Development Workflow

## Overview

This skill implements a 10-phase software development lifecycle optimized for AI-assisted engineering.
It combines Spec-Driven Development (SDD) with Research-Plan-Implement (RPI) methodology, adding
structured review gates, error documentation, and iteration loops.

**Core principle:** Specifications are the source of truth. Code serves specifications, not the other way around.
**Second principle:** You cannot outsource the thinking. AI amplifies thinking you've already done.
**Third principle:** Context is a scarce resource. Each phase resets context with compacted artifacts.

## Quick Start

Ask the user:
1. **Is this a new project (greenfield) or existing codebase (brownfield)?**
   - Greenfield → Skip Research phase, go straight to Constitution + Spec
   - Brownfield → Research phase is mandatory
2. **What do you want to build/change?**
3. **Do you already have a constitution/standards document?**

## Directory Structure

Create this structure at the project root:

```
.sdd/
├── constitution.md          # Phase 0: Project governance (permanent)
├── features/
│   └── NNN-feature-name/
│       ├── research.md      # Phase 1: Codebase investigation
│       ├── spec.md          # Phase 2: What to build
│       ├── plan.md          # Phase 3: How to build it
│       ├── plan-review.md   # Phase 4: Plan approval/rejection
│       ├── tasks.md         # Phase 5: Atomic work units
│       ├── verify.md        # Phase 7: Automated check results
│       ├── review.md        # Phase 8: Code review findings
│       └── ship.md          # Phase 10: Delivery checklist
└── changelog.md             # Running log of all shipped features
```

## The 10 Phases

For detailed templates of each phase, read `references/templates.md`.
For the review and error documentation system, read `references/review-system.md`.

### Phase 0: CONSTITUTION (One-time setup, permanent)

**When:** Project initialization only. Reused across all features.
**Output:** `.sdd/constitution.md`
**Mode:** Interactive — interview the user about their standards.

Ask:
- What tech stack? (language, framework, DB, infra)
- Architecture style? (monolith, microservices, DDD, clean arch, etc.)
- Testing requirements? (coverage %, TDD, types of tests)
- Code standards? (linting, formatting, naming conventions)
- Security/compliance requirements?
- Performance constraints?
- Any libraries/patterns that are FORBIDDEN?
- Any libraries/patterns that are REQUIRED?

For **brownfield projects**, also run: analyze the existing codebase to infer conventions,
then present findings to the user for confirmation before writing the constitution.

The constitution must include:
1. **Immutable Principles** — Non-negotiable rules for every change
2. **Tech Stack** — Approved technologies and versions
3. **Architecture** — Patterns, layers, boundaries
4. **Quality Gates** — What must pass before any merge
5. **Conventions** — Naming, file structure, imports, exports

### Phase 1: RESEARCH (Brownfield only — Compressing Truth)

**When:** Before every feature in existing codebases. Skip for greenfield.
**Output:** `.sdd/features/NNN-feature-name/research.md`
**Mode:** Agent investigates autonomously. No code changes. No opinions.

The agent must:
1. Identify all files relevant to the planned change
2. Document existing patterns and conventions in those areas
3. Map dependencies and potential impact zones
4. Note any technical debt or constraints
5. List specific file paths + line numbers for everything found

**Research document structure:**
- Summary (3-5 sentences max)
- Relevant Files (path + what it does + why it matters)
- Existing Patterns (how similar things are done today)
- Dependencies & Impact (what could break)
- Constraints & Risks (what to watch out for)
- Open Questions (things that need human clarification)

**Anti-patterns to avoid:**
- Research document > 2 pages for a small feature = over-research
- Research document < 5 lines for a complex migration = under-research
- Including opinions or suggestions = scope creep (save for Plan phase)

### Phase 2: SPEC (Defining What — Not How)

**When:** After Research (brownfield) or after Constitution (greenfield).
**Output:** `.sdd/features/NNN-feature-name/spec.md`
**Mode:** Collaborative — draft then iterate with user.

The spec defines WHAT to build. It must NOT contain implementation details.

**Required sections:**
1. **Problem Statement** — What problem does this solve? Why now?
2. **Goals** — What success looks like (measurable)
3. **Non-Goals** — What is explicitly OUT of scope
4. **User Stories / Scenarios** — How users interact with this
5. **Acceptance Criteria** — Testable conditions that prove it works
6. **Edge Cases** — Known boundary conditions
7. **Constraints** — Business rules, regulatory, performance

**Quality check:** Can someone implement this without asking clarifying questions?
If not, the spec isn't done.

### Phase 3: PLAN (Defining How — Technical Design)

**When:** After Spec is written.
**Output:** `.sdd/features/NNN-feature-name/plan.md`
**Mode:** Agent drafts, human reviews.

The plan transforms the spec into technical decisions, informed by the research.

**Required sections:**
1. **Architecture Approach** — How this fits into the existing system
2. **Data Model** — Entities, relationships, migrations needed
3. **API/Interface Contracts** — Endpoints, payloads, responses
4. **Implementation Phases** — Ordered steps with dependencies
5. **Testing Strategy** — Unit, integration, e2e, what to test
6. **Rollback Plan** — How to undo if things go wrong
7. **Constitution Compliance** — Checklist against constitution articles

**Pre-implementation gates (from constitution):**
- [ ] Follows approved architecture patterns
- [ ] Uses approved tech stack only
- [ ] Meets testing requirements
- [ ] Meets security requirements
- [ ] No forbidden patterns used

### Phase 4: PLAN REVIEW (Human Gate #1)

**When:** After Plan is written. BEFORE any code.
**Output:** `.sdd/features/NNN-feature-name/plan-review.md`
**Mode:** Present plan to user, document their decision.

Present to the user:
1. Summary of what will be built (from spec)
2. Summary of how it will be built (from plan)
3. Number of tasks and estimated phases
4. Any risks or open questions
5. Constitution compliance checklist

**Document the decision:**
- APPROVED → Proceed to Tasks
- APPROVED WITH CHANGES → Document changes, update plan, re-present
- REJECTED → Document reason, return to Research or Spec

This is the highest-leverage review point. Catching a bad plan here
saves hours of wasted implementation.

### Phase 5: TASKS (Atomic Decomposition)

**When:** After Plan is approved.
**Output:** `.sdd/features/NNN-feature-name/tasks.md`
**Mode:** Agent generates, user confirms.

Each task must be:
- **Independently implementable** in a single context window
- **Testable in isolation** with clear pass/fail criteria
- **Small enough** to review as a single commit/PR

**Task format:**
```markdown
## Task N: [Short Title]
- **Status:** [ ] Pending / [x] Complete / [!] Failed
- **Depends on:** Task M (if any)
- **Files to modify:** path/to/file.ts, path/to/other.ts
- **Changes:** What specifically changes
- **Verification:** How to confirm it works
  - [ ] Unit test: description
  - [ ] Integration test: description
  - [ ] Manual check: description
- **Estimated complexity:** Low / Medium / High
```

### Phase 6: IMPLEMENT (Execution with Clean Context)

**When:** After Tasks are confirmed.
**Output:** Working code + tests, task by task.
**Mode:** Agent implements each task sequentially with fresh context.

**Rules:**
1. One task at a time
2. Each task starts with: read constitution + plan + current task only
3. Write tests FIRST (TDD when possible)
4. Implement the change
5. Run verification checks
6. Update task status in tasks.md
7. Commit after each task
8. If context fills up, compact and continue from tasks.md checkboxes

### Phase 7: VERIFY (Automated Checks)

**When:** After each task is implemented (and again after all tasks complete).
**Output:** `.sdd/features/NNN-feature-name/verify.md`
**Mode:** Automated — agent runs checks and documents results.

**Verification checklist:**
- [ ] Build compiles without errors
- [ ] All existing tests pass (no regressions)
- [ ] New tests pass
- [ ] Linting passes
- [ ] Type checking passes
- [ ] No new security warnings
- [ ] Performance within acceptable bounds (if measurable)

**Format:**
```markdown
## Verification Report — Task N
- **Date:** YYYY-MM-DD
- **Build:** ✅ Pass / ❌ Fail (details)
- **Tests:** ✅ X passed, ❌ Y failed (details for failures)
- **Lint:** ✅ Pass / ⚠ N warnings, M errors
- **Types:** ✅ Pass / ❌ Fail (details)
- **Verdict:** PASS → proceed / FAIL → iterate
```

### Phase 8: CODE REVIEW (Human Gate #2 + Critic Agent)

**When:** After all tasks are implemented and verified.
**Output:** `.sdd/features/NNN-feature-name/review.md`
**Mode:** Fresh agent session reviews against spec. Then human reviews.

**The review agent (or a fresh context session) must:**
1. Read the original spec (acceptance criteria)
2. Read the plan (architecture decisions)
3. Read the constitution (quality standards)
4. Review all changed files
5. Produce a structured review document

**review.md structure:**
```markdown
# Code Review — [Feature Name]

## Acceptance Criteria Check
| Criterion | Status | Notes |
|-----------|--------|-------|
| User can... | ✅/❌ | ... |

## Constitution Compliance
| Article | Status | Notes |
|---------|--------|-------|
| Testing coverage | ✅/❌ | ... |

## Issues Found
### Critical (must fix)
1. [FILE:LINE] Description — Suggested fix

### Important (should fix)
1. [FILE:LINE] Description — Suggested fix

### Minor (nice to have)
1. [FILE:LINE] Description — Suggested fix

## Code Quality Assessment
- Readability: X/5
- Maintainability: X/5
- Test coverage: X/5
- Error handling: X/5

## Decision
- [ ] APPROVED — Ready to ship
- [ ] ITERATE — Fix issues listed above (max 3 iterations)
- [ ] REJECT — Fundamental problems, return to Plan
```

### Phase 9: ITERATE (Correction Loop)

**When:** Review found issues that need fixing.
**Output:** Updated code + updated review.md
**Mode:** Agent fixes issues, re-verifies, updates review.

**Rules:**
- Maximum 3 iteration cycles. If still failing after 3, escalate to human.
- Each iteration: fix → verify → re-review
- Only fix issues identified in review (don't refactor unrelated code)
- Update review.md with iteration history

**Decision framework:**
- Issues are cosmetic/minor → ITERATE (fix and re-verify)
- Architecture is wrong → REJECT (return to Plan phase)
- Requirements were wrong → REJECT (return to Spec phase)
- Research was incomplete → REJECT (return to Research phase)

### Phase 10: SHIP (Delivery + Documentation)

**When:** Review is approved.
**Output:** `.sdd/features/NNN-feature-name/ship.md` + updated changelog
**Mode:** Agent prepares delivery artifacts.

**Delivery checklist:**
- [ ] All tasks complete in tasks.md
- [ ] All verifications pass in verify.md
- [ ] Review approved in review.md
- [ ] PR/commit created with descriptive message
- [ ] README updated (if needed)
- [ ] Changelog updated in `.sdd/changelog.md`
- [ ] Spec archived (mark as SHIPPED with date)

**ship.md contents:**
- Date shipped
- Summary of what was delivered
- Link to PR/commits
- Any known limitations or follow-ups
- Lessons learned (what went well, what to improve)

## Slash Commands Reference

When used with Claude Code, suggest these as slash commands:

| Command | Phase | Description |
|---------|-------|-------------|
| `/sdd-init` | 0 | Initialize project with constitution |
| `/sdd-research` | 1 | Research codebase for a feature |
| `/sdd-spec` | 2 | Create feature specification |
| `/sdd-plan` | 3 | Create technical plan |
| `/sdd-review-plan` | 4 | Review and approve plan |
| `/sdd-tasks` | 5 | Decompose plan into tasks |
| `/sdd-implement` | 6 | Implement tasks one by one |
| `/sdd-verify` | 7 | Run verification checks |
| `/sdd-review-code` | 8 | Review implementation against spec |
| `/sdd-ship` | 10 | Prepare delivery artifacts |
| `/sdd-status` | * | Show current progress |

## Important Notes

- **Never skip phases.** Each phase produces artifacts the next phase needs.
- **Context resets between phases.** Each phase should start with a fresh context
  loading only the artifacts from previous phases, not the full conversation history.
- **The human approves at two gates:** Plan Review (Phase 4) and Code Review (Phase 8).
- **Constitution is permanent.** It doesn't change per feature. Update it only through
  a deliberate process, not during feature development.
- **Brownfield vs Greenfield:** The only difference is Phase 1 (Research). Everything
  else applies equally.

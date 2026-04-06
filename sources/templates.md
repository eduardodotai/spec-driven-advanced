# SDD+RPI Templates Reference

## Constitution Template

```markdown
# Project Constitution — [Project Name]
> Last updated: YYYY-MM-DD | Version: 1.0

## Article 1: Immutable Principles
- [e.g., All code must have tests before merge]
- [e.g., No direct database access from UI layer]
- [e.g., All API endpoints require authentication]

## Article 2: Tech Stack
- **Language:** [e.g., TypeScript 5.x, strict mode]
- **Runtime:** [e.g., Node.js 22 LTS]
- **Framework:** [e.g., Next.js 15 App Router]
- **Database:** [e.g., PostgreSQL 16 + Prisma ORM]
- **Testing:** [e.g., Vitest + Playwright]
- **CI/CD:** [e.g., GitHub Actions]

## Article 3: Architecture
- **Style:** [e.g., Clean Architecture with DDD]
- **Layers:** [e.g., Presentation → Application → Domain → Infrastructure]
- **State management:** [e.g., Server state via React Query, local via Zustand]
- **API style:** [e.g., REST with OpenAPI spec]

## Article 4: Quality Gates
- Minimum test coverage: [e.g., 80%]
- All linting rules must pass
- No TypeScript `any` without documented justification
- PR requires at least 1 human review
- Performance budget: [e.g., LCP < 2.5s, FID < 100ms]

## Article 5: Conventions
- **File naming:** [e.g., kebab-case for files, PascalCase for components]
- **Folder structure:** [e.g., feature-based co-location]
- **Imports:** [e.g., absolute paths via @/ alias]
- **Error handling:** [e.g., Result pattern, no throwing in domain layer]
- **Logging:** [e.g., structured JSON via pino]

## Article 6: Forbidden Patterns
- [e.g., No global mutable state]
- [e.g., No CSS-in-JS (use Tailwind only)]
- [e.g., No circular dependencies between modules]

## Article 7: Required Patterns
- [e.g., All API responses follow {data, error, meta} envelope]
- [e.g., All DB queries go through repository pattern]
- [e.g., All user input validated with Zod schemas]

## Article 8: Security
- [e.g., OWASP Top 10 compliance]
- [e.g., All secrets in environment variables]
- [e.g., SQL injection prevention via parameterized queries]

## Article 9: Documentation
- [e.g., All public functions have JSDoc]
- [e.g., All API endpoints documented in OpenAPI]
- [e.g., Architecture Decision Records for major changes]
```

---

## Research Template

```markdown
# Research — [Feature Name]
> Date: YYYY-MM-DD | Feature: NNN-feature-name | Status: Complete

## Summary
[3-5 sentences describing what was found. No opinions, only facts.]

## Relevant Files
| File | Purpose | Relevance |
|------|---------|-----------|
| `src/modules/auth/login.ts` | Handles login flow | Will need modification for SSO |
| `src/shared/types/user.ts` | User type definitions | Must extend for new fields |

## Existing Patterns
- **Authentication:** Currently uses JWT with refresh tokens (see `src/middleware/auth.ts:42`)
- **Data access:** Repository pattern via `src/repositories/base.repository.ts`
- **Error handling:** Custom AppError class at `src/shared/errors.ts:15`

## Dependencies & Impact
- Changing `User` type affects: login, profile, settings, admin panel
- Database migration needed: adding `sso_provider` column to users table
- API v2 consumers may need notification

## Constraints & Risks
- Current session store cannot handle multiple auth providers simultaneously
- Rate limiting on third-party SSO callback must be considered
- Migration must be backward-compatible (existing users must not be affected)

## Open Questions
1. Which SSO providers should be supported initially?
2. Should existing password users be forced to link SSO?
3. What is the expected load increase from SSO adoption?
```

---

## Spec Template

```markdown
# Specification — [Feature Name]
> Date: YYYY-MM-DD | Feature: NNN-feature-name | Status: Draft/Approved

## Problem Statement
[What problem does this solve? Who has this problem? Why solve it now?]

## Goals
1. [Measurable goal — e.g., "Users can log in via Google SSO in under 3 seconds"]
2. [Measurable goal]

## Non-Goals
1. [Explicitly excluded — e.g., "Apple SSO support is out of scope for this iteration"]
2. [Explicitly excluded]

## User Stories
- **As a** [role], **I want to** [action], **so that** [benefit]
- **As a** [role], **I want to** [action], **so that** [benefit]

## Acceptance Criteria
- [ ] AC-1: [Testable condition — e.g., "User can click 'Sign in with Google' and complete auth flow"]
- [ ] AC-2: [Testable condition]
- [ ] AC-3: [Testable condition]

## Edge Cases
| Scenario | Expected Behavior |
|----------|-------------------|
| User cancels SSO midway | Return to login page, show message |
| SSO email matches existing account | Link accounts, notify user |
| SSO provider is down | Show fallback to password login |

## Constraints
- Must work on mobile browsers (iOS Safari, Chrome Android)
- Response time < 3 seconds for auth callback
- Must comply with GDPR for data from SSO provider
```

---

## Plan Template

```markdown
# Technical Plan — [Feature Name]
> Date: YYYY-MM-DD | Feature: NNN-feature-name | Status: Draft/Approved
> Spec: spec.md | Research: research.md

## Architecture Approach
[How this fits into the existing system. Include a diagram if helpful.]

## Data Model Changes
[New entities, modified fields, migrations.]

## API / Interface Contracts
[New endpoints, changed signatures, request/response schemas.]

## Implementation Phases
### Phase 1: [Name] (e.g., Database & Types)
- What changes
- Dependencies: none

### Phase 2: [Name] (e.g., Backend Logic)
- What changes
- Dependencies: Phase 1

### Phase 3: [Name] (e.g., Frontend Integration)
- What changes
- Dependencies: Phase 2

## Testing Strategy
- **Unit tests:** [what to test at unit level]
- **Integration tests:** [what to test across boundaries]
- **E2E tests:** [critical user flows to test end-to-end]

## Rollback Plan
1. [How to revert if things go wrong]
2. [Data migration rollback steps]

## Constitution Compliance
- [ ] Art 1 (Immutable Principles): compliant
- [ ] Art 2 (Tech Stack): uses approved stack
- [ ] Art 3 (Architecture): follows approved patterns
- [ ] Art 4 (Quality Gates): testing strategy meets requirements
- [ ] Art 5 (Conventions): follows naming/structure conventions
- [ ] Art 6 (Forbidden Patterns): no violations
- [ ] Art 7 (Required Patterns): all required patterns used
- [ ] Art 8 (Security): security requirements met
```

---

## Review Template

```markdown
# Code Review — [Feature Name]
> Date: YYYY-MM-DD | Feature: NNN-feature-name
> Reviewer: [Agent/Human] | Iteration: 1/3

## Acceptance Criteria Validation
| ID | Criterion | Status | Evidence |
|----|-----------|--------|----------|
| AC-1 | [from spec] | ✅/❌ | [file:line or test name] |
| AC-2 | [from spec] | ✅/❌ | [file:line or test name] |

## Constitution Compliance
| Article | Status | Notes |
|---------|--------|-------|
| Art 1: Immutable Principles | ✅/❌ | |
| Art 2: Tech Stack | ✅/❌ | |
| Art 3: Architecture | ✅/❌ | |
| Art 4: Quality Gates | ✅/❌ | |
| Art 5: Conventions | ✅/❌ | |
| Art 6: Forbidden Patterns | ✅/❌ | |
| Art 7: Required Patterns | ✅/❌ | |
| Art 8: Security | ✅/❌ | |

## Issues Found

### 🔴 Critical (must fix before ship)
1. **[FILE:LINE]** Description
   - **Impact:** [what breaks]
   - **Fix:** [suggested fix]

### 🟡 Important (should fix)
1. **[FILE:LINE]** Description
   - **Impact:** [what could go wrong]
   - **Fix:** [suggested fix]

### 🔵 Minor (nice to have)
1. **[FILE:LINE]** Description
   - **Fix:** [suggested fix]

## Quality Scores
| Dimension | Score | Notes |
|-----------|-------|-------|
| Readability | X/5 | |
| Maintainability | X/5 | |
| Test Coverage | X/5 | |
| Error Handling | X/5 | |
| Performance | X/5 | |

## Iteration History
| # | Date | Issues | Fixed | Remaining |
|---|------|--------|-------|-----------|
| 1 | YYYY-MM-DD | N | - | N |

## Decision
- [ ] ✅ APPROVED — Ready to ship
- [ ] 🔄 ITERATE — Fix critical/important issues (iteration N+1)
- [ ] ❌ REJECT — Return to [Research/Spec/Plan] (reason: ___)
```

---

## Ship Template

```markdown
# Ship Report — [Feature Name]
> Date: YYYY-MM-DD | Feature: NNN-feature-name

## Summary
[1-2 sentences: what was delivered]

## Delivery Checklist
- [ ] All tasks complete (tasks.md)
- [ ] All verifications pass (verify.md)
- [ ] Code review approved (review.md)
- [ ] Commit/PR created
- [ ] README updated
- [ ] Changelog updated
- [ ] Spec marked as SHIPPED

## Changes Made
| File | Change Type | Description |
|------|-------------|-------------|
| path/to/file | Added/Modified/Deleted | Brief description |

## Known Limitations
- [Any shortcuts taken or follow-ups needed]

## Lessons Learned
- **Went well:** [what worked in this cycle]
- **Improve next time:** [what was painful or slow]
- **Constitution update needed?** [any new rules to add based on learnings]
```

---

## Status Dashboard Template

```markdown
# SDD Status — [Project Name]
> Last updated: YYYY-MM-DD

## Active Features
| # | Feature | Phase | Progress | Blocker |
|---|---------|-------|----------|---------|
| 001 | [name] | Implement | ▓▓▓▓▓░ 60% | None |
| 002 | [name] | Plan Review | ▓▓▓▓░░ 40% | Awaiting approval |

## Phase Progress Key
| Phase | % |
|-------|---|
| Constitution | 0% (permanent) |
| Research | 10% |
| Spec | 20% |
| Plan | 30% |
| Plan Review | 40% |
| Tasks | 50% |
| Implement | 60% |
| Verify | 70% |
| Code Review | 80% |
| Iterate | 85% |
| Ship | 100% |

## Recently Shipped
| # | Feature | Date | Review Score |
|---|---------|------|-------------|
| ... | ... | ... | .../5 |
```

# Phase -1 — PRODUCT VISION

> **Added in v1.2.0.** This phase exists *before* the Constitution. It captures the high-level product story so that every downstream phase has the "why" and the "for whom" available without re-litigating it.

## When

- **Greenfield projects:** mandatory before Phase 0. The agent cannot make sensible Constitution choices without knowing what product is being built.
- **Brownfield projects:** optional but recommended. If the project has been around for a while and there is no written product vision, run this phase once to reverse-engineer it from the codebase + product owner interview.

## Output

`.sdd/product-vision.md`

## Mode

**Multilingual interactive interview.** The agent asks the user **which language they want to use for the interview** (English as default), then adapts every question to that language. The final document is **always written in English**, regardless of the interview language. This is a deliberate split:

- **Questions in the user's chosen language** → low cognitive load, the user thinks naturally
- **Document in EN** → maximum reach for code comments, future contributors, AI agents that work better in English

### Language-selection protocol (Q0 — asked before any other question)

The agent's first message in `/sdd-vision` is **always in English**:

> "Which language would you like to use for this interview? (English / Português / Español / Français / Italiano / Deutsch / … — I'll adapt. The final `product-vision.md` will always be written in English.)"

Rules:

| User response | Agent behavior |
|---|---|
| Clear language ("Português", "Spanish", "fr") | Switch to that language for all subsequent questions |
| "default" / silence / skip | Use **English** |
| Language the agent cannot confidently handle | Offer English or the closest supported one |
| Mid-interview switch ("can we continue in English?") | Switch immediately, preserve all answers |

The agent records the chosen language in the output document's frontmatter as `interview_language: <code>` for auditability. Example:

```yaml
---
interview_language: pt-BR
document_language: en
---
```

## Required sections

| # | Section | Purpose |
|---|---------|---------|
| 1 | Overview | One paragraph: what the product is and its core purpose |
| 2 | Problem Statement | What problem, who has it, why solve it now |
| 3 | Goals | 3–5 measurable outcomes |
| 4 | Target Users | Table of role / description / capabilities |
| 5 | Core Capabilities | 5–10 high-level features the product enables |
| 6 | Technical Considerations | Auth, privacy, scale, regulatory, performance |
| 7 | Tech Stack Preference | Backend, frontend, DB, infra (high-level only — versions go in Constitution) |
| 8 | Out of Scope | At least 3 things the product explicitly does NOT do |
| 9 | Success Metrics | How we know the product is achieving its goals |

## Quality check

- A stranger can read this document and understand what the product is in under 5 minutes
- Goals are measurable (numbers, not adjectives)
- At least 3 explicit out-of-scope items
- Tech stack has at least language + framework
- The Constitution that follows can directly reference this file

## Anti-patterns

| Anti-pattern | Why it fails | Correct move |
|--------------|--------------|--------------|
| Vision contains feature-level details | Couples product with implementation | Move details to feature `spec.md` |
| Vision changes per feature | Vision is supposed to be stable | Update only between major pivots, with version bump |
| Skipping it because "the team knows the product" | Agents do not "know" — they need text | Always write it down |
| Vague goals ("make it good", "be fast") | Not measurable | Use numbers: "p95 latency < 200ms", "10k users" |
| Missing Out of Scope section | Scope creeps invisibly | List 3+ explicit non-goals |

---

## Canonical question bank (EN)

The agent runs this interview interactively in the user's chosen language. The canonical questions below are in **English** — the agent translates them on the fly to the selected language while preserving meaning, and always maps answers back to the same structured document sections.

### Block 1 — Problem & Vision

1. **"Let's start with the problem: what problem do you want to solve, and who feels it today?"**
   → Maps to: Problem Statement

2. **"How is this problem solved today? Are there alternatives? If so, why aren't they good enough?"**
   → Maps to: Problem Statement (context)

3. **"In one sentence: what does this product do?"**
   → Maps to: Overview (1-line elevator pitch)

4. **"Why now? What changed in the world (or in your life) that makes this the right moment to build it?"**
   → Maps to: Problem Statement (urgency)

### Block 2 — Goals & Success

5. **"What are the 3 to 5 main goals of this product? Try to use numbers when possible (e.g., 'reduce time X by 50%', '1000 users in the first month')."**
   → Maps to: Goals

6. **"Six months from now, how will we know this product is succeeding? What would we be measuring?"**
   → Maps to: Success Metrics

### Block 3 — Users

7. **"Who will use this? List the user types (can be 1, 2, 3...). For each type, tell me: what do they need to do in the product?"**
   → Maps to: Target Users (table)

### Block 4 — Capabilities

8. **"What are the 5 to 10 core capabilities of the product? Think in verbs: 'create account', 'send message', 'generate report', 'pay', 'search', etc."**
   → Maps to: Core Capabilities

### Block 5 — Technical Constraints

9. **"Are there any important technical constraints? For example: does it need to work offline? Does it handle sensitive data (health, financial)? What scale do you expect (10, 1000, 100k users)? Any compliance requirements (GDPR, HIPAA, LGPD)?"**
   → Maps to: Technical Considerations

10. **"What's your stack preference? Language, framework, database. If you're unsure or want my suggestion, tell me the product type (web, mobile, CLI, API) and I'll suggest a stack based on best practices."**
    → Maps to: Tech Stack Preference

### Block 6 — Limits

11. **"What does this product explicitly NOT do? List at least 3 things that are out of scope. This is as important as what it does — it prevents scope creep."**
    → Maps to: Out of Scope

### Final block — Confirmation

12. **"Before I write the document: anything important I didn't ask about? Any context, any decisions already made, any analogies ('it's like X but for Y')?"**
    → Free-form: agent incorporates into Overview / Problem Statement

---

## Illustrative translation — PT-BR

For reference, here is how Block 1 question 1 looks when the user selects Portuguese. The agent adapts all 12 questions the same way:

> **"Vamos começar pelo problema: que problema você quer resolver, e pra quem ele dói hoje?"**

Other example renderings of the same question:

| Language | Rendering |
|---|---|
| English (default) | "Let's start with the problem: what problem do you want to solve, and who feels it today?" |
| Português | "Vamos começar pelo problema: que problema você quer resolver, e pra quem ele dói hoje?" |
| Español | "Empecemos por el problema: ¿qué problema quieres resolver, y a quién le duele hoy?" |
| Français | "Commençons par le problème : quel problème veux-tu résoudre, et qui en souffre aujourd'hui ?" |
| Italiano | "Iniziamo dal problema: quale problema vuoi risolvere, e chi ne soffre oggi?" |
| Deutsch | "Fangen wir mit dem Problem an: Welches Problem willst du lösen, und wer hat es heute?" |

The agent is responsible for idiomatic, not literal, translations. The goal is **low cognitive load** for the user, not textbook accuracy.

---

## Output protocol

After the interview, the agent:

1. Synthesizes answers into the EN template (see `templates.md`)
2. Writes the file to `.sdd/product-vision.md`
3. Shows the document to the user with a confirmation message **in the chosen interview language** (e.g., EN: *"Here is your product vision. Read it and tell me if you want to change anything before I run `/sdd-init`."*; PT-BR: *"Aqui está sua product vision. Lê e me diz se quer mudar alguma coisa antes de eu rodar o `/sdd-init`."*)
4. If user wants edits, iterate until approved
5. Marks the file as `Status: Approved` in frontmatter
6. **Suggests** running `/sdd-init` next (does NOT auto-run it)

## How the Constitution uses this

When `/sdd-init` runs after Vision:

- The agent reads `.sdd/product-vision.md` first
- Many Constitution questions become **suggestions instead of open questions** because the Vision already implied the answer (e.g., if Vision says "web app, Next.js preference", Constitution Article 2 is pre-filled)
- The Constitution gets a header line: `> Product vision: ./product-vision.md` so any future feature spec can find it

## How feature Specs use this

Every `/sdd-spec <feature>` automatically loads `.sdd/product-vision.md` into context before the spec interview. This ensures features stay aligned with the product story instead of drifting into "cool ideas the team had this week".

## Reverse engineering for brownfield

If brownfield and no Vision exists, run a hybrid: agent investigates the codebase (similar to Phase 1 Research, but at product level — README, package.json, top-level routes, main models) and **proposes** a draft Vision. User edits and approves. This is faster than asking 12 questions cold.

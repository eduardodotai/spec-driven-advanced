# Phase -1 — PRODUCT VISION

> **Added in v1.2.0.** This phase exists *before* the Constitution. It captures the high-level product story so that every downstream phase has the "why" and the "for whom" available without re-litigating it.

## When

- **Greenfield projects:** mandatory before Phase 0. The agent cannot make sensible Constitution choices without knowing what product is being built.
- **Brownfield projects:** optional but recommended. If the project has been around for a while and there is no written product vision, run this phase once to reverse-engineer it from the codebase + product owner interview.

## Output

`.sdd/product-vision.md`

## Mode

**Bilingual interactive interview.** The agent asks questions in the user's native language (Portuguese by default for this user) but writes the document in English. This is a deliberate split:

- **Questions in PT-BR** → low cognitive load, the user thinks naturally
- **Document in EN** → maximum reach for code comments, future contributors, AI agents that work better in English

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

## Bilingual question bank (PT-BR → EN doc)

The agent runs this interview interactively. Questions are asked in PT-BR; answers are translated and structured into the EN document at the end.

### Bloco 1 — Problema e Visão

1. **"Vamos começar pelo problema: que problema você quer resolver, e pra quem ele dói hoje?"**
   → Maps to: Problem Statement

2. **"Como esse problema é resolvido hoje? Existe alguma alternativa? Se sim, por que ela não é boa o suficiente?"**
   → Maps to: Problem Statement (context)

3. **"Em uma frase só, o que esse produto faz?"**
   → Maps to: Overview (1-line elevator pitch)

4. **"Por que agora? O que mudou no mundo (ou na sua vida) que faz esse o momento certo pra construir isso?"**
   → Maps to: Problem Statement (urgency)

### Bloco 2 — Objetivos e Sucesso

5. **"Quais são os 3 a 5 objetivos principais desse produto? Tenta usar números quando der (ex: 'reduzir o tempo de X em 50%', '1000 usuários no primeiro mês')."**
   → Maps to: Goals

6. **"Daqui a 6 meses, como vamos saber se esse produto está dando certo? O que estaríamos medindo?"**
   → Maps to: Success Metrics

### Bloco 3 — Usuários

7. **"Quem vai usar isso? Liste os tipos de usuário (pode ser 1, 2, 3...). Pra cada tipo, me diz: o que ele precisa fazer no produto?"**
   → Maps to: Target Users (table)

### Bloco 4 — Capacidades

8. **"Quais são as 5 a 10 capacidades centrais do produto? Pensa em verbos: 'criar conta', 'enviar mensagem', 'gerar relatório', 'pagar', 'buscar', etc."**
   → Maps to: Core Capabilities

### Bloco 5 — Restrições Técnicas

9. **"Tem alguma restrição técnica importante? Por exemplo: precisa funcionar offline? Lida com dados sensíveis (saúde, financeiro)? Espera quanto de escala (10, 1000, 100k usuários)? Tem requisito de compliance (LGPD, GDPR, HIPAA)?"**
   → Maps to: Technical Considerations

10. **"Qual sua preferência de stack? Linguagem, framework, banco. Se você não tem ideia ou quer minha sugestão, me diz o tipo de produto (web, mobile, CLI, API) e eu sugiro um stack baseado nas melhores práticas."**
    → Maps to: Tech Stack Preference

### Bloco 6 — Limites

11. **"O que esse produto explicitamente NÃO faz? Liste pelo menos 3 coisas que estão fora do escopo. Isso é tão importante quanto o que ele faz — evita que o escopo cresça sem controle."**
    → Maps to: Out of Scope

### Bloco final — Confirmação

12. **"Antes de eu escrever o documento: alguma coisa importante que eu não perguntei? Algum contexto, alguma decisão já tomada, alguma analogia ('é tipo o X mas pra Y')?"**
    → Free-form: agent incorporates into Overview / Problem Statement

---

## Output protocol

After the interview, the agent:

1. Synthesizes answers into the EN template (see `templates.md`)
2. Writes the file to `.sdd/product-vision.md`
3. Shows the document to the user with **"Aqui está sua product vision. Lê e me diz se quer mudar alguma coisa antes de eu rodar o `/sdd-init`."**
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

# Guided Mode — Accessibility Layer for Non-Engineers

> **Added in v1.2.0.** This file is the deep reference for the optional `--guided` flag that makes the skill usable by non-technical users (or by engineers who want lower-friction interviews on side projects).

> **Multilingual (v1.2.1+):** the agent picks up the user's chosen interview language (set in Phase -1 via `/sdd-vision` or asked at the start of any interactive phase). The PT-BR examples in the tables below are **illustrative** — the agent translates jargon questions on the fly to whichever language the user selected. Smart defaults, auto-detection, and the "In plain English" banner all adapt to the chosen language. The output artifacts are always written in English.

## What it does

Guided mode does **not** change the workflow. The 10 phases, the two human gates, the writer/reviewer separation — all of it stays identical. What changes is **how the agent talks to you** during interactive phases.

| Without `--guided` | With `--guided` |
|---|---|
| "What's your error handling strategy? (Result pattern, exceptions, ...)" | "Como o sistema deve reagir quando algo dá errado? (mostrar mensagem amigável, tentar de novo automaticamente, ...)" |
| Asks every Constitution question cold | Infers defaults from product type, asks only what cannot be inferred |
| Demands testable Acceptance Criteria | "Me dá 3 exemplos do que o usuário deveria conseguir fazer" — agent translates to ACs |
| Refuses vague answers | Accepts vague answers, fills gaps with sensible defaults, shows what was inferred for confirmation |
| Output uses jargon ("OWASP Top 10", "N+1 queries") | Output uses jargon BUT a "Plain English summary" appears at the top of each artifact |

## When to activate

| Situation | Use guided mode? |
|---|---|
| User is a product owner / non-engineer | ✅ Yes |
| User is an engineer on a personal side project | ✅ Optional — lower friction |
| User is an engineer on a serious project | ❌ Default mode is fine |
| User explicitly asks "modo guiado" / "guided mode" / "easier" | ✅ Yes |
| User gives vague answers to 2+ questions in a row | ✅ Auto-detect — agent should switch and confirm |
| Production code, regulated industry | ❌ Default mode (full rigor) |

## How to activate

Three ways:

1. **Slash command flag:** `/sdd-init --guided` or `/sdd-spec auth --guided` or `/sdd-plan auth --guided`
2. **Persistent project flag:** add `guided_mode: true` to `.sdd/constitution.md` frontmatter — applies to every phase
3. **Auto-detection:** if the agent detects 2+ vague answers, it asks: *"Quer que eu mude pro modo guiado? Faço perguntas mais simples e preencho os defaults técnicos por você."*

Once activated, guided mode persists for the current phase. To exit, the user types "modo normal" / "exit guided".

---

## Jargon translation table (Phase 0 — Constitution)

| Technical question | Guided question (PT-BR) | Default if skipped |
|---|---|---|
| Architecture pattern (DDD, Clean, MVC...)? | "Como o código vai ficar organizado? Se não souber, eu sugiro um padrão baseado no tipo do produto." | Feature-based co-location for small projects, layered architecture for medium+ |
| Test coverage minimum? | "Quanto do código tem que ter teste automatizado? Padrão é 70%, posso ajustar pra mais ou menos." | 70% |
| Error handling strategy (Result, exceptions, ...)? | "Como o sistema deve reagir quando algo dá errado? (mostrar mensagem amigável e logar, ou parar tudo e gritar?)" | Result pattern in domain layer; user-friendly errors at UI |
| Forbidden patterns? | "Tem alguma coisa que você NÃO quer ver no código? (ex: 'sem variáveis globais', 'sem jQuery'). Pode pular se não souber." | None — leave empty |
| Required patterns? | "Tem alguma coisa que sempre tem que estar lá? (ex: 'todo input deve ser validado'). Pode pular." | Input validation at every system boundary |
| OWASP Top 10 compliance? | "Boas práticas de segurança contra os ataques mais comuns na web. Eu cuido disso por padrão." | Yes — auto-applied |
| Logging strategy (structured JSON, plain text)? | "Como vamos guardar os 'logs' (registros do que aconteceu) pra debugar depois? Eu sugiro um padrão." | Structured JSON with severity levels |
| State management (Zustand, Redux, ...)? | "Como o frontend vai lembrar das coisas entre telas? Eu escolho baseado no tamanho do produto." | React Query for server state, Zustand for local — small/medium; Redux Toolkit only if explicitly needed |
| Imports style (absolute, relative)? | "Pequenos detalhes de organização — eu uso o padrão do framework escolhido." | Absolute imports via path alias (@/) |

## Jargon translation table (Phase 2 — Spec)

| Technical question | Guided question (PT-BR) | What guided mode does |
|---|---|---|
| Acceptance Criteria (testable, numbered) | "Como vamos saber que isso está funcionando? Me dá 3 exemplos do que o usuário deveria conseguir fazer no fim." | Translates each example into a numbered AC, shows back to user for confirmation |
| Non-Goals | "O que esse trabalho NÃO vai resolver dessa vez? Liste 3 coisas. Isso evita o escopo crescer." | Lists as bullets |
| Edge Cases | "O que pode dar errado? Tipo: o que acontece se a internet cair, se o usuário cancelar no meio, se o servidor estiver fora?" | Each scenario becomes an edge case row |
| User Stories ("As a... I want to... so that...") | "Quem vai usar isso, o que ele quer fazer, e por que isso ajuda ele?" | Auto-formats into the user story template |
| Constraints (regulatory, performance budgets) | "Tem alguma regra que esse produto precisa seguir? Tipo lei de proteção de dados, velocidade mínima?" | Lists or marks "none specified" |

## Jargon translation table (Phase 3 — Plan)

| Technical question | Guided question (PT-BR) | What guided mode does |
|---|---|---|
| Data model entities | "Que tipos de informação o sistema precisa guardar? (ex: usuário, pedido, mensagem)" | Generates entity tables with fields inferred from capabilities |
| API contracts | "Quais ações o usuário pode fazer? Pra cada uma, o que ele manda e o que recebe de volta?" | Generates endpoint specs with request/response shapes |
| Architecture diagram | "Como as partes do sistema se conversam? Eu desenho um diagrama simples e você confirma." | Auto-generates a Mermaid diagram |
| Implementation phases (ordered with deps) | "Em que ordem a gente faz isso? Eu proponho uma ordem que minimiza risco." | Auto-orders by dependencies, shows the user |
| Testing strategy (unit/integration/e2e per layer) | "Que tipo de teste vamos escrever? Eu proponho o mínimo necessário pra cada parte." | Defaults: unit for logic, integration for API, e2e for critical user flows |
| Rollback plan | "Se essa mudança quebrar alguma coisa, como a gente desfaz? Eu proponho um plano e você confirma." | Auto-generates: revert commit + DB migration rollback |
| Constitution Compliance checklist | (hidden in guided mode — auto-runs and only surfaces violations) | Silent unless something fails |

---

## Smart defaults by product type

When user mentions a product type, guided mode pre-fills these defaults instead of asking:

### Web app (SaaS, dashboard, internal tool)

```yaml
language: TypeScript 5.x strict
framework: Next.js 15 App Router
database: PostgreSQL 16 + Prisma
styling: Tailwind CSS 4
auth: NextAuth (or Clerk for SaaS)
deployment: Vercel
testing: Vitest (unit) + Playwright (e2e)
state: React Query + Zustand
api: REST with OpenAPI
```

### Mobile app

```yaml
framework: React Native + Expo
language: TypeScript 5.x strict
state: React Query + Zustand
backend: separate (use the Web app stack or specify)
testing: Jest + Detox
```

### CLI tool

```yaml
language: Python 3.12 OR TypeScript (Bun)
testing: pytest OR vitest
distribution: pipx OR npm
```

### API / Backend service

```yaml
language: TypeScript (Hono or Fastify) OR Python (FastAPI)
database: PostgreSQL + Prisma OR SQLAlchemy
auth: JWT
testing: integration-first
deployment: Railway / Fly.io / Render
```

### Quick prototype / hackathon

```yaml
framework: Next.js + Vercel
database: SQLite (turso) OR Postgres (Neon free tier)
auth: skip or Clerk
quality_gates: relaxed (50% coverage minimum)
```

The user can override any default. If they accept defaults, the Constitution interview goes from ~12 questions to ~3.

---

## How auto-detection works

The agent counts vague answers in the current phase. A "vague answer" is one of:

- "Não sei" / "I don't know"
- "Tanto faz" / "Whatever"
- "O que você acha melhor" / "Whatever you think is best"
- A question asked back ("o que isso significa?")
- An empty answer
- Three+ words of context that does not actually answer the question

After **2 vague answers in the same phase**, the agent pauses and asks:

> "Notei que você não está certo de algumas respostas técnicas — isso é normal! Quer que eu mude pro **modo guiado**? Eu faço perguntas mais simples, em linguagem do dia a dia, e preencho os defaults técnicos baseado no tipo do produto. Você sempre pode revisar antes de eu salvar."

If yes → switch and re-ask the current question in guided form. If no → continue in default mode.

---

## What guided mode does NOT change

- The 10 phases still happen in order
- The two human gates (Phase 4 and Phase 8) still require explicit human approval — guided mode does not auto-approve them
- The validator (`scripts/validate_phase.py`) still enforces every prerequisite
- Writer/reviewer separation in Phase 8 still applies
- The artifact files (`spec.md`, `plan.md`, etc.) are still written in English with full technical content
- Quality bars are still applied — guided mode just makes the *path to meeting them* friendlier

In other words: guided mode lowers the cognitive load of the interview, not the rigor of the output. A guided-mode `spec.md` is indistinguishable from a default-mode `spec.md` — only the conversation that produced it was different.

---

## Plain English summary banner

When guided mode is active, every artifact gets a "Plain English Summary" callout at the top:

```markdown
> **In plain English:** This feature lets logged-in users export their data as a CSV file. It works for free and paid users, only for data they own, and is rate-limited to prevent abuse.
```

This makes artifacts approachable for non-technical stakeholders reviewing the work without needing to read 200 lines of structured spec.

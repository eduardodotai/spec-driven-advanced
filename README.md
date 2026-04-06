# spec-driven-advanced

> A Claude Code skill that implements the complete **10-phase SDD + RPI** workflow — Spec-Driven Development combined with Research, Plan, Implement.

**No vibe coding. Plan before code. Specs are the source of truth.**

---

🇬🇧 **English** · [🇧🇷 Português](#-português)

---

## What is this?

`spec-driven-advanced` is a Claude Code skill that turns AI-assisted software engineering into a disciplined, 10-phase workflow with two human review gates and an automated verification checkpoint. It works for both new projects (greenfield) and existing codebases (brownfield).

It combines two methodologies:

- **SDD (Spec-Driven Development)** — specifications are the source of truth, code is derived
- **RPI (Research, Plan, Implement)** — pioneered by Dex Horthy at HumanLayer; each phase resets context to stay outside the "Dumb Zone" where LLM performance collapses

The skill enforces the **writer/reviewer separation rule**: the agent that writes code is never the same context that reviews it. This eliminates confirmation bias and is the single biggest quality lever in AI-assisted development.

## The 10 phases

| # | Phase | When | Output | Gate |
|---|-------|------|--------|------|
| 0 | Constitution | Once per project | `constitution.md` | — |
| 1 | Research | Brownfield only | `research.md` | — |
| 2 | Spec | Every feature | `spec.md` | — |
| 3 | Plan | Every feature | `plan.md` | — |
| 4 | **Plan Review** | After Plan | `plan-review.md` | **Human Gate #1** |
| 5 | Tasks | After Plan approved | `tasks.md` | — |
| 6 | Implement | One task at a time | code + tests | — |
| 7 | Verify | After each task | `verify.md` | Automated |
| 8 | **Code Review** | After Verify passes | `review.md` | **Human Gate #2** |
| 9 | Iterate | If Review fails | updated code | Max 3 cycles |
| 10 | Ship | After Review approved | `ship.md` + changelog | — |

## Why this exists

When "vibe coding" with AI agents collapses on real projects, the root cause is almost always the same: the gap between what the human wants and what the model assumes. The model fills the gap with statistically plausible completion (fancy hallucination).

The fix is not "better prompts." The fix is **engineering discipline applied upstream**:

1. Compress the truth (Research) before you propose anything
2. Define the WHAT (Spec) before you decide the HOW (Plan)
3. Review the plan **before any code exists** — reviewing 200 lines of markdown is 10× cheaper and 100× more valuable than reviewing 2,000 lines of generated code
4. Reset context between phases — the LLM stays in its "smart zone"
5. Use a fresh agent to review the code, never the agent that wrote it

## Installation

```bash
git clone https://github.com/eduardodotai/spec-driven-advanced.git
cd spec-driven-advanced
bash install.sh
```

This installs the skill to `~/.claude/skills/spec-driven-advanced/`. Restart Claude Code to load it.

**Uninstall:** `bash install.sh --uninstall`

**Update:** `git pull && bash install.sh --force`

## Usage

Once installed, the skill auto-triggers when you mention SDD, RPI, "spec-driven", "no vibe coding", "plan before code", "build properly", "the right way", or any of dozens of natural-language variants.

You can also invoke the slash commands directly:

| Command | What it does |
|---------|--------------|
| `/sdd-init` | Bootstrap `.sdd/` and walk through the constitution interview |
| `/sdd-research <feature>` | Brownfield codebase investigation (no code, no opinions) |
| `/sdd-spec <feature>` | Draft the spec (problem, goals, ACs, edge cases) |
| `/sdd-plan <feature>` | Draft the technical plan |
| `/sdd-review-plan <feature>` | Present plan + critic agent — Gate #1 |
| `/sdd-tasks <feature>` | Decompose plan into atomic tasks |
| `/sdd-implement <feature> [task]` | Implement one task with fresh context |
| `/sdd-verify <feature>` | Run build/tests/lint/types |
| `/sdd-review-code <feature>` | Fresh-context critic reviews code vs spec — Gate #2 |
| `/sdd-iterate <feature>` | Apply review fixes (max 3 cycles) |
| `/sdd-ship <feature>` | Produce ship report + update changelog |
| `/sdd-status [feature]` | Show progress |

## What gets created

```
your-project/
└── .sdd/
    ├── constitution.md          # permanent project governance
    ├── changelog.md             # running log of shipped features
    └── features/
        └── 001-google-sso/
            ├── research.md      # Phase 1
            ├── spec.md          # Phase 2
            ├── plan.md          # Phase 3
            ├── plan-review.md   # Phase 4 — Human Gate #1
            ├── tasks.md         # Phase 5
            ├── verify.md        # Phase 7
            ├── review.md        # Phase 8 — Human Gate #2
            └── ship.md          # Phase 10
```

## Parallelism strategy (v1.1.0)

The skill parallelizes **analysis**, not **execution**. Wall-clock improvements come from running multiple analytical sub-agents concurrently at the gates — not from racing implementation tasks.

| Phase | Default | Where parallel helps |
|---|---|---|
| **1 — Research** | 4 sub-agents in parallel by default | Big brownfield: 3–5× faster |
| **3 — Plan** | Sequential | Optional `--explore` mode dispatches 2–3 alternative architectures |
| **6 — Implement** | **Always sequential** | Only for mechanical refactors on disjoint files |
| **8 — Code Review** | 4 fresh-context critics in parallel by default | 2–3× catch rate (security / performance / maintainability / AC coverage) |

See [`references/parallel-agents.md`](references/parallel-agents.md) for the full dispatch protocol.

## Helper scripts

The skill ships with three Python 3 stdlib-only scripts:

| Script | Purpose |
|--------|---------|
| `scripts/init_sdd_project.py` | Bootstraps `.sdd/` with constitution stub |
| `scripts/new_feature.py` | Creates a numbered feature folder with all 8 artifact stubs (refuses to run if constitution still has `[TO BE FILLED]` markers) |
| `scripts/validate_phase.py` | Verifies a feature is ready to advance to a target phase — mechanically enforces the two human gates by checking for `[x] APPROVED` decisions |

## Project layout

```
spec-driven-advanced/
├── README.md                    # this file
├── LICENSE                      # MIT
├── install.sh                   # one-liner installer
├── .gitignore
├── .skillignore                 # excludes from skill packaging
├── SKILL.md                     # main skill entry (lean, ~180 lines)
├── references/                  # lazy-loaded deep docs
│   ├── phases.md                # full description of all 10 phases
│   ├── templates.md             # all 9 artifact templates
│   └── review-system.md         # P0/P1/P2 + iteration protocol + validator behavior
├── scripts/                     # helper Python scripts
│   ├── init_sdd_project.py
│   ├── new_feature.py
│   └── validate_phase.py
└── sources/                     # input materials used to build the skill (not installed)
```

## Methodology references

- **"No Vibes Allowed"** — Dex Horthy at AI Engineer World's Fair
- **12 Factor Agents** — HumanLayer
- **GitHub Spec Kit** — github.com/github/spec-kit
- **Context Rot** — Chroma Research on the Dumb Zone

## License

MIT — see [LICENSE](LICENSE).

---

## 🇧🇷 Português

> Uma skill do Claude Code que implementa o workflow completo de **10 fases SDD + RPI** — Spec-Driven Development combinado com Research, Plan, Implement.

**Sem vibe coding. Planeje antes de codar. Specs são a fonte de verdade.**

### O que é

`spec-driven-advanced` transforma engenharia de software assistida por IA em um workflow disciplinado de 10 fases, com dois portões humanos de revisão e um checkpoint automatizado. Funciona tanto para projetos novos (greenfield) quanto para codebases existentes (brownfield).

Combina duas metodologias:

- **SDD (Spec-Driven Development)** — especificações são a fonte de verdade, código é derivado
- **RPI (Research, Plan, Implement)** — desenvolvido por Dex Horthy na HumanLayer; cada fase reseta o contexto para manter o LLM fora da "Dumb Zone" onde a performance despenca

A skill impõe a **regra de separação escritor/revisor**: o agente que escreve código nunca é o mesmo contexto que o revisa. Isso elimina viés de confirmação e é a maior alavanca de qualidade em desenvolvimento assistido por IA.

### As 10 fases

| # | Fase | Quando | Output | Portão |
|---|------|--------|--------|--------|
| 0 | Constitution | Uma vez por projeto | `constitution.md` | — |
| 1 | Research | Apenas brownfield | `research.md` | — |
| 2 | Spec | Toda feature | `spec.md` | — |
| 3 | Plan | Toda feature | `plan.md` | — |
| 4 | **Plan Review** | Após o Plan | `plan-review.md` | **Portão Humano #1** |
| 5 | Tasks | Após Plan aprovado | `tasks.md` | — |
| 6 | Implement | Uma task por vez | código + testes | — |
| 7 | Verify | Após cada task | `verify.md` | Automatizado |
| 8 | **Code Review** | Após Verify passar | `review.md` | **Portão Humano #2** |
| 9 | Iterate | Se Review falhar | código atualizado | Máx 3 ciclos |
| 10 | Ship | Após Review aprovado | `ship.md` + changelog | — |

### Por que existe

Quando "vibe coding" com agentes de IA colapsa em projetos reais, a causa raiz é quase sempre a mesma: a lacuna entre o que o humano quer e o que o modelo assume. O modelo preenche a lacuna com completação estatisticamente plausível (alucinação sofisticada).

A correção não é "prompts melhores". A correção é **disciplina de engenharia aplicada upstream**:

1. Comprima a verdade (Research) antes de propor qualquer coisa
2. Defina o QUE (Spec) antes de decidir o COMO (Plan)
3. Revise o plano **antes de qualquer código existir** — revisar 200 linhas de markdown é 10× mais barato e 100× mais valioso que revisar 2.000 linhas de código gerado
4. Resete o contexto entre fases — o LLM fica na "zona inteligente"
5. Use um agente novo para revisar o código, nunca o agente que o escreveu

### Instalação

```bash
git clone https://github.com/eduardodotai/spec-driven-advanced.git
cd spec-driven-advanced
bash install.sh
```

Instala a skill em `~/.claude/skills/spec-driven-advanced/`. Reinicie o Claude Code para carregá-la.

**Desinstalar:** `bash install.sh --uninstall`

**Atualizar:** `git pull && bash install.sh --force`

### Uso

Depois de instalada, a skill auto-dispara quando você menciona SDD, RPI, "spec-driven", "sem vibe coding", "planejar antes de codar", "fazer direito", "do jeito certo", ou dezenas de variantes em linguagem natural.

Você também pode invocar os slash commands diretamente — veja a tabela de comandos na seção em inglês acima.

### Licença

MIT — veja [LICENSE](LICENSE).

---

**Built by [@eduardodotai](https://github.com/eduardodotai)** — 2026

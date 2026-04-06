# SDD + RPI: Guia Completo
## Spec-Driven Development + Research, Plan, Implement

> Conversa exportada — Abril 2026
> Coach & Mentor de AI

---

## Sumário

1. [O Problema Fundamental](#o-problema-fundamental)
2. [Parte 1: SDD — Spec-Driven Development](#parte-1-sdd--spec-driven-development)
3. [Parte 2: RPI — Research, Plan, Implement](#parte-2-rpi--research-plan-implement)
4. [Parte 3: Como SDD e RPI se Complementam](#parte-3-como-sdd-e-rpi-se-complementam)
5. [Parte 4: A Regra de Ouro](#parte-4-a-regra-de-ouro)
6. [Parte 5: Quando Usar Cada Um](#parte-5-quando-usar-cada-um)
7. [O Workflow Completo: 10 Fases](#o-workflow-completo-10-fases)
8. [Ferramentas Existentes](#ferramentas-existentes)
9. [Skill Customizada SDD+RPI](#skill-customizada-sddrpi)
10. [Materiais Complementares para Estudo](#materiais-complementares-para-estudo)

---

## O Problema Fundamental

### Por que SDD + RPI existem

Quando o "vibe coding" surgiu no início de 2025 (termo cunhado por Andrej Karpathy), desenvolvedores tratavam agentes de IA como mecanismos de busca — digitavam uma pergunta e recebiam código de volta. Essa abordagem funciona para protótipos rápidos, mas colapsa ao construir aplicações sérias e de missão crítica.

O resultado? **Slop** — código de baixa qualidade que parece funcional, compila, passa nos testes básicos, mas viola premissas arquiteturais profundas.

**Caso emblemático:** Uma equipe usou um agente de IA para remover dependências Hadoop do Parquet Java. O agente tinha acesso a tudo — codebase completo, documentação, histórico de commits. O código compilou e os testes passaram. Quando fizeram merge, quebrou tudo. O agente havia misturado APIs de três versões diferentes do Hadoop, criando uma camada de compressão que funcionava em testes mas corrompia dados em produção.

O problema de raiz? **A lacuna entre intenção e implementação.** Você sabe o que quer, mas a IA não sabe — e sem uma estrutura disciplinada, ela preenche as lacunas com "completação estatisticamente plausível" (alucinação sofisticada).

---

## Parte 1: SDD — Spec-Driven Development

### O que é

SDD inverte a estrutura de poder tradicional do desenvolvimento. Especificações não servem ao código — código serve às especificações. O PRD não é um guia para implementação; é a fonte que **gera** implementação.

Em termos simples: você primeiro descreve **o quê** construir com precisão cirúrgica, e só depois o código é gerado a partir dessa descrição. SDD é um paradigma de desenvolvimento que utiliza especificações de requisitos bem elaboradas como prompts, auxiliadas por agentes de codificação com IA, para gerar código executável.

### Os 4 Pilares do SDD

**1. Constitution (Constituição)** — O documento de governança do projeto. Estabelece princípios inegociáveis que se aplicam a toda mudança. Por exemplo: "toda aplicação deve ser CLI-first", "sempre usar TypeScript strict mode", "testes com cobertura mínima de 80%". É basicamente um arquivo de regras poderoso que é referenciado por todo o workflow subsequente.

**2. Spec (Especificação)** — O documento que define **o quê** construir, do ponto de vista do usuário. Inclui critérios de sucesso, restrições, e cenários de aceitação. A separação crucial aqui: manter o "o quê" (especificação) separado do "como" (plano de implementação).

**3. Plan (Plano Técnico)** — Define **como** implementar a spec. Inclui decisões de arquitetura, stack tecnológica, modelos de dados. A mesma spec pode gerar múltiplas variantes de plano em branches paralelos — habilitando a fase de Exploração Criativa.

**4. Tasks (Tarefas)** — Cada tarefa deve ser implementável de forma independente, testável em isolamento e revisável como um único PR.

### O Workflow SDD na Prática

O fluxo é sequencial e disciplinado:

**Constitution → Specify → Plan → Tasks → Implement**

Para facilitar o processo SDD, foram introduzidos comandos sequenciais — primeiro você cria a spec com `/specify`, depois o plano com `/plan`, e então as tarefas com `/tasks`.

A beleza disso: a mesma spec pode produzir uma implementação .NET/Blazor em um branch e uma implementação Vite/vanilla-JS em outro. A spec é agnóstica de tecnologia. O plano é onde as decisões técnicas vivem.

### Por que SDD é diferente de documentação tradicional

A diferença entre SDD e processos tradicionais de documentação é que SDD separa explicitamente as fases de design e implementação, comprimindo o contexto em specs. Antigamente, a documentação ficava desatualizada no dia seguinte ao código ser escrito. No SDD, a spec **é** a fonte de verdade que gera o código.

---

## Parte 2: RPI — Research, Plan, Implement

### Origem e Contexto

RPI foi desenvolvido por Dex Horthy na HumanLayer. O framework ajuda engenheiros a dividir tarefas complexas de codificação em fases discretas: pesquisar o codebase primeiro, planejar a abordagem, e então implementar, em vez de jogar um ticket inteiro para um agente de codificação e torcer pelo melhor.

### O Conceito-Chave: A "Dumb Zone"

Este é o insight mais importante de toda a metodologia.

Pesquisas mostram que modelos que alegam janelas de contexto de 200k tokens se tornam pouco confiáveis por volta de 130k. A performance não degrada gradualmente — ela despenca de um penhasco.

Dex Horthy cunhou o termo "Dumb Zone" para descrever a faixa de 40-60% de uma janela de contexto grande onde a performance do modelo cai significativamente. Informação colocada nessa zona tem mais chance de ser ignorada ou mal interpretada.

A implicação prática: **mais contexto ≠ melhores resultados**. O contrário é verdadeiro. A única forma de obter melhor performance de um LLM é colocar tokens melhores na entrada, e então você recebe tokens melhores na saída.

### As 3 Fases do RPI

#### FASE 1 — RESEARCH (Pesquisa: Comprimindo a Verdade)

Antes de escrever uma única linha de código, o agente **investiga** o codebase existente.

Execute prompts que exploram o codebase para encontrar os arquivos exatos e números de linha relevantes para o problema.

Regras desta fase:
- O agente **NÃO escreve código**. Ele apenas lê e documenta.
- O output é um arquivo markdown compacto com: arquivos relevantes, padrões encontrados, dependências, e restrições.
- O trabalho é muito estrito: documentar o que existe hoje. Sem opiniões.
- A pesquisa pode acionar sub-agentes paralelos: um para localizar arquivos, outro para analisar código, outro para encontrar padrões.

#### FASE 2 — PLAN (Plano: Comprimindo a Intenção)

O plano não é apenas uma lista com bullets; deve incluir nomes de arquivos específicos e trechos de código do que vai mudar.

Este é o momento de **alinhamento mental** — o conceito mais poderoso do RPI. Ler um plano permite alinhamento mental. É muito mais fácil para um humano revisar um plano e identificar um erro de lógica do que revisar 1.000 linhas de código gerado depois do fato.

Como Dex Horthy coloca: o plano é para alinhamento mental entre o usuário e o agente, mas também é o documento perfeito para alinhamento entre equipes.

#### FASE 3 — IMPLEMENT (Implementação: Execução com Contexto Limpo)

Somente quando a pesquisa é sólida e o plano é aprovado é que você permite que o agente gere o código. Como você fez a engenharia de contexto de antemão, até modelos menores e mais baratos podem executar a implementação com sucesso porque o caminho é tão claro.

O detalhe crucial: a implementação acontece com uma **janela de contexto fresca**. O agente recebe apenas o plano compactado, não todo o histórico da conversa de pesquisa. Isso mantém o agente na "zona inteligente".

---

## Parte 3: Como SDD e RPI se Complementam

A relação é simples e elegante:

**SDD define a filosofia** ("specs são a fonte de verdade, código é output derivado"). **RPI define a execução** ("pesquise antes de planejar, planeje antes de implementar, resete o contexto entre cada fase").

O workflow SDD é similar ao RPI (Specify → Plan → Task → Implement), mas SDD é mais formal e orientado a ferramentas. Ambas as metodologias surgiram como resposta ao mesmo problema: "vibe coding" não-estruturado com agentes de IA produz resultados não-confiáveis.

Na prática, eles se encaixam assim:

- **Constitution** (SDD) — define as regras imutáveis do projeto
- **Research** (RPI) — investiga o codebase e contexto existente
- **Spec** (SDD) — define o quê construir
- **Plan** (SDD + RPI) — define como construir, informado pela pesquisa
- **Tasks** (SDD) — decompõe o plano em unidades atômicas
- **Implement** (RPI) — executa cada tarefa com contexto limpo

---

## Parte 4: A Regra de Ouro

> **"Você não pode terceirizar o pensamento."** — Dex Horthy

Uma armadilha comum é esperar que a IA faça o pensamento por você. Ela não vai. IA não pode substituir o pensamento; ela só pode amplificar o pensamento que você já fez.

Uma linha ruim de pesquisa se torna cem linhas ruins de código. Um plano ruim se torna uma semana de retrabalho. Coloque seu esforço upstream: verifique a pesquisa, valide os planos, arbitre a estratégia. Deixe o agente escrever o código.

---

## Parte 5: Quando Usar Cada Um

RPI é projetado especificamente para codebases brownfield — onde existe arquitetura legada e restrições que não podem ser ignoradas. A fase de pesquisa é absolutamente essencial em contextos brownfield. Porém, para projetos greenfield a metodologia não funciona tão bem — quando não existe código legado para pesquisar, o movimento de maior alavancagem é escrever specs e usar execução baseada em loops.

**Resumindo:**
- Projeto novo do zero → **SDD puro**
- Projeto existente com código legado → **SDD + RPI**
- Tarefa complexa em codebase grande → **RPI obrigatório**

---

## O Workflow Completo: 10 Fases

Cada fase produz artefatos que a próxima fase consome, e cada artefato tem uma máquina de estados: **rascunho → em revisão → aprovado → completo**.

### FASE 0: CONSTITUTION (Fundação)

**O que é:** O documento de governança permanente do projeto. Não muda entre features — ele governa tudo.

**O que produz:** `constitution.md`

**Conteúdo típico:**
- Stack tecnológica obrigatória
- Padrões de arquitetura (DDD, Clean Architecture, etc.)
- Convenções de código e testes
- Requisitos de compliance e segurança
- Restrições de infraestrutura

A constitution funciona como portões pré-implementação. A IA deve passar por cada portão ou documentar uma exceção justificada antes de prosseguir para as fases de implementação.

**Analogia:** Pense na Constitution como a Constituição de um país — ela não muda a cada lei nova. Ela define os princípios que toda lei deve respeitar.

### FASE 1: RESEARCH (Pesquisa — Comprimindo a Verdade)

**O que é:** Investigação profunda do codebase existente e do domínio do problema. Zero opinião, zero código.

**O que produz:** `research.md`

Antes de escrever uma spec, você precisa entender o codebase. Isso pode acionar uma frota de sub-agentes especializados em paralelo — um localizador de codebase para encontrar arquivos relevantes, um analisador de codebase para entender como código específico funciona, um buscador de padrões para identificar convenções existentes.

**Regras rígidas:**
- O agente NÃO escreve código
- O agente NÃO dá opiniões
- O output deve incluir: arquivos relevantes, dependências, padrões existentes, restrições técnicas
- Inclua caminhos de arquivo + números de linha + uma frase explicando "por quê" para cada decisão

**Anti-pattern:**
- Pesquisa de 10 páginas para adicionar um botão é "paralisia de pesquisa"
- Pesquisa de 3 frases para uma migração de banco é "sub-compactação"

### FASE 2: SPEC (Especificação — Definindo o Quê)

**O que é:** Define O QUÊ construir, do ponto de vista do usuário e do negócio. Sem decisões técnicas aqui.

**O que produz:** `spec.md`

A spec é um documento estilo RFC com resumo executivo, objetivos e não-objetivos, arquitetura proposta (com diagramas Mermaid), design detalhado, alternativas consideradas, e questões em aberto.

**Conteúdo essencial:**
- Problema que está sendo resolvido
- Critérios de aceitação (testáveis e mensuráveis)
- O que NÃO está no escopo (não-objetivos)
- Cenários de uso e edge cases
- Restrições de negócio

**Regra de ouro:** A spec deve ser explícita o suficiente para que uma sessão fresca de agente possa implementar a partir dela sem nenhum histórico de conversa.

### FASE 3: PLAN (Plano Técnico — Definindo o Como)

**O que é:** Transforma a spec em decisões de arquitetura e design técnico.

**O que produz:** `plan.md`

**Conteúdo:**
- Decisões de arquitetura (informadas pela pesquisa)
- Modelos de dados e contratos
- Estratégia de testes
- Plano de rollback
- Fases de implementação ordenadas

Documentos de design são revisados antes de qualquer código ser escrito. É aqui que humanos mantêm controle sobre a arquitetura.

### FASE 4: REVIEW DO PLANO (Portão Humano #1)

**O que é:** O humano revisa spec + plan antes de qualquer código existir.

**O que produz:** Plano aprovado (ou plano revisado com correções)

Para verificações que exigem julgamento ("esses critérios de aceitação são realmente testáveis?" ou "essa arquitetura segue padrões estabelecidos?"), um agente crítico dedicado valida o output contra a definição de pronto, retornando aprovado/reprovado com explicação.

**Por que isso é tão importante:** Validação frequentemente revela lacunas na sua pesquisa ou falhas no seu plano. Isso é esperado. O valor não está em executar cada fase perfeitamente na primeira vez; está em ter um framework sistemático que captura problemas antes que eles se acumulem.

A decisão neste ponto é binária: **aprovar e avançar** ou **iterar de volta para pesquisa/spec**.

### FASE 5: TASKS (Decomposição em Tarefas Atômicas)

**O que é:** O plano é decomposto em unidades de trabalho pequenas, independentes e verificáveis.

**O que produz:** `tasks.md`

O agente lê a spec e a decompõe em tarefas discretas com critérios de verificação e dependências identificadas.

**Cada tarefa deve ter:**
- Descrição clara do que muda
- Arquivos afetados
- Critérios de verificação (como saber se está pronto)
- Dependências de outras tarefas
- Testes esperados

### FASE 6: IMPLEMENT (Implementação — Execução Fase a Fase)

**O que é:** Execução do código, tarefa por tarefa, com contexto limpo.

**O que produz:** Código funcional + testes

O agente gera um worker sub-agente para a tarefa de maior prioridade pendente e faz um loop: implementar, testar, validar, avançar. Cada worker segue TDD e princípios SOLID por padrão.

**Regras críticas:**
- Uma tarefa por vez, com contexto fresco
- Teste o código após cada tarefa
- O agente atualiza os checkboxes diretamente no arquivo do plano conforme avança, permitindo retomar de onde parou se a janela de contexto encher

### FASE 7: VERIFY (Verificação Automatizada)

**O que é:** Após cada tarefa implementada, verificações automatizadas rodam.

**O que produz:** Relatório de verificação (passa/falha)

**O que é verificado:**
- Build compila
- Testes unitários passam
- Linting/formatação passa
- Testes de integração passam
- Verificação de tipos (typecheck)

Execute seu build, testes e linters. Se falharem, você tem sinal claro de que iteração ou regeneração é necessária. Se passarem, verifique manualmente se o comportamento corresponde ao seu plano e modelo mental.

### FASE 8: REVIEW DO CÓDIGO (Portão Humano #2 + Agente Crítico)

**O que é:** Revisão do código gerado contra a spec original. O agente que revisa gera um documento de erros estruturado.

**O que produz:** `review.md` (documento de revisão com erros, sugestões, e decisões)

Uma sessão fresca de agente revisa a implementação contra a spec. Essa é a separação escritor/revisor — o agente revisor não tem viés em relação ao código que está avaliando.

**Estrutura do review.md:**
- Checklist de critérios de aceitação (da spec): passou/falhou
- Bugs ou inconsistências encontrados
- Violações da constitution
- Sugestões de melhoria
- Decisão: aprovar / iterar / rejeitar

Se qualquer camada rejeitar o output, o agente produtor itera (ainda dentro da mesma fase) até que o artefato passe. O número de iterações é limitado a 3-5 tentativas para prevenir loops infinitos; se o agente não conseguir passar nas avaliações dentro do limite, o workflow falha e volta para intervenção humana.

### FASE 9: ITERATE (Loop de Correção)

**O que é:** Se o review encontrou problemas, o agente corrige sem precisar recomeçar tudo.

**O que produz:** Código corrigido + review atualizado

**Decisão crítica:** iterar com correções ou regenerar do zero?
- **Itere** quando o output está alinhado com suas expectativas mas tem lacunas — edge cases faltando, débito técnico, tratamento de erro incompleto
- **Regenere** quando algo fundamental está errado — a arquitetura não corresponde ao seu modelo mental, o agente não entendeu os requisitos

O agente é melhor em encontrar problemas no código do que em gerar código perfeito na primeira tentativa. Use-o para revisar seu próprio trabalho.

### FASE 10: SHIP (Entrega + Documentação Final)

**O que é:** PR criado, documentação atualizada, entrega feita.

**O que produz:** PR pronto para merge + documentação atualizada

**Inclui:**
- PR com descrição clara vinculada à spec
- README atualizado
- Changelog atualizado
- plan.md e tasks.md atualizados com status final

### Por que Isso NÃO é Waterfall

Agentes mudam a economia. Quando um agente pode executar o ciclo completo de requisitos → arquitetura → tarefas → implementação em horas (não meses), você pode bancar a estrutura. Equipes rodam múltiplos ciclos completos por dia. Isso entrega o que waterfall prometia — rastreabilidade, consistência arquitetural, trilhas de decisão claras — sem o custo que o tornava impraticável.

---

## Ferramentas Existentes

### 1. cc-sdd (mais popular)

Suporta Claude Code, Codex, Cursor, Gemini CLI, Copilot, Windsurf, e outros.

```bash
npx cc-sdd@latest --claude --lang pt
```

Segue o fluxo Kiro: requirements → design → tasks → implement.

**Repositório:** [github.com/gotalab/cc-sdd](https://github.com/gotalab/cc-sdd)

### 2. claude-code-spec-workflow (Pimzino)

Inclui 14 slash commands, steering documents, templates, sub-agentes validadores, e redução de 60-80% no consumo de tokens.

```bash
npx @pimzino/claude-code-spec-workflow
```

**Repositório:** [github.com/Pimzino/claude-code-spec-workflow](https://github.com/Pimzino/claude-code-spec-workflow)

### 3. sdd-skill (SpillwaveSolutions)

Funciona com Claude Code, Copilot, Cursor, Windsurf, Gemini CLI. Suporta tanto projetos greenfield quanto brownfield — consegue fazer engenharia reversa de projetos existentes para formato SDD.

**Repositório:** [github.com/SpillwaveSolutions/sdd-skill](https://github.com/SpillwaveSolutions/sdd-skill)

### Limitação das ferramentas existentes

Nenhuma dessas implementa o workflow completo de 10 fases. Faltam as fases de Research profundo (estilo RPI), Review com documento de erros, e o loop de iteração estruturado.

---

## Materiais Complementares para Estudo

### Recursos Primários (em ordem de prioridade)

1. **"No Vibes Allowed"** — Palestra do Dex Horthy no AI Engineer World's Fair (YouTube). Material original que apresentou a Dumb Zone e o RPI.

2. **12 Factor Agents** — Paper da HumanLayer sobre princípios para construir agentes confiáveis — [humanlayer.dev](https://humanlayer.dev)

3. **GitHub Spec Kit** — Repositório oficial do GitHub com templates e CLI para SDD — [github.com/github/spec-kit](https://github.com/github/spec-kit)

4. **Artigo da Thoughtworks sobre SDD** — Análise equilibrada de uma das organizações mais respeitadas em engenharia — [thoughtworks.com](https://www.thoughtworks.com/en-us/insights/blog/agile-engineering-practices/spec-driven-development-unpacking-2025-new-engineering-practices)

5. **Tutorial RPI do Goose** — Implementação prática do workflow RPI com recipes — [block.github.io/goose/docs/tutorials/rpi/](https://block.github.io/goose/docs/tutorials/rpi/)

6. **Artigo da Martin Fowler** sobre as 3 ferramentas de SDD — Análise crítica e honesta do estado atual — [martinfowler.com](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html)

### Recursos Secundários

7. **Tyler Burleigh — Research, Plan, Implement, Review** — Workflow agentic completo com review em cada transição — [tylerburleigh.com](https://tylerburleigh.com/blog/2026/02/22/)

8. **QuantumBlack (McKinsey) — Agentic Workflows for Software Development** — Implementação enterprise com agentes críticos e máquina de estados — [medium.com/quantumblack](https://medium.com/quantumblack/agentic-workflows-for-software-development-dc8e64f4a79d)

9. **Agent Factory — Chapter 16: SDD with Claude Code** — Guia completo usando capacidades nativas do Claude Code — [agentfactory.panaversity.org](https://agentfactory.panaversity.org/docs/General-Agents-Foundations/spec-driven-development)

10. **Context Rot (Chroma Research)** — Pesquisa sobre degradação de performance em janelas de contexto — [morphllm.com/context-rot](https://www.morphllm.com/context-rot)

### Podcasts

11. **Dev Interrupted — Dex Horthy on Ralph, RPI, and the Dumb Zone** — [linearb.io](https://linearb.io/dev-interrupted/podcast/dex-horthy-humanlayer-rpi-methodology-ralph-loop)

---

> **Lembre-se:** Você não pode terceirizar o pensamento. IA amplifica o pensamento que você já fez — ou a falta dele.

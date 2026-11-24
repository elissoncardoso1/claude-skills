---
name: prompt-engineering
description: Engenharia de prompt e de contexto baseada em evidência (papers + docs oficiais Anthropic, OpenAI, Google) para escrever, revisar, depurar e otimizar prompts — system prompts, prompts de usuário, few-shot, chain-of-thought, prompts para modelos de raciocínio, instruções de agentes, descrições de ferramentas/MCP, schemas de saída estruturada (JSON), pipelines multi-etapa, RAG/contexto longo, LLM-as-judge, avaliação (evals) e otimização automática (APE, OPRO, DSPy, TextGrad), além de defesa contra prompt injection. Use sempre que o usuário pedir para criar, melhorar, auditar ou traduzir um prompt; montar instruções de um GPT/Projeto/agente/skill; escrever o prompt que vai dentro de código (API Claude/OpenAI/Gemini, LangChain, Agent SDK); diagnosticar por que um LLM ignora instruções, alucina, formata errado ou quebra o JSON; ou comparar variantes de prompt — mesmo que não diga "engenharia de prompt".
---

# Prompt Engineering — da intenção ao prompt validado

Esta skill transforma um objetivo em um prompt (ou contexto completo de agente) que funciona de forma **mensurável**. Ela cobre três superfícies que compartilham os mesmos princípios:

| Superfície | Exemplos | Referência principal |
|---|---|---|
| **Chat / uso direto** | prompt para colar no Claude/ChatGPT/Gemini, instruções de Projeto/GPT | `references/fundamentos.md` |
| **Código / API** | system prompt em app, prompt builder versionado, structured output, chains | `references/provedores.md`, `references/saida-estruturada.md` |
| **Agentes** | system prompt de agente, ferramentas, MCP, subagentes, skills, tarefas longas | `references/agentes.md`, `references/ferramentas.md` |

A ideia central (Anthropic F30, Prompt Report F14): um LLM é *persuadido, não programado*. Pequenas mudanças de formato, ordem ou palavra mudam resultados em dezenas de pontos (F11–F13), e o que vale para um modelo nem sempre vale para outro. Por isso o trabalho real não é "escrever o prompt perfeito" e sim **definir sucesso → escrever o mínimo claro → testar → corrigir a partir de falhas observadas**.

## 1. Fluxo de trabalho

### Passo 0 — Classificar o pedido
Identifique o modo antes de escrever qualquer coisa, porque cada modo pede um entregável diferente:

- **Criar** um prompt do zero → siga os passos 1–5.
- **Revisar/auditar** um prompt existente → rode `scripts/prompt_lint.py` (arquivo, ou texto colado via stdin com `-`) e aplique o checklist da seção 4; entregue diagnóstico + versão reescrita + o que mudou e por quê.
- **Depurar** comportamento ruim ("ele ignora X", "inventa", "quebra o JSON") → tabela de sintomas na seção 5.
- **Agente/ferramentas/skill** → leia `references/agentes.md` e/ou `references/ferramentas.md` antes.
- **Saída estruturada** → `references/saida-estruturada.md`.
- **Avaliar/comparar/otimizar** → `references/avaliacao.md` e `references/otimizacao.md`.
- **Prompt que recebe dados externos** (e-mail, web, documentos, saída de ferramenta) → leia também `references/seguranca.md`.

### Passo 1 — Definir sucesso (antes do prompt)
Escreva em 2–5 linhas: tarefa, público/consumidor da saída (humano? parser?), formato de saída, restrições duras, e **como saberemos que funcionou** (critério verificável ou rubrica). Sem isso não há como iterar (Anthropic F34; OpenAI F24/F28). Se faltar informação essencial, assuma o razoável e declare a suposição — não trave em perguntas.

### Passo 2 — Escolher a arquitetura mais simples que resolve
Ordem de preferência (Anthropic F29): **uma chamada bem escrita (+ exemplos/recuperação)** → **workflow** (chaining, routing, paralelização, orchestrator-workers, evaluator-optimizer) → **agente** autônomo. Só suba de nível quando houver ganho demonstrável; cada nível adiciona custo, latência e erros compostos. Para raciocínio: modelo de raciocínio/thinking adaptativo antes de técnicas manuais (ver `references/raciocinio.md`).

### Passo 3 — Redigir o prompt
Use a anatomia da seção 2. Escreva na "altitude certa" (F30): específico o bastante para guiar, flexível o bastante para o modelo generalizar — nem if/else frágil, nem orientação vaga. Comece mínimo e acrescente instruções **em resposta a falhas observadas**, não a falhas imaginadas.

### Passo 4 — Testar
Monte 5–20 casos representativos incluindo bordas (entrada vazia, fora de escopo, ambígua, adversarial). Para código, use `scripts/eval_harness.py`; para julgamento qualitativo, `scripts/pairwise_judge.py` (troca a ordem para anular viés de posição — F17). Em chat, rode mentalmente o prompt contra os casos e mostre ao usuário.

### Passo 5 — Iterar e entregar
Corrija uma causa por vez, guarde as versões e reavalie. Ao entregar:

- Prompt **dentro de bloco de código** (pronto para copiar), com variáveis em `{{chaves}}` ou tags.
- Abaixo: decisões de design em 3–6 bullets (o *porquê*), suposições feitas, e como testar.
- Prompts para ferramentas visuais de IA (imagem/vídeo): prompt em inglês, texto visível na arte em português.
- Para código: entregue o prompt como constante/arquivo versionado + chamada de API mínima correta do provedor.

## 2. Anatomia de um bom prompt

Ordem recomendada (convergência OpenAI F24, Anthropic F34, Gemini F35). Use apenas os blocos necessários:

```
[Identidade/papel]        1–2 frases: quem é, para quem trabalha, objetivo.
[Contexto e motivação]    por que a tarefa existe; quem lê a saída; o que importa.
[Instruções]              o que fazer, em passos numerados se ordem importar.
[Restrições]              limites, o que fazer em casos de borda e quando não souber.
[Formato de saída]        estrutura exata, extensão, idioma, tom.
[Exemplos]                3–5, diversos, no mesmo formato da saída desejada.
[Dados/documentos]        delimitados em tags; marcados como dados, não instruções.
[Tarefa/pergunta final]   no fim quando houver contexto longo.
```

Princípios com evidência — aplique por padrão:

1. **Claro e direto, como para um colega brilhante sem contexto.** Teste: alguém de fora entenderia o que fazer? (F34)
2. **Explique o porquê.** "Será lido por TTS, então não use reticências" generaliza melhor que "NUNCA use reticências" (F34). Evite CAIXA ALTA/"CRITICAL: MUST" — modelos atuais seguem instruções literalmente e superdisparam com linguagem agressiva (F34, F35).
3. **Diga o que fazer, não só o que não fazer.** "Escreva em parágrafos corridos" > "não use markdown". O estilo do prompt contamina a saída: prompt cheio de bullets gera bullets (F34).
4. **Delimite seções** com tags XML (`<instrucoes>`, `<contexto>`, `<documento index="1">`) ou cabeçalhos Markdown — um padrão só, consistente (F24, F35).
5. **Exemplos são o controle mais forte de formato e tom** (F01, F34, F35). 3–5 exemplos diversos, formato idêntico entre si, rótulos balanceados e sem agrupar a mesma classe no fim (F11, F12). A ordem dos exemplos pode mover a acurácia de ~50% a ~90% e não transfere entre modelos — revalide ao trocar de modelo.
6. **Contexto longo: documentos no topo, pergunta no fim** (até +30% — F34; curva em U "lost in the middle" — F10). Peça para citar trechos relevantes antes de responder.
7. **Dê ao modelo uma saída honesta** para quando não souber ou a entrada não servir ("se não estiver no texto, responda `NÃO ENCONTRADO`"). Reduz alucinação e preenchimento forçado de schema (F27, F35).
8. **Persona muda estilo, não capacidade.** Papel no system prompt ajuda tom e profundidade em tarefas consultivas; em perguntas conceituais pode piorar clareza (S5a, 2026). Não espere ganho de acurácia.
9. **Apelos emocionais/pressão ("minha carreira depende disso", "respire fundo")**: efeito pequeno em modelos antigos (S5b, 2023), praticamente nulo em modelos atuais (S5c, 2026). Não use como técnica.
10. **Separe instruções de dados não confiáveis.** Conteúdo externo nunca vai no system/developer prompt; vai delimitado, com lembrete de que instruções ali são informação (F25, F37, F19).

## 3. Mapa das referências — leia só o que o caso pede

| Arquivo | Leia quando |
|---|---|
| `references/fundamentos.md` | Qualquer prompt: clareza, estrutura, exemplos (few-shot), formato, papel, sensibilidade a formato/ordem |
| `references/raciocinio.md` | Tarefas multi-etapa, matemática, lógica, planejamento; modelos de raciocínio; CoT, self-consistency, least-to-most, ReAct, ToT |
| `references/contexto-rag.md` | Documentos longos, RAG, memória, compactação, contexto de agente de longa duração |
| `references/agentes.md` | System prompt de agente, padrões de workflow, autonomia/segurança de ações, subagentes, tarefas multi-janela, skills |
| `references/ferramentas.md` | Escrever/revisar definições de tools, servidores MCP, respostas e erros de ferramentas |
| `references/saida-estruturada.md` | JSON, schemas, function calling vs structured output, regras por provedor |
| `references/avaliacao.md` | Critérios de sucesso, datasets, graders, LLM-as-judge e seus vieses |
| `references/otimizacao.md` | Otimização automática: APE, OPRO, DSPy, TextGrad; quando vale a pena |
| `references/seguranca.md` | Prompt injection direta/indireta, hierarquia de instruções, vazamento de dados |
| `references/provedores.md` | Particularidades e parâmetros de Claude, OpenAI e Gemini (thinking/effort, roles, prefill, sampling) |
| `references/templates.md` | Modelos prontos: assistente, agente, extração, classificador, juiz, revisão de prompt, tool |
| `references/fontes.md` | Bibliografia F01–F37/S5 com achado-chave e ressalvas — use para citar evidência |

### Scripts (Python 3, só stdlib; SDK do provedor apenas se for chamar modelo)

| Script | Para quê |
|---|---|
| `scripts/prompt_lint.py <arquivo> [--role system] [--json]` | Checagem estática: ênfase agressiva, excesso de proibições, ausência de formato/fallback, dados externos no system prompt, tags abertas, termos vagos, apelos emocionais |
| `scripts/eval_harness.py --variants v1.txt v2.txt --dataset casos.jsonl --graders g.json --provider anthropic\|openai\|gemini\|mock --model M` | Compara variantes de prompt num dataset com graders (exact, contains, regex, json_keys, json_field_equals, max_words, python) e gera relatório |
| `scripts/pairwise_judge.py --batch pares.jsonl --criteria "..." --provider P --model M` | Juiz LLM A/B nas duas ordens (controle de viés de posição) |
| `scripts/llm_client.py` | Cliente único usado pelos anteriores; `mock` permite testar o fluxo sem chave |

Execute os scripts em vez de reimplementá-los; leia o `--help` de cada um.

## 4. Checklist de revisão (use ao auditar ou antes de entregar)

- [ ] Objetivo e critério de sucesso explícitos? Um colega sem contexto executaria?
- [ ] Motivação dada para as regras não óbvias?
- [ ] Formato de saída especificado (estrutura, extensão, idioma)? Se for para parser, usa structured output em vez de "responda em JSON"?
- [ ] Casos de borda tratados: sem resposta, entrada fora do escopo, ambiguidade?
- [ ] Exemplos: 3–5, diversos, formato consistente, rótulos balanceados, não contradizem as instruções?
- [ ] Sem instruções contraditórias, redundantes ou só negativas; sem CAIXA ALTA agressiva?
- [ ] Dados externos delimitados e fora do system prompt? Lembrete anti-injeção quando há ferramentas com efeito colateral?
- [ ] Contexto longo no topo, pergunta no fim?
- [ ] Para modelo de raciocínio: objetivo + restrições + contrato de saída, sem micro-gerenciar passos internos?
- [ ] Para agentes: critério de "pronto", verificação, limites de autonomia, ações que exigem confirmação, condição de parada?
- [ ] Prompt mínimo — cada frase muda comportamento? (corte o resto)
- [ ] Plano de teste definido (casos + como medir)?

## 5. Diagnóstico rápido por sintoma

| Sintoma | Causas prováveis | Correção (ver referência) |
|---|---|---|
| Ignora uma instrução | Enterrada no meio; conflita com exemplo; formulada só como proibição | Mover para início/fim, alinhar exemplos, reescrever positiva + porquê (fundamentos) |
| Alucina fatos | Sem fonte; sem saída "não sei" (ou "nunca diga que não sabe"); pergunta antes do documento | Grounding em documento, citações primeiro, permissão para "não encontrado" (contexto-rag) |
| Inventa dados dinâmicos (agenda, estoque, preços, status) | O dado não está no contexto — nenhum prompt resolve | Mudar o **código**: injetar o dado atual na mensagem ou dar uma ferramenta de consulta; o prompt só define o que fazer quando o dado faltar (ferramentas) |
| Formato inconsistente / JSON quebrado | Formato só descrito em prosa | Structured output/strict schema; exemplos; campo de raciocínio antes da resposta (saida-estruturada) |
| Respostas longas demais / curtas demais | Default do modelo; estilo do prompt | Extensão explícita em unidades concretas; exemplo do tamanho desejado (provedores) |
| Erra raciocínio multi-etapa | Resposta antes do raciocínio; tarefa grande demais | Thinking/effort maior, decompor (least-to-most), self-consistency (raciocinio) |
| Agente para cedo ou declara sucesso sem verificar | Sem critério de pronto; preocupação com budget de contexto | Definir "pronto" + verificação; avisar sobre compactação (agentes) |
| Agente faz demais / ações destrutivas | Instruções pró-ação sem limites | Bloco de reversibilidade e confirmação; escopo de autonomia (agentes, seguranca) |
| Chama a ferramenta errada / parâmetros inválidos | Tools sobrepostas; descrições vagas | Consolidar, namespacing, descrição "para novo funcionário", exemplos de uso (ferramentas) |
| Segue instruções escondidas em documentos/web | Dados não delimitados; dados no system prompt | Delimitar, lembrete pós-dados, structured output entre etapas, aprovação humana (seguranca) |
| Funciona num modelo e não noutro | Sensibilidade a formato/ordem/modelo | Re-avaliar formatos e ordem por modelo; não portar prompts otimizados sem teste (avaliacao) |

## 6. Regras de conduta desta skill

- **Baseie recomendações em evidência e diga o grau de confiança.** Achados de papers são de modelos/datas específicas; docs de provedor mudam rápido (as anotadas aqui foram coletadas em out/2026). Para nomes de modelos e parâmetros de API, confira a documentação atual antes de afirmar que algo é suportado.
- **Não invente** dados, números, nomes de modelos ou parâmetros. Se o usuário pedir algo que depende de dado não fornecido, use placeholder explícito (`{{nome_do_paciente}}`).
- **Prefira consertar com o mínimo**: uma frase de motivação ou um exemplo costuma valer mais que um parágrafo de regras.
- Ao escrever prompts para uso pelo próprio usuário em contextos profissionais, respeite o domínio, terminologia e restrições institucionais que ele informar; nunca coloque dados sensíveis reais em exemplos.

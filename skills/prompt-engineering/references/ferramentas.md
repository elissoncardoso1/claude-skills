# Ferramentas (tools / function calling / MCP) — interface agente-computador

Sumário: 1. Princípios · 2. Escolha e granularidade · 3. Nomes e namespacing · 4. Descrições e parâmetros · 5. Respostas · 6. Erros · 7. Avaliação de ferramentas · 8. Template

---

## 1. Princípios (Anthropic F29, F31; Model Spec F25)

- Uma ferramenta é um **contrato entre um sistema determinístico e um agente não determinístico**. Projete para agentes, não como API para desenvolvedores.
- Dê às definições de ferramentas a mesma atenção que ao prompt. No SWE-bench, a Anthropic gastou "mais tempo otimizando ferramentas que o prompt geral"; exigir **caminhos absolutos** eliminou erros de caminho relativo.
- **Poka-yoke**: mude argumentos para tornar erros difíceis de cometer.
- Formatos próximos do texto natural da internet; evite overhead (contar linhas para diffs, escapar código dentro de JSON). Dê espaço para o modelo "pensar" antes de se encurralar.
- Descreva confiabilidade e efeitos colaterais de cada ferramenta (terminal na máquina pessoal ≠ sandbox descartável) (F25). No MCP, use **annotations** para sinalizar acesso open-world e mudanças destrutivas (F31).

## 2. Escolha e granularidade

- Mais ferramentas ≠ melhor. Anti-padrão: embrulhar cada endpoint da API.
- Agentes têm contexto limitado: em vez de `list_contacts` (retorna tudo), ofereça `search_contacts`.
- Consolide operações encadeadas:
  - `schedule_event` em vez de `list_users` + `list_events` + `create_event`
  - `search_logs` (linhas relevantes + contexto) em vez de `read_logs`
  - `get_customer_context` em vez de `get_customer_by_id` + `list_transactions` + `list_notes`
- Teste decisivo: "Se um engenheiro humano não consegue dizer com certeza qual ferramenta usar numa situação, o agente também não conseguirá" (F30). Sobreposição distrai.
- Código para operações determinísticas (ordenar, contar, calcular) — Toolformer (F08) mostrou que delegar cálculo a ferramentas mais que dobra o desempenho em matemática; Gemini recomenda code execution para qualquer aritmética/contagem (F35).

## 3. Nomes e namespacing

- Prefixos por serviço (`asana_search`, `jira_search`) e por recurso (`asana_projects_search`, `asana_users_search`). Prefixo vs sufixo teve efeitos dependentes do modelo — decida por eval (F31).
- Parâmetros sem ambiguidade: `user_id`, não `user`.

## 4. Descrições e parâmetros

- Escreva como para um **funcionário novo**: torne explícito o contexto implícito — formatos de consulta, jargão, relações entre recursos, quando usar e quando *não* usar, diferença para ferramentas parecidas, exemplos de uso, casos de borda, requisitos de formato (F29, F31).
- Pequenos refinamentos de descrição tiveram efeito dramático (Claude Sonnet 3.5 chegou ao estado da arte no SWE-bench Verified após ajustes precisos — F31).
- Modelos de dados estritos para entradas e saídas (`strict: true` no OpenAI; enums; tipos fortes) — ver `saida-estruturada.md`.
- Exemplo de correção por descrição: o modelo acrescentava "2025" a toda busca web, enviesando resultados; uma descrição melhor resolveu (F31).
- Decisão de chamar ferramenta é sensível à formulação (F08) — teste frases de usuário variadas.

## 5. Respostas das ferramentas

- Retorne **informação de alto sinal**; relevância > flexibilidade.
- Evite IDs técnicos crus (`uuid`, `mime_type`, `256px_image_url`); prefira `name`, `file_type`, `image_url`. Resolver UUIDs para linguagem semântica (ou um índice 0..n) melhora precisão e reduz alucinação (F31).
- Ofereça `response_format: "concise" | "detailed"` — no exemplo do Slack, conciso usou ~⅓ dos tokens (72 vs 206) (F31).
- Paginação, filtros, seleção de intervalo e truncamento com padrões sensatos (Claude Code limita a 25.000 tokens por resposta). Ao truncar, inclua instrução de direcionamento ("faça buscas menores e mais específicas").
- Estrutura da resposta (XML/JSON/Markdown) afeta o desempenho sem vencedor universal — escolha por eval.
- Saídas de ferramentas são **dados não confiáveis** para o modelo (ver `seguranca.md`).

## 6. Mensagens de erro

- Projete erros como prompts: diga o que estava errado e como corrigir, com exemplo de entrada válida — não códigos opacos nem stack traces (F31).
  - Ruim: `Error 422`
  - Bom: `Data inválida em 'start': use ISO 8601, ex.: "2026-11-03T14:00:00-03:00".`

## 7. Avaliação de ferramentas (F31)

1. Protótipo (servidor MCP local ou tools direto na API); teste você mesmo.
2. Tarefas de avaliação **realistas**, que exijam várias chamadas:
   - Forte: "Agende uma reunião com a Jane na próxima semana sobre o projeto Acme, anexe as notas da última reunião de planejamento e reserve uma sala."
   - Fraca: "Agende uma reunião com jane@acme.corp na próxima semana."
3. Cada tarefa com resposta/resultado verificável; verificadores não estritos demais com formatação.
4. Loop programático simples (chamada LLM ↔ ferramenta). No system prompt do agente avaliado, peça blocos de raciocínio e feedback antes das chamadas (ou ative thinking intercalado).
5. Métricas além de acurácia: nº de chamadas, tokens, tempo, erros de ferramenta.
6. Analise transcrições: muitas chamadas redundantes → ajustar paginação; muitos parâmetros inválidos → melhorar descrição/exemplos. O que o agente *omite* importa.
7. Cole transcrições num agente de código para refatorar as ferramentas; use conjunto **held-out** para não sobreajustar.

## 8. Template de definição de ferramenta

```json
{
  "name": "crm_search_customers",
  "description": "Busca clientes no CRM por nome, e-mail ou CPF parcial e retorna até `limit` resultados resumidos. Use quando precisar identificar um cliente antes de consultar pedidos ou abrir chamados. Não use para listar todos os clientes; para detalhes completos de um cliente já identificado, use crm_get_customer_context. A busca é case-insensitive e aceita correspondência parcial; e-mails devem ser completos.",
  "input_schema": {
    "type": "object",
    "properties": {
      "query": {"type": "string", "description": "Nome, e-mail completo ou parte do CPF (mín. 4 dígitos). Ex.: 'Maria Souza', 'maria@exemplo.com'."},
      "limit": {"type": "integer", "minimum": 1, "maximum": 20, "description": "Máximo de resultados. Padrão 5."},
      "response_format": {"type": "string", "enum": ["concise", "detailed"], "description": "'concise' retorna nome e id curto; 'detailed' inclui contatos e status."}
    },
    "required": ["query"]
  }
}
```
(OpenAI usa `parameters` e `strict: true`, que exige todos os campos em `required` e `additionalProperties: false` — ver `saida-estruturada.md`.)

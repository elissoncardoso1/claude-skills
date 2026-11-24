# Particularidades por provedor

> As informações abaixo vêm das docs oficiais coletadas em **outubro de 2026** (pasta-fonte F24–F37). Nomes de modelos, parâmetros e prazos mudam com frequência: antes de afirmar suporte a um parâmetro ou escrever código de produção, confira a documentação atual.

Sumário: 1. Anthropic (Claude) · 2. OpenAI · 3. Google (Gemini) · 4. Modelos abertos e outros · 5. Portando prompts entre provedores

---

## 1. Anthropic (Claude) — F34, F30, F31

**Estrutura e estilo**
- Parâmetro `system` para papel/instruções; tags XML para separar blocos; documentos longos no topo, pergunta no fim.
- Exemplos: 3–5 em `<example>` dentro de `<examples>`.
- Modelos recentes: mais diretos e menos verbosos (exceções existem, ex.: Opus 5 tende a respostas longas — peça concisão explicitamente).
- Linguagem agressiva ("CRITICAL", "MUST") causa superdisparo de ferramentas/comportamentos — use tom normal.
- Seguem instruções literalmente: use verbos de ação quando quer ação.
- Leia a página de orientação específica do seu modelo antes (a doc mantém uma tabela por modelo: effort, verbosidade, disparo de ferramentas, subagentes etc.).

**Thinking e effort**
- `thinking: {type: "adaptive"}` (Claude 4.6+): o modelo decide quanto pensar, guiado por `output_config: {effort: "low"|"medium"|"high"|...}`. Em alguns modelos recentes o thinking fica sempre ligado.
- A partir do Claude 4.7, `budget_tokens` manual retorna erro 400 — migre para `effort`.
- Quando thinking está ligado por padrão: selecione blocos de conteúdo **por tipo, não por posição**; reserve espaço em `max_tokens`.
- Passe blocos de thinking de volta **inalterados**; mantenha histórico append-only (Claude 5.1+).
- CoT manual em tags só quando thinking estiver desligado.

```python
import anthropic
client = anthropic.Anthropic()
msg = client.messages.create(
    model="{{MODELO}}",          # ex.: claude-opus-5-5
    max_tokens=16000,
    system="Você é ...",
    thinking={"type": "adaptive"},
    output_config={"effort": "high"},
    messages=[{"role": "user", "content": prompt_usuario}],
)
texto = "".join(b.text for b in msg.content if b.type == "text")
```

**Outros**
- **Prefill** do último turno do assistente: não suportado a partir do Claude 4.6 (erro 400). Use instruções de formato, tools/structured output.
- Autoconhecimento: "O assistente é Claude, criado pela Anthropic. O modelo atual é {{nome}}." Para apps que escolhem modelo, informe a string exata.
- Consciência de contexto: alguns modelos acompanham o orçamento de tokens restante; se o harness compacta, diga isso (ver `contexto-rag.md`).
- Ferramentas: descrições detalhadas, `tool_choice` para forçar; MCP com annotations; respostas de tools ≤ 25k tokens no Claude Code.
- Prompt caching: prefixo estável (system, tools, documentos) no início.

## 2. OpenAI — F24–F28, F37

**Roles e estrutura**
- `developer` (regras do app, prioridade sobre `user`), `user`, `assistant`. Na Responses API, `instructions` ≈ mensagem developer e **não** é herdado via `previous_response_id`.
- Ordem: Identidade → Instruções → Exemplos → Contexto. Markdown para seções + XML para delimitar conteúdo.
- Modelos GPT (não-raciocínio) precisam de instruções mais explícitas; modelos de raciocínio, de objetivo + restrições + contrato de saída.
- Leia `output_text` (agrega texto) — não assuma `output[0].content[0].text`.
- Fixe **snapshots** em produção; versione prompts em código (o objeto de prompts reutilizáveis `v1/prompts` foi descontinuado; desligamento anunciado para 30/11/2026).

**Raciocínio (F26)**
- `reasoning.effort`: `none | minimal | low | medium | high | xhigh | max` (suporte varia por modelo; muitos defaultam para `medium`). Comece em `medium`; `high`/`xhigh` só com ganho medido.
- Tokens de raciocínio são cobrados como saída e contam em `max_output_tokens` — reserve ≥ 25.000 ao começar; `status: "incomplete"` pode ocorrer antes de qualquer texto.
- Em function calling, devolva todos os itens de raciocínio, chamadas e outputs desde a última mensagem do usuário (ou use `previous_response_id`). Sem armazenamento (`store: false`), reenvie `encrypted_content`.
- `phase` (`commentary` | `final_answer`) em mensagens do assistente em alguns modelos — preserve ao reenviar histórico, senão o modelo pode parar cedo.
- `reasoning.summary` (`auto`/`concise`/`detailed`) para resumos de raciocínio.

**Structured Outputs, avaliação e segurança**: ver `saida-estruturada.md`, `avaliacao.md`, `seguranca.md`. (A plataforma Evals legada e o Agent Builder têm desligamento anunciado para 30/11/2026; os princípios continuam válidos.)

```python
from openai import OpenAI
client = OpenAI()
r = client.responses.create(
    model="{{MODELO}}",
    reasoning={"effort": "medium"},
    instructions=SYSTEM_PROMPT,        # regras fixas
    input=[{"role": "user", "content": entrada_usuario}],  # dados do usuário aqui
)
print(r.output_text)
```

## 3. Google (Gemini) — F35, F36

- **System instruction** para restrições críticas, persona e formato (ou no início do prompt).
- Delimitadores consistentes: XML (`<role>`, `<constraints>`, `<context>`, `<task>`) **ou** Markdown — um só.
- Gemini 3: direto/eficiente por padrão — peça explicitamente estilo conversacional ou detalhado; evite linguagem persuasiva.
- Contexto longo: dados primeiro, pergunta no fim, âncora "Com base nas informações acima…".
- Recomendação forte de few-shot; formato consistente; sem número ótimo fixo.
- Raciocínio: Gemini 2.5/3 pensam internamente; "Pense muito bem antes de responder" aumenta o pensamento.
- Cláusulas úteis: data atual para buscas sensíveis ao tempo; data de corte de conhecimento; grounding estrito.
- Ferramentas: Google Search grounding para fatos recentes; **code execution para qualquer cálculo/contagem**.
- Amostragem: `temperature`, `topK`, `topP` (padrão 0,95), `stop_sequences`. Se um filtro devolve resposta padrão (fallback), tente temperatura maior.
- Structured output: subconjunto de JSON Schema; várias restrições ignoradas silenciosamente — valide no cliente (ver `saida-estruturada.md`).

```python
from google import genai
client = genai.Client()
r = client.models.generate_content(
    model="{{MODELO}}",
    contents=f"<context>\n{dados}\n</context>\n<task>{tarefa}</task>",
    config={"system_instruction": SYSTEM_PROMPT, "temperature": 0.2},
)
print(r.text)
```

Template de system instruction agêntico do Gemini (F35, resumido): antes de qualquer ação, raciocinar sobre (1) dependências e restrições na ordem políticas → ordem de operações → pré-requisitos → preferências do usuário; (2) risco da ação; (3) hipóteses abdutivas; (4) adaptação a resultados; (5) fontes de informação disponíveis; (6) precisão — citar a política aplicável; (7) completude; (8) persistência com limite de retries; (9) "inibir a resposta": agir só após raciocinar, pois ações não se desfazem.

## 4. Modelos abertos e outros provedores

Fontes localizadas mas **não verificadas na íntegra** (secao5-fontes-localizadas.md) — consulte antes de usar:
- **Chat templates** (Llama, Qwen, Hugging Face `apply_chat_template`): use sempre o template oficial do modelo; erros de template degradam muito o desempenho; function calling depende do formato de tools do template.
- **Saída estruturada**: Cohere (Structured Outputs, `strict_tools`), Mistral (JSON mode, structured output), DeepSeek (strict mode beta em tool calls). Em modelos locais, prefira decodificação restrita (Outlines, XGrammar, llama.cpp grammars, Guidance) — ver F16.
- **Guardrails** gerenciados: Amazon Bedrock Guardrails (ataques de prompt).
- Modelos pequenos: técnicas que dependem de escala (CoT, auto-otimização) podem falhar (F02, S5d); use instruções diretas + few-shot.

## 5. Portando prompts entre provedores

1. Mapeie roles: `system` (Anthropic) ↔ `developer`/`instructions` (OpenAI) ↔ `system_instruction` (Gemini).
2. Remova prefill (Claude 4.6+) e budget de thinking manual; traduza para effort/instruções.
3. Ajuste ênfase: remova CAIXA ALTA para Claude/Gemini 3; para modelos GPT não-raciocínio, explicite mais passos.
4. Reconverta schemas (regras de `required`/`additionalProperties` do OpenAI; restrições ignoradas no Gemini).
5. **Reavalie** formato e ordem de exemplos — não transferem entre modelos (F12, F13).
6. Rode o mesmo eval nos dois e compare antes de migrar.

# Saída estruturada (JSON, schemas, function calling)

Sumário: 1. Qual mecanismo · 2. Design de schema · 3. Regras OpenAI · 4. Regras Gemini · 5. Casos de borda · 6. Evidência (JSONSchemaBench) · 7. Exemplos de código

---

## 1. Qual mecanismo usar

| Necessidade | Mecanismo |
|---|---|
| Conectar o modelo a funções/dados/ações do sistema | **Function calling / tools** (modo strict quando disponível) |
| Formatar a **resposta final** para um parser/UI | **Structured output** (`json_schema`) |
| Modelo antigo sem suporte a schema | JSON mode + validação + retry |
| Saída simples para humano | Prosa/markdown — não force JSON |

- OpenAI: prefira Structured Outputs a JSON mode sempre que suportado; JSON mode garante JSON válido mas **não** o schema (F27).
- Gemini: structured output formata a resposta final; function calling executa ação durante a conversa (F36).
- Decodificação restrita > "responda em JSON" no prompt: prompt-only tem a menor conformidade e degrada em schemas difíceis (F16).
- Entre etapas de um pipeline/agente, schemas com enums **também são defesa** contra injeção: removem canais de texto livre (F37).

## 2. Design de schema

- Chaves com nomes claros; `title`/`description` nas chaves importantes — o modelo lê (F27, F36).
- Tipos fortes: `integer`, `enum`, `boolean` em vez de string livre.
- **Ordem das chaves é preservada**: coloque `raciocinio`/`passos` **antes** de `resposta` para obter benefício de CoT (F27; F16 usa {reasoning, answer}).
- Inclua campo/valor para "não aplicável"/"não encontrado" (`null`, enum `"desconhecido"`), senão o modelo inventa para preencher.
- Prefira schemas rasos; separe tarefas complexas em subtarefas.
- Mantenha schema e tipos do código sincronizados (Pydantic/Zod; checagem em CI) (F27).
- Escolha a estrutura por eval (F27).

## 3. Regras OpenAI Structured Outputs (doc coletada out/2026, F27)

- Ativar: `text: {format: {type: "json_schema", name, strict: true, schema}}` (Responses) — ou `response_format` em Chat Completions. Function calling: `strict: true` na função.
- Raiz deve ser `object` (não `anyOf`).
- **Todos os campos em `required`**; opcional = união com null: `"type": ["string", "null"]`.
- **`additionalProperties: false` em todo objeto.**
- Suportado: string, number, boolean, integer, object, array, enum, anyOf, `$defs`/`$ref`, recursão. Strings: `pattern`, `format` (date-time, time, date, duration, email, hostname, ipv4, ipv6, uuid). Números: min/max/exclusive/multipleOf. Arrays: minItems/maxItems.
- Não suportado: `allOf`, `not`, `if/then/else`, `dependentRequired`, `dependentSchemas`.
- Limites: ≤ 5.000 propriedades, ≤ 10 níveis de aninhamento, ≤ 1.000 valores de enum no total.
- Primeira requisição com schema novo tem latência extra (processamento); depois é cacheado.
- JSON mode: a palavra "JSON" precisa aparecer no contexto, senão erro/espaços em branco infinitos.

## 4. Regras Gemini (doc coletada out/2026, F36)

- `response_format` com `mime_type: "application/json"` e `schema` (Interactions API); SDKs aceitam Pydantic/Zod.
- Suportado: string, number, integer, boolean, object, array, null; `enum`, `format` (date-time, date, time), `minimum`/`maximum`, `items`, `prefixItems`, `minItems`/`maxItems`, `anyOf`, recursão, `additionalProperties`.
- **Ignorados silenciosamente** (não aplicados): `minLength`, `maxLength`, `minProperties`, `maxProperties`, `uniqueItems`, `contains` — inclusive os gerados automaticamente por Pydantic `Field(min_length=…)` ou Zod `.min()`. Valide no cliente.
- Schemas complexos demais → `400 INVALID_ARGUMENT` ("too many states"). Causas: `maxItems` grandes em arrays aninhados, nomes longos, enums enormes, muitas propriedades opcionais seguidas, `anyOf` com muitas alternativas, limites numéricos. Correção: simplificar, encurtar nomes, intercalar obrigatórios entre opcionais.
- Gemini 3 combina structured output com Search grounding, URL context, code execution e function calling.

## 5. Casos de borda — trate no código (F27, F36)

- **Recusa**: pode não seguir o schema; vem como `refusal` (OpenAI). Ramifique.
- **Incompleto**: `status: "incomplete"` / `max_output_tokens` — pode ocorrer antes de qualquer saída visível em modelos de raciocínio.
- **Entrada incompatível com o schema**: o modelo tenta preencher e alucina → diga no prompt o que retornar nesse caso.
- **JSON válido, conteúdo errado**: sempre valide semântica (faixas, consistência, referências cruzadas).
- Streaming: pedaços são JSON parcial; concatene/deixe o SDK fazer o parse.

## 6. Evidência (JSONSchemaBench, F16)

- 10 mil schemas reais. Decodificação restrita pode ser ~50% **mais rápida** que livre; cobertura de features varia ~2× entre frameworks; provedores fechados têm cobertura conservadora (subconjunto) mas alta conformidade.
- Qualidade: restrição melhorou acurácia em até ~4% com schema {reasoning, answer}.
- Restrições podem empurrar o modelo para fora da distribuição (ex.: forçado a omitir vírgula gerou "890000") — verifique features suportadas e teste.

## 7. Exemplos de código

Python — OpenAI (Responses + Pydantic):
```python
from pydantic import BaseModel
from openai import OpenAI

class Extracao(BaseModel):
    raciocinio: str
    categoria: str          # use Literal[...] para enum
    valor_total: float | None

client = OpenAI()
resp = client.responses.parse(
    model="{{MODELO}}",
    instructions="Extraia os campos da nota. Se um campo não existir no texto, use null.",
    input=texto_da_nota,
    text_format=Extracao,
)
dados = resp.output_parsed   # trate resp.output para refusal/incomplete
```

Python — Anthropic (tool como schema de saída):
```python
import anthropic
client = anthropic.Anthropic()
tool = {
  "name": "registrar_extracao",
  "description": "Registra os campos extraídos da nota fiscal.",
  "input_schema": {
    "type": "object",
    "properties": {
      "raciocinio": {"type": "string"},
      "categoria": {"type": "string", "enum": ["servico", "produto", "outro"]},
      "valor_total": {"type": ["number", "null"]}
    },
    "required": ["raciocinio", "categoria", "valor_total"]
  }
}
msg = client.messages.create(
    model="{{MODELO}}", max_tokens=2048,
    tools=[tool], tool_choice={"type": "tool", "name": "registrar_extracao"},
    messages=[{"role": "user", "content": f"<nota>{texto}</nota>"}],
)
dados = next(b.input for b in msg.content if b.type == "tool_use")
```
(Confira na doc atual se o modelo-alvo oferece structured outputs nativos e as restrições de `tool_choice` forçado com thinking ativo.)

Python — Gemini (google-genai):
```python
from google import genai
from pydantic import BaseModel
class Extracao(BaseModel):
    raciocinio: str
    categoria: str
    valor_total: float | None
client = genai.Client()
r = client.models.generate_content(
    model="{{MODELO}}", contents=texto,
    config={"response_mime_type": "application/json", "response_schema": Extracao},
)
dados = Extracao.model_validate_json(r.text)  # valida o que o Gemini ignora
```

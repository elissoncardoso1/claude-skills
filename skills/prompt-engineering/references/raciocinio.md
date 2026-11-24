# Raciocínio: CoT, modelos de raciocínio e técnicas de busca

Sumário: 1. Decisão rápida · 2. Modelos de raciocínio / thinking · 3. Chain-of-Thought manual · 4. Self-consistency · 5. Decomposição (least-to-most) · 6. ReAct · 7. Tree of Thoughts · 8. Quando o raciocínio atrapalha

---

## 1. Decisão rápida

| Situação | Técnica | Custo |
|---|---|---|
| Modelo com raciocínio nativo (Claude com thinking adaptativo, OpenAI reasoning, Gemini 2.5/3) | Objetivo + restrições + contrato de saída; ajuste `effort` | Médio |
| Modelo sem thinking, tarefa multi-etapa | CoT manual: raciocinar antes, resposta final em tag | Baixo |
| Resposta discreta (número, rótulo) e alto risco de erro | Self-consistency: 5–10 amostras, voto de maioria | 5–10× |
| Entradas mais longas/difíceis que os exemplos | Least-to-most: decompor, depois resolver em sequência | 2×+ |
| Precisa de fatos externos / agir no ambiente | ReAct (pensamento ↔ ação ↔ observação) | Variável |
| Exploração com decisões iniciais decisivas (planejamento, puzzles) | Tree of Thoughts (BFS/DFS com auto-avaliação) | ~100× CoT |
| Tarefa de um passo / consulta factual simples | Nenhuma — responder direto | — |

## 2. Modelos de raciocínio / thinking nativo

**Princípio comum (OpenAI F26, Anthropic F34, Gemini F35):** dê *objetivo claro, restrições fortes e contrato de saída explícito*, sem prescrever cada passo intermediário. O raciocínio do modelo costuma superar o plano que um humano escreveria ("pense com cuidado" frequentemente vence um passo a passo escrito à mão — F34).

- OpenAI: modelo de raciocínio é como "um colega sênior" (dê o objetivo); modelo GPT é "um júnior" (instruções explícitas) (F24).
- Trate `effort` como **botão de ajuste, não a principal forma de recuperar qualidade** (F26). Avalie `medium` vs `high`; só use níveis extremos quando evals mostrarem benefício.
- Para tarefas agênticas/pesquisa: defina **o que conta como pronto** e **como verificar** (F26).
- Não peça raciocínio visível em `<thinking>` em modelos com thinking nativo — pode ser recusado ou redundante; use o thinking (F34). Gemini 2.5/3: em geral não é necessário pedir plano no output; "Pense muito bem antes de responder" aumenta o pensamento (F35).
- Auto-verificação: "Antes de terminar, verifique sua resposta contra [critérios de teste]" funciona bem em código e matemática (F34). Exceção: modelos que já verificam bem sozinhos (ex.: Opus 5) superverificam com essa instrução herdada — remova.
- Superpensar: em effort alto, alguns modelos exploram demais. Use: "Ao decidir uma abordagem, escolha uma e comprometa-se. Só revisite decisões se surgir informação que contradiga diretamente seu raciocínio." (F34)
- Reduzir frequência de thinking (system prompts grandes): "Pensar adiciona latência e só deve ser usado quando melhorar significativamente a qualidade — tipicamente em problemas de várias etapas. Na dúvida, responda diretamente." (F34)
- Reflexão após ferramentas: "Após receber resultados de ferramentas, reflita sobre a qualidade deles e determine os próximos passos ideais antes de prosseguir." (F34)
- Sem thinking, alguns modelos (ex.: Opus 4.5) são sensíveis à palavra "think" — use "considere", "avalie", "raciocine sobre" (F34).
- Detalhes de API (adaptive thinking, `effort`, `reasoning.effort`, preservação de raciocínio entre chamadas) em `provedores.md`.

## 3. Chain-of-Thought manual (sem thinking nativo)

Evidência:
- CoT few-shot (F02): exemplos com raciocínio intermediário antes da resposta. PaLM 540B no GSM8K: ~18% → ~57%. **Emergente**: só ajuda a partir de ~100B parâmetros; modelos pequenos geram cadeias fluentes e ilógicas.
- Ablação (F02): só equação, só "tokens extras" ou raciocínio *depois* da resposta ≈ sem ganho. O que importa é raciocínio sequencial em linguagem natural **antes** da resposta.
- Zero-shot CoT (F03): "Vamos pensar passo a passo." MultiArith 17,7% → 78,7%. Gatilhos instrutivos funcionam; enganosos ("Não pense, apenas sinta") pioram. Use dois estágios: raciocinar → extrair a resposta num formato fixo.
- Sem ganho em senso comum (CommonsenseQA, StrategyQA) e em problemas de um passo (F03).

Template:
```
Resolva o problema abaixo. Primeiro raciocine passo a passo dentro de <raciocinio>. Depois dê apenas a resposta final dentro de <resposta>, no formato: {{formato}}.

<problema>
{{problema}}
</problema>
```
Em structured output, coloque o campo `raciocinio` **antes** de `resposta` no schema — a ordem das chaves é preservada (F27, F16).

## 4. Self-consistency (F04)

- Amostre várias cadeias de raciocínio com temperatura > 0 e faça voto de maioria na resposta final.
- GSM8K (PaLM-540B): 56,5 → 74,4 (+17,9). Ganhos também em SVAMP, AQuA, StrategyQA, ARC.
- **5–10 caminhos** capturam a maior parte do ganho; voto simples ≈ ponderado.
- A **taxa de concordância** correlaciona com acurácia → use como sinal de confiança/escalonamento (ex.: < 60% de concordância → revisar humano ou modelo maior).
- Requer conjunto de respostas discreto; para texto aberto, precisa de medida de concordância.
- Em modelos atuais, combine com prompts few-shot (no Prompt Report F14, SC só ajudou prompts zero-shot).

## 5. Decomposição — Least-to-Most (F05)

- Dois estágios: (1) decompor em subproblemas mais simples; (2) resolver em sequência, passando respostas anteriores adiante.
- Concatenação de últimas letras com 12 palavras: CoT 31,8% vs LtM 74,0%. SCAN: 99,7% vs 16,2% (CoT).
- Melhor quando o teste é **mais difícil que os exemplos** (generalização fácil→difícil).
- Prompts de decomposição **não generalizam entre domínios** — escreva exemplos de decomposição por domínio. A decomposição costuma ser "a maior parte do problema".
- Implementação: duas chamadas (planejar → resolver k dado 1..k-1) ou uma chamada com seções.

## 6. ReAct — raciocinar e agir (F06)

- Intercala `Pensamento → Ação (ferramenta) → Observação`. Base dos agentes com ferramentas atuais.
- CoT puro alucina (56% das falhas no HotpotQA); ReAct alucina menos, mas tem mais erros de raciocínio/loops e sofre com buscas pouco informativas (23% dos erros).
- Melhor: combinar. ReAct → fallback para CoT-SC se não houver resposta em N passos; CoT-SC → ReAct se a maioria tiver < n/2 votos.
- Prática: limite de passos, detecção de loop (mesma ação repetida), e ferramentas de busca com bons resultados (ver `ferramentas.md`).

## 7. Tree of Thoughts (F07)

- Busca sobre "pensamentos" com propostas, auto-avaliação de estados e backtracking.
- Game of 24 (GPT-4): CoT 4% → ToT 74%. Custo ≈ 100 amostras de CoT.
- Os próprios autores: "pode não ser necessário para muitas tarefas que o GPT-4 já resolve". Use só quando decisões iniciais são decisivas e há exploração real.

## 8. Quando o raciocínio atrapalha

- Em modelos modernos, zero-shot CoT pode **piorar**: no benchmark do Prompt Report (gpt-3.5-turbo, MMLU), Zero-Shot 0,627 vs Zero-Shot-CoT 0,547; Few-Shot-CoT foi o melhor (0,692) (F14).
- Modelos pequenos: CoT gera cadeias ilógicas (F02).
- Tarefas simples, latência crítica, classificação: raciocínio custa sem ganho.
- Raciocínio correto não é garantido mesmo com resposta certa (F02) — não use a cadeia como explicação confiável sem verificar.
- Conclusão: **meça** com e sem raciocínio na sua tarefa.

# Avaliação de prompts (evals)

Sumário: 1. Por que avaliar · 2. Critérios de sucesso · 3. Dataset · 4. Graders · 5. LLM-as-judge · 6. Protocolo de comparação · 7. Uso dos scripts

---

## 1. Por que avaliar

- Prompts são frágeis: formato (até 76 pontos — F13), ordem dos exemplos (~50%→~90% — F11, F12), palavra do gatilho (F03, F21) e modelo (prompts otimizados não transferem — F20 vs F21, S5d) mudam resultados.
- Sem eval, "melhorou" é impressão. Fixe snapshots de modelo em produção e rode evals ao iterar e ao trocar de modelo (OpenAI F24).
- Prompts em produção: versione em código (módulo de prompt builder perto da feature, argumentos tipados, fixtures/testes antes de mudar, rollout via feature flag) (F24).

## 2. Critérios de sucesso

Bons critérios são **específicos, mensuráveis, alcançáveis e relevantes**. Exemplos:
- "≥ 95% das extrações com todos os campos corretos no conjunto de validação de 50 notas."
- "Classificação com F1 macro ≥ 0,85; nenhuma confusão entre `urgente` e `rotina`."
- "Rubrica de 1–5 em fidelidade à fonte com média ≥ 4,5 e nenhuma nota < 3."
Inclua também latência, custo (tokens) e taxa de recusa/erro de formato.

## 3. Dataset (OpenAI F28; Anthropic F31)

- Colunas de entrada + colunas de verdade (ground truth) referenciáveis pelo prompt e pelos graders.
- Casos reais > sintéticos simplistas. Inclua: típicos, bordas, fora de escopo, adversariais (injeção), entradas longas.
- Dataset vivo: cada falha encontrada em produção vira caso.
- Anotação: bom/ruim, crítica em texto livre, colunas customizadas; **anotador especialista no domínio** se você não for um (F28).
- Separe **desenvolvimento** e **held-out** (teste) para não sobreajustar o prompt aos casos que você olhou (F31, F21).

## 4. Tipos de grader (F28)

| Grader | Uso | Exemplo |
|---|---|---|
| String/regex | Resposta exata, rótulos | saída == `ground_truth` |
| Código (Python) | Formato, contagens, validação de schema, faixas | JSON válido e ≤ 50 palavras |
| Similaridade (embeddings) | Paráfrase aceitável | cos ≥ 0,85 com referência |
| Modelo — rótulo | Classificar a saída | "concisa" vs "prolixa" |
| Modelo — nota | Rubrica | fidelidade 1–5 |
| Humano | Qualidade subjetiva, alto risco | revisão por especialista |

Prefira o grader mais barato e determinístico que mede o que importa. Verificadores não devem rejeitar respostas corretas por formatação (F31).

## 5. LLM-as-judge (F17)

- GPT-4 como juiz concordou com especialistas em 85% (sem empates), acima da concordância humano-humano (81%).
- **Vieses medidos:**
  - Posição: consistência ao inverter a ordem só 65% (GPT-4), 46% (GPT-3.5), 24% (Claude-v1).
  - Verbosidade: com ataque de "lista repetitiva", juízes fracos preferiram a resposta inflada em 91% dos casos.
  - Autopreferência: ~10% (GPT-4) a ~25% (Claude-v1) a mais de vitórias para si mesmo (inconclusivo).
  - Matemática: juiz aceitou resposta errada em 70% (prompt padrão), 30% (CoT), 15% (com referência).
- **Mitigações:**
  1. Avalie nas duas ordens; vitória só se consistente, senão empate (`scripts/pairwise_judge.py` faz isso).
  2. Juiz guiado por referência: gere/forneça a resposta correta primeiro, independente, e compare.
  3. Rubrica explícita com critérios separados e escala ancorada (o que é 1, 3, 5).
  4. Instrua: "não favoreça respostas mais longas; avalie apenas os critérios".
  5. Juiz de modelo forte e, se possível, de outra família que a do gerador.
  6. Exemplos few-shot no juiz aumentam consistência (65% → 77,5%) a ~4× o custo.
  7. Calibre o juiz contra uma amostra anotada por humanos antes de confiar.
- Template de juiz em `templates.md`.

## 6. Protocolo de comparação de variantes

1. Baseline: prompt atual (ou zero-shot simples) medido no dataset.
2. Uma mudança por variante; nomeie (`v2_exemplos_balanceados`).
3. Rode cada variante várias vezes se temperatura > 0; reporte média ± desvio.
4. Para comparações entre modelos/prompts, teste **2–3 formatos plausíveis** (F13).
5. Leia transcrições/saídas das falhas, não só a métrica.
6. Confirme no held-out antes de adotar.
7. Registre: versão do prompt, modelo e snapshot, parâmetros, data, resultado.

## 7. Uso dos scripts

- `scripts/eval_harness.py`: roda N variantes de prompt sobre um dataset JSONL com graders (`exact`, `contains`, `regex`, `json_schema`, `python`) e chamada de modelo plugável (Anthropic, OpenAI, Gemini ou `mock`). Gera relatório Markdown + JSON.
- `scripts/pairwise_judge.py`: compara duas saídas com juiz LLM nas duas ordens, com rubrica e referência opcional.
- `scripts/prompt_lint.py`: checagem estática de um prompt (sinais de problema comuns) antes de gastar tokens.

Rode `python scripts/<script>.py --help` para opções.

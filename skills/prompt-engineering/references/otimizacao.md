# Otimização automática de prompts

Sumário: 1. Quando vale a pena · 2. APE · 3. OPRO (e suas limitações) · 4. DSPy · 5. TextGrad · 6. Meta-prompting manual · 7. Receita prática

---

## 1. Quando vale a pena

Pré-requisitos: (a) métrica automática confiável, (b) dataset com ≥ dezenas de exemplos rotulados e split de validação, (c) modelo otimizador **forte**. Sem isso, iteração manual guiada por falhas é melhor.

Evidência geral: no estudo de caso do Prompt Report (F14), 47 passos manuais (~20 h) chegaram a F1 0,53; DSPy chegou a 0,548 e "superou bastante os prompts do engenheiro humano". Melhor resultado: **automação + revisão humana**.

## 2. APE — Automatic Prompt Engineer (F20)

- Um LLM propõe instruções candidatas a partir de pares entrada→saída; cada candidata é pontuada no conjunto de validação; fica a melhor.
- ≥ humano em 24/24 tarefas de Instruction Induction e 17/21 do BIG-Bench.
- Descobriu: "Let's work this out in a step by step way to be sure we have the right answer." (GSM8K 40,7 → 43,0 no InstructGPT).
- Iteração extra deu ganho marginal. Selecione no mesmo regime do deploy (zero-shot vs few-shot) — instrução escolhida em zero-shot pode piorar few-shot.
- Modelos propositores maiores geram instruções melhores e mais curtas (mais baratas de pontuar).

## 3. OPRO — LLMs como otimizadores (F21) e revisão (S5d)

- Meta-prompt com soluções anteriores + notas (ordem crescente) + exemplos da tarefa; otimizador propõe ~8 instruções por passo; avaliador pontua; repete.
- Até +8% no GSM8K e até +50% em tarefas do BBH sobre prompts humanos. "Take a deep breath and work on this problem step-by-step." = 80,2 com PaLM 2-L como avaliador.
- **Prompts otimizados são específicos do modelo**: a instrução do APE rendeu só 58,8 nesse avaliador.
- Temperatura 1,0 no otimizador, 0 no avaliador; vários candidatos por passo estabilizam; sobreajuste existe → early stopping e mais dados.
- **Revisiting OPRO (S5d)**: com modelos pequenos (LLaMA-2 7B–70B, Mistral 7B) como otimizadores, OPRO ficou **abaixo** de few-shot CoT (ex.: LLaMA-2-70B 27,98 vs 48,67). Recomendação: para modelos pequenos, instruções diretas e claras + few-shot CoT. **Não use modelo fraco para otimizar o próprio prompt.**

## 4. DSPy (F22)

- Programa declarativo: **assinaturas** (`pergunta -> resposta`), **módulos** (Predict, ChainOfThought, ReAct…) e **otimizadores** (BootstrapFewShot, random search…) que compilam o pipeline contra uma métrica e poucos exemplos (só rótulo final; demonstrações intermediárias são geradas automaticamente).
- GSM8K, GPT-3.5: vanilla 25,2 → CoT bootstrap 72,9 → + ensemble 81,6 (teste). Llama2-13b: 9,4 → 46,9.
- Use quando há pipeline multi-etapa e você prefere definir interfaces + métrica a ajustar strings.

```python
import dspy
dspy.configure(lm=dspy.LM("{{provedor/modelo}}"))

class Triagem(dspy.Signature):
    """Classifique a mensagem do cliente na categoria correta."""
    mensagem: str = dspy.InputField()
    categoria: str = dspy.OutputField(desc="uma de: cobranca, tecnico, cancelamento, outro")

programa = dspy.ChainOfThought(Triagem)
metrica = lambda ex, pred, trace=None: ex.categoria == pred.categoria
otimizador = dspy.BootstrapFewShotWithRandomSearch(metric=metrica, max_bootstrapped_demos=4)
compilado = otimizador.compile(programa, trainset=treino)
```
(Confira a API da versão instalada; nomes de otimizadores mudam entre versões.)

## 5. TextGrad (F23)

- "Diferenciação" via texto: feedback em linguagem natural de um LLM é retropropagado num grafo; variáveis podem ser prompts, soluções, código.
- Otimização de system prompt do gpt-3.5-turbo com GPT-4o como motor de "gradiente": Object Counting 77,8 (CoT) → 91,9. Refinamento em tempo de teste: GPQA 51 → 55%.
- Padrão útil: **modelo forte critica e reescreve o prompt de um modelo barato**; aceite a nova versão só se melhorar na validação.

## 6. Meta-prompting manual (sem framework)

Prompt para o modelo forte melhorar um prompt a partir de falhas:
```
Você é um engenheiro de prompts. Abaixo estão o prompt atual, o objetivo e exemplos de casos em que a saída falhou, com a saída esperada.

<objetivo>{{objetivo e critério de sucesso}}</objetivo>
<prompt_atual>{{prompt}}</prompt_atual>
<falhas>
  <caso><entrada>…</entrada><saida_obtida>…</saida_obtida><saida_esperada>…</saida_esperada></caso>
</falhas>

1. Em <diagnostico>, identifique a causa comum das falhas (instrução ausente, ambígua, conflitante, exemplo enganoso, formato).
2. Em <prompt_revisado>, reescreva o prompt com a menor mudança que corrige a causa, sem sobreajustar a esses casos específicos.
3. Em <riscos>, liste comportamentos que a mudança pode piorar.
```
Depois, valide no conjunto completo e no held-out.

## 7. Receita prática

1. Baseline manual claro (fundamentos) + eval.
2. Gere 10–20 variantes com um modelo forte (estilo APE) ou meta-prompt com falhas.
3. Pontue todas no dev set com `scripts/eval_harness.py`.
4. Top-3 → mais iterações (estilo OPRO/TextGrad) com early stopping.
5. Confirme no held-out; revise manualmente a vencedora (legibilidade, regras de negócio, segurança).
6. Revalide ao trocar de modelo.

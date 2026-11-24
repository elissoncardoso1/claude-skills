# Fundamentos de escrita de prompts

Sumário: 1. Clareza · 2. Contexto e motivação · 3. Estrutura e delimitadores · 4. Few-shot · 5. Controle de formato · 6. Papel/persona e apelos emocionais · 7. Sensibilidade a formato e ordem · 8. Parâmetros de amostragem · 9. Estratégias de iteração

---

## 1. Clareza

- Trate o modelo como "um funcionário brilhante, mas novo, sem contexto das suas normas" (Anthropic F34). Se você quer algo além do mínimo, peça explicitamente.
  - Fraco: `Crie um dashboard de analytics.`
  - Forte: `Crie um dashboard de analytics. Inclua o máximo de recursos e interações relevantes. Vá além do básico para uma implementação completa.`
- Modelos atuais seguem instruções **literalmente**. "Você pode sugerir mudanças?" gera sugestões; "Mude esta função para melhorar a performance" gera a mudança (F34). Escolha o verbo conforme o resultado desejado.
- Passos numerados quando ordem ou completude importam.
- Defina termos ambíguos ("curto" = até 3 frases; "recente" = após 2024) (Gemini F35).
- Gemini 3 / modelos recentes: evite linguagem persuasiva ou enfática desnecessária; seja preciso (F35).

## 2. Contexto e motivação

- Explique o *porquê* de cada regra não óbvia. O modelo generaliza a partir da razão:
  - Fraco: `NUNCA use reticências.`
  - Forte: `Sua resposta será lida por um sintetizador de voz, então nunca use reticências — ele não sabe pronunciá-las.` (F34)
- Diga quem consome a saída (cliente leigo, parser, outro agente, revisor técnico) e o que importa para essa pessoa.
- Forneça o material de referência em vez de supor que o modelo sabe ("Responda usando apenas o texto abaixo") (F35).
- "Mínimo não significa curto": dê toda a informação necessária, mas corte o que não muda comportamento (F30).

## 3. Estrutura e delimitadores

- Use **tags XML** quando o prompt mistura instruções, contexto, exemplos e variáveis: `<instrucoes>`, `<contexto>`, `<exemplos><exemplo>…</exemplo></exemplos>`, `<documentos><documento index="1"><fonte>…</fonte><conteudo>…</conteudo></documento></documentos>` (F34). Nomes descritivos e consistentes; aninhe quando houver hierarquia.
- Ou **Markdown** (`# Identidade`, `# Instruções`, `# Exemplos`, `# Contexto`). Escolha um padrão e mantenha em todo o prompt (F35).
- Atributos XML podem carregar metadados referenciáveis: `<avaliacao id="ex-1">` ↔ `<resposta id="ex-1">` (OpenAI F24).
- Ordem típica de um developer/system prompt (F24): Identidade → Instruções → Exemplos → Contexto (o contexto que muda por requisição vai no fim; o prefixo estável no início favorece **prompt caching**).
- Em prompts de sistema, o formato exato importa cada vez menos à medida que os modelos ficam mais capazes (F30) — mas a consistência ainda importa (ver §7).

## 4. Few-shot (exemplos)

Evidência: few-shot é a base da aprendizagem em contexto (F01); exemplos são o direcionador mais confiável de formato, tom e estrutura (F34); Gemini recomenda "sempre incluir few-shot" (F35).

Regras de design:

| Aspecto | Recomendação | Fonte |
|---|---|---|
| Quantidade | 3–5 como ponto de partida; mais costuma ajudar com retorno decrescente (~20); excesso causa sobreajuste ao exemplo | F34, F14, F35 |
| Diversidade | Cobrir bordas e variar superfície para evitar padrões não intencionais | F34, F30 |
| Formato | Idêntico entre exemplos e com a consulta (tags, espaços, quebras) | F35, F13 |
| Rótulos | Distribuição balanceada; rótulos corretos | F11, F14 |
| Ordem | Não agrupar a mesma classe no fim (viés de recência); a ordem pode variar ~50%→~90% e não transfere entre modelos | F11, F12 |
| Similaridade | Exemplos semelhantes à instância de teste ajudam (seleção dinâmica por embeddings) | F14 |
| Canônicos | Preferir poucos exemplos canônicos a uma lista exaustiva de casos de borda | F30 |

- Embrulhe: `<exemplos><exemplo>…</exemplo></exemplos>`.
- Peça ao modelo para avaliar a diversidade dos seus exemplos ou gerar mais (F34).
- Exemplos de **outra tarefa** com CoT pioram resultados; o dano é menor quando o formato da resposta coincide (F03).
- Com thinking ativo, exemplos multishot ainda funcionam: mostre problema → método → resposta (F34).
- Viés de modelo em classificação: maioria, recência e token comum. Se tiver logprobs, calibre com entrada vazia ("N/A") (F11).

## 5. Controle de formato de saída

1. Diga o que fazer: "Componha a resposta em parágrafos de prosa corrida" em vez de "não use markdown" (F34).
2. Indicadores em tags: "Escreva as seções em prosa dentro de `<prosa>`" (F34).
3. **Espelhe o estilo**: o estilo do prompt influencia o da resposta (menos markdown no prompt → menos na saída) (F34).
4. Preferências detalhadas quando necessário — bloco para reduzir bullets excessivos:

```
<evitar_markdown_excessivo>
Escreva conteúdo longo em parágrafos de prosa clara e corrida. Reserve markdown para `código inline`, blocos de código e títulos simples (##, ###). Não use listas numeradas ou com marcadores, a menos que (a) você apresente itens realmente discretos, em que lista é a melhor forma, ou (b) o usuário peça explicitamente uma lista ou ranking. Integre os itens em frases. Nunca produza uma série de bullets curtos demais.
</evitar_markdown_excessivo>
```

   Atenção: em modelos que já formatam pouco por padrão, esse bloco pode suprimir estrutura necessária (F34).

5. Extensão: especifique em unidades concretas (palavras, frases, parágrafos, itens). Modelos recentes variam: alguns são mais concisos por padrão, outros mais longos (Opus 5 tende a respostas longas) (F34). Gemini 3 é direto por padrão — peça "conversacional/detalhado" se quiser (F35).
6. Matemática: o padrão é LaTeX. Para texto puro: "Formate apenas em texto simples. Não use LaTeX, MathJax ou notações como \( \), $ ou \frac{}{}; use '/', '*' e '^'." (F34)
7. **Prefill** (pré-preencher o início da resposta do assistente) não é suportado no último turno a partir do Claude 4.6 (erro 400). Substitua por instruções de formato, structured output ou tags (F34). Gemini ainda aceita a "estratégia de completamento" (prefixo/padrão parcial que o modelo continua) (F35).
8. Saída programática vs interativa: se a saída vai para código, diga "apenas X, sem comentários nem cercas de código" — o modelo então não deve fazer perguntas nem adicionar texto (Model Spec F25).

## 6. Papel/persona e apelos emocionais

- Uma frase de papel no system prompt já direciona tom e foco ("Você é um assistente de programação especializado em Python.") (F34).
- Evidência controlada (S5a, 2026; 1.140 perguntas, 38 papéis): no agregado, **sem papel ≈ com papel** (d < 0,12). Papéis **aumentam profundidade técnica** (d = 0,54) mas **reduzem clareza** e alongam respostas; ajudam em perguntas consultivas e em medicina/psicologia; atrapalham em perguntas conceituais, finanças, direito e ciência.
  - Prática: use papel quando quer vocabulário/cautela de especialista; acrescente "seja claro e em linguagem simples" quando o público é leigo.
- EmotionPrompt (S5b, 2023): ganhos relatados em modelos antigos, muitas vezes em métrica relativa sobre bases baixas. Estudo de 2026 (S5c) com modelos atuais: prefixos emocionais estáticos "raramente produzem mudanças grandes". **Não use pressão emocional como técnica de qualidade.** "Respire fundo e resolva passo a passo" (OPRO F21) foi ótimo para um modelo específico (PaLM 2) — não é universal.

## 7. Sensibilidade a formato e ordem

- Mudanças semanticamente neutras (separadores, espaços, caixa, formatação de itens) causam variação de até 76 pontos (LLaMA-2-13B) e mediana ~7,5 pontos; persiste com mais exemplos, modelos maiores e instruction tuning; rankings de modelos podem inverter conforme o formato (FormatSpread, F13).
- Implicações:
  - Ao comparar dois prompts ou modelos, avalie **vários formatos plausíveis**, não um só.
  - Fixe um formato e mantenha-o idêntico entre exemplos e consulta.
  - Ao trocar de modelo, **reavalie** formato e ordem dos exemplos (F12, F13).
- Caso real (F14): duplicar acidentalmente um e-mail no prompt *melhorou* o F1; anonimizar nomes piorou. Moral: decisões de prompt são empíricas — teste, não presuma.

## 8. Parâmetros de amostragem

- `temperature`: baixa para determinismo/extração/classificação; alta para criatividade. 0 ≈ sempre o token mais provável (F35).
- `top_p` (padrão Gemini 0,95), `top_k` (1 = greedy). Ordem de filtragem no Gemini: topK → topP → temperatura (F35).
- `stop_sequences`: escolha sequências que não aparecem no conteúdo (F35).
- `max_output_tokens`: em modelos de raciocínio inclui os tokens de raciocínio — reserve folga (OpenAI recomenda começar com ≥25.000) (F26).
- Modelos de raciocínio podem não aceitar/ignorar temperature/top_p; confira a doc do modelo.
- 1 token ≈ 4 caracteres em inglês; 100 tokens ≈ 60–80 palavras (F35). Em português a razão é um pouco pior.

## 9. Estratégias de iteração (quando o prompt não funciona)

1. Leia as saídas ruins e classifique o erro antes de mudar algo.
2. Reformule a instrução (outra palavra, outra ordem).
3. Troque por tarefa análoga: classificação vira "questão de múltipla escolha" para manter a resposta nas opções (F35).
4. Reordene blocos: [exemplos][contexto][entrada] vs [entrada][exemplos][contexto] (F35).
5. Adicione ou troque um exemplo que mostre exatamente o comportamento falho corrigido.
6. Divida em etapas (chaining) se uma chamada faz coisas demais (F29, F35).
7. Mude uma coisa por vez e meça (ver `avaliacao.md`).

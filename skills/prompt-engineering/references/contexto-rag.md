# Engenharia de contexto, contexto longo e RAG

Sumário: 1. Conceito · 2. Posição e contexto longo · 3. Documentos e citações · 4. RAG · 5. Recuperação just-in-time · 6. Tarefas de longo horizonte · 7. Checklist

---

## 1. Conceito

- **Engenharia de contexto** = curar e manter o conjunto ideal de tokens durante a inferência: system prompt, ferramentas, MCP, dados externos, histórico, memória (Anthropic F30). É a evolução natural da engenharia de prompt: prompt é escrito uma vez; contexto é curado a cada chamada.
- Formalização (survey F15): C = A(instruções, conhecimento, ferramentas, memória, estado, consulta), otimizado sob |C| ≤ L_max.
- **Context rot**: quanto mais tokens, menor a precisão de recuperação — em todos os modelos, como gradiente, não precipício (F30). Contexto é recurso finito com retorno decrescente ("orçamento de atenção").
- Princípio-guia: **"o menor conjunto de tokens de alto sinal que maximize a probabilidade do resultado desejado"** (F30).

## 2. Posição e contexto longo

- "Lost in the middle" (F10): acurácia em curva em U — melhor com a informação relevante no início ou no fim; cai >20% no meio. Com 20–30 documentos e a resposta no meio, GPT-3.5 ficou **abaixo do desempenho sem documento nenhum**.
- Modelos com janela estendida "não são necessariamente melhores" em usar o contexto (F10).
- Leitores saturam antes da recuperação: 50 documentos em vez de 20 acrescentaram só ~1–1,5% (F10).
- Regras práticas:
  - Documentos longos (20k+ tokens) **no topo**; pergunta, instruções e exemplos **no fim** — até +30% em entradas multi-documento complexas (Claude, F34). Gemini: contexto primeiro, pergunta no final, com âncora "Com base nas informações acima…" (F35).
  - Repita a pergunta/instrução crítica depois do bloco longo (consulta antes e depois ajuda recuperação de chave-valor — F10).
  - Re-rankeie e trunque; prefira poucos trechos relevantes a muitos.
  - Restrições críticas, persona e formato no system prompt ou no início (F35).

## 3. Documentos e citações

Estrutura recomendada (F34):
```
<documentos>
  <documento index="1">
    <fonte>relatorio_2025.pdf</fonte>
    <conteudo>
      {{CONTEUDO}}
    </conteudo>
  </documento>
  ...
</documentos>

Primeiro, extraia em <citacoes> os trechos literais relevantes para a pergunta, cada um com o index do documento. Depois responda em <resposta> usando apenas essas citações. Se não houver evidência suficiente, diga isso explicitamente.

Pergunta: {{PERGUNTA}}
```
- "Citar antes de responder" ancora a resposta e reduz alucinação.
- Grounding estrito (cláusula Gemini F35, adaptada): "Você é um assistente estritamente fundamentado no contexto fornecido. Use **apenas** fatos mencionados diretamente nele; não use conhecimento próprio. Se a resposta exata não estiver escrita no contexto, diga que a informação não está disponível."
- Inclua data atual e data de corte de conhecimento quando a pergunta for temporal (F35).

## 4. RAG (Retrieval-Augmented Generation)

- RAG original (F09): memória paramétrica + índice denso; reduz alucinação (humanos acharam RAG mais factual em 42,7% vs 7,1% do BART) e permite **atualizar conhecimento trocando o índice** sem retreinar.
- BM25 venceu recuperação densa em tarefas centradas em entidades → considere **busca híbrida** (lexical + vetorial).
- Mais documentos nem sempre é melhor; ajuste top-k por avaliação.
- Prompt do gerador: delimitar trechos, pedir citação por index, definir comportamento sem evidência, separar instruções de conteúdo recuperado (conteúdo recuperado é **não confiável** — ver `seguranca.md`).
- Arquiteturas (F15): RAG modular, agêntico (o modelo decide quando e o que buscar), em grafo.

## 5. Recuperação just-in-time (agentes)

- Tendência: sair da recuperação pré-inferência por embeddings para **contexto just-in-time** — o agente mantém identificadores leves (caminhos, queries, links) e carrega dados via ferramentas (F30).
- Metadados carregam sinal: hierarquia de pastas, nomes, datas, tamanhos (`tests/test_utils.py` ≠ `src/core/test_utils.py`).
- **Divulgação progressiva**: descobrir contexto camada a camada; guardar só o necessário.
- Estratégia **híbrida**: algo carregado de antemão (ex.: CLAUDE.md/AGENTS.md) + exploração com glob/grep sob demanda. Boa para domínios menos dinâmicos (jurídico, financeiro).
- Custo: exploração em tempo de execução é mais lenta e exige boas ferramentas e heurísticas.

## 6. Tarefas de longo horizonte (F30, F34)

| Técnica | Como | Quando |
|---|---|---|
| **Compactação** | Resumir conversa perto do limite e reiniciar com o resumo (manter decisões de arquitetura, bugs abertos, detalhes de implementação; descartar saídas redundantes) | Diálogo extenso de ida-e-volta. Ajuste o prompt de compactação maximizando recall primeiro, depois precisão |
| **Limpeza de resultados de ferramentas** | Remover outputs antigos de tools | Forma mais leve de compactação |
| **Notas estruturadas / memória** | Agente escreve NOTES.md, to-do, progress.txt fora da janela e relê depois | Desenvolvimento iterativo com marcos claros |
| **Subagentes** | Subagentes com janelas limpas retornam resumos de ~1.000–2.000 tokens ao agente líder | Pesquisa complexa com exploração paralela |

Prompt para ambientes com compactação automática (F34, adaptado):
```
Sua janela de contexto será compactada automaticamente ao se aproximar do limite, permitindo continuar indefinidamente. Portanto, não encerre tarefas cedo por preocupação com orçamento de tokens. Ao se aproximar do limite, salve progresso e estado na memória antes da renovação do contexto. Seja persistente e conclua a tarefa por completo.
```
- Estado estruturado (resultados de testes, status de tarefas) em JSON; notas de progresso em texto livre; **git** para log e checkpoints (F34).
- Em janelas novas, é comum ser melhor recomeçar lendo o estado do sistema de arquivos do que compactar: "Rode pwd. Revise progress.txt, tests.json e o git log. Rode um teste de integração básico antes de implementar novas funcionalidades." (F34)
- Claude 5.1+: mantenha o histórico **append-only**; editar mensagens anteriores, reconstruir `system`/`tools` ou resumir turnos in-place invalida blocos de thinking posteriores — use mensagens de sistema no meio da conversa e gerenciamento de contexto do servidor (F34).

## 7. Checklist de contexto

- [ ] Cada bloco do contexto muda o comportamento? Remova o resto.
- [ ] Informação crítica no início/fim, não no meio?
- [ ] Documentos com fonte/índice, delimitados, marcados como dados?
- [ ] Top-k e chunking ajustados por avaliação?
- [ ] Comportamento definido para "sem evidência"?
- [ ] Para agentes longos: estratégia de compactação/notas/subagentes escolhida e comunicada ao modelo?

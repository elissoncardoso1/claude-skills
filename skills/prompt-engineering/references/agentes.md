# Prompts para agentes e sistemas agênticos

Sumário: 1. Workflows vs agentes · 2. Padrões de workflow · 3. Anatomia do system prompt de agente · 4. Persistência, planejamento e progresso · 5. Ação vs conservadorismo · 6. Autonomia e segurança de ações · 7. Ferramentas em paralelo · 8. Subagentes · 9. Código: escopo, testes, alucinação · 10. Multi-janela · 11. Skills (SKILL.md)

---

## 1. Workflows vs agentes (Anthropic F29)

- **Workflow**: LLMs e ferramentas orquestrados por caminhos de código predefinidos — previsível, consistente.
- **Agente**: o LLM dirige dinamicamente seu processo e uso de ferramentas — flexível, mais caro, erros compostos. Na prática: "LLMs usando ferramentas com base em feedback do ambiente, em loop".
- Regra: **a solução mais simples possível**. Muitas aplicações resolvem com uma chamada otimizada + recuperação + exemplos. Adicione complexidade só quando melhora resultados de forma demonstrável.
- Frameworks escondem prompts e respostas; comece com a API direta e entenda o código por baixo.
- Três princípios: simplicidade; transparência (planejamento visível); interface agente-computador (ACI) cuidadosa.
- Agentes rendem mais em tarefas com conversa + ação, critério de sucesso claro, ciclos de feedback e supervisão humana (suporte ao cliente, código com testes).

## 2. Padrões de workflow (F29)

| Padrão | Use quando | Dica de prompt |
|---|---|---|
| **Prompt chaining** | Tarefa decomponível em subtarefas fixas | "Gates" programáticos entre etapas; cada prompt faz uma coisa |
| **Routing** | Categorias distintas, classificação precisa | Classificador com saída enum; prompts especializados por rota; rotear fácil→modelo barato, difícil→modelo forte |
| **Paralelização — seções** | Subtarefas independentes | Uma chamada responde, outra filtra conteúdo; cada aspecto em sua chamada |
| **Paralelização — votação** | Precisa de confiança | Vários prompts revisam o mesmo código; limiar de votos |
| **Orchestrator-workers** | Subtarefas não previsíveis | Orquestrador decompõe e sintetiza; workers recebem objetivo, formato de retorno e limites |
| **Evaluator-optimizer** | Critérios claros e iteração gera valor | Avaliador com rubrica; gerador recebe feedback; limite de rodadas |

O chaining mais comum: **rascunho → revisão contra critérios → refinamento**, cada passo uma chamada separada para logar, avaliar ou ramificar (F34).

## 3. Anatomia do system prompt de agente

Na "altitude certa" (F30), com seções delimitadas:

```
<papel_e_objetivo>        quem é, para quem trabalha, missão
<contexto>                ambiente, usuários, sistemas, restrições de negócio
<ferramentas>             quando usar cada uma (complementa as descrições das tools)
<fluxo_de_trabalho>       planejar → executar → verificar → reportar
<criterio_de_pronto>      o que precisa ser verdade para encerrar; como verificar
<limites_de_autonomia>    o que pode fazer sozinho; o que exige confirmação; o que é proibido
<formato_de_saida>        relatório final, atualizações de progresso
<exemplos>                1–3 trajetórias canônicas, se necessário
```
Processo (F30): teste um prompt mínimo no melhor modelo disponível; acrescente instruções e exemplos a partir dos modos de falha observados.

Template completo em `templates.md`.

## 4. Persistência, planejamento e progresso

- Persistência (OpenAI F24, adaptado): "Você é um agente: continue até a solicitação do usuário estar completamente resolvida antes de encerrar o turno. Decomponha a solicitação em todos os sub-pedidos e confirme que cada um foi concluído. Só encerre quando tiver certeza de que o problema está resolvido."
- Planejamento: "Planeje antes de cada chamada de ferramenta relevante e reflita sobre o resultado de cada uma." Use uma ferramenta de TODO ou rubrica (F24).
- Preâmbulos: "Antes de chamar uma ferramenta, explique brevemente por quê" — apenas em passos notáveis (F24).
- Visibilidade: modelos recentes podem pular resumos após ferramentas. Para mais transparência: "Após concluir uma tarefa com ferramentas, dê um resumo rápido do que foi feito." (F34)
- Modelos que escrevem poucas atualizações (ex.: Fable 5.1): peça explicitamente texto de progresso e remova instruções de brevidade (F34).
- Gemini (F35) — dimensões agênticas que você pode direcionar: decomposição lógica, diagnóstico abdutivo, exaustividade; adaptabilidade (seguir plano vs pivotar), persistência e recuperação (risco de loop), avaliação de risco (leitura vs escrita); ambiguidade e permissões, verbosidade, precisão.
- Persistência em erros (F35): em erros **transitórios**, tente de novo até um limite explícito; em outros erros, mude estratégia ou argumentos em vez de repetir a mesma chamada.

## 5. Ação vs conservadorismo (F34)

Proativo:
```
<agir_por_padrao>
Por padrão, implemente as mudanças em vez de apenas sugeri-las. Se a intenção do usuário não estiver clara, infira a ação mais útil provável e prossiga, usando ferramentas para descobrir detalhes ausentes em vez de adivinhar.
</agir_por_padrao>
```
Conservador:
```
<nao_agir_antes_de_instrucoes>
Não comece a implementar nem altere arquivos a menos que seja claramente instruído. Quando a intenção for ambígua, prefira fornecer informação, pesquisar e recomendar. Só edite ou implemente quando o usuário pedir explicitamente.
</nao_agir_antes_de_instrucoes>
```
- Superdisparo: modelos recentes respondem fortemente ao system prompt. Troque "CRITICAL: você DEVE usar esta ferramenta quando…" por "Use esta ferramenta quando…"; troque "Na dúvida, use [ferramenta]" por "Use [ferramenta] quando ela melhorar sua compreensão do problema." (F34)
- Gemini (F35): para ações exploratórias, parâmetros opcionais ausentes são risco BAIXO — "prefira chamar a ferramenta com a informação disponível a perguntar ao usuário, a menos que a informação seja necessária depois".

## 6. Autonomia e segurança de ações

Bloco de reversibilidade (F34, adaptado):
```
Considere a reversibilidade e o impacto potencial das suas ações. Ações locais e reversíveis (editar arquivos, rodar testes) estão liberadas. Para ações difíceis de reverter, que afetam sistemas compartilhados ou que possam ser destrutivas, peça confirmação antes:
- Destrutivas: apagar arquivos ou branches, dropar tabelas, rm -rf.
- Difíceis de reverter: git push --force, git reset --hard, alterar commits publicados.
- Visíveis a terceiros: enviar mensagens, comentar em PRs/issues, publicar, alterar infraestrutura compartilhada.
Diante de obstáculos, não use ações destrutivas como atalho (ex.: --no-verify, descartar arquivos desconhecidos que podem ser trabalho em andamento).
```
Escopo de autonomia (OpenAI Model Spec F25): defina sub-objetivos permitidos, efeitos colaterais aceitáveis (tempo, dinheiro, dados, acesso), quando pausar para aprovação, e **condição de término** (limite de tempo é boa prática). Estrutura sugerida: `allowed_tools`, `latest_time`, `max_cost`, `tool_constraints`, `additional_details`. Sem atalhos: não delegar ação proibida a outro agente, não editar o próprio escopo. Subagentes herdam o escopo e pedidos de parada.

Mínimo privilégio sem exagero: escopo estreito demais faz o usuário aprovar tudo no automático (F25).

## 7. Ferramentas em paralelo (F34)

```
<chamadas_paralelas>
Se você pretende chamar várias ferramentas e não há dependências entre elas, faça todas as chamadas independentes em paralelo. Ex.: ao ler 3 arquivos, faça 3 chamadas simultâneas. Se uma chamada depende do resultado de outra para definir parâmetros, faça-as em sequência. Nunca use placeholders nem adivinhe parâmetros ausentes.
</chamadas_paralelas>
```
- Pode elevar o paralelismo a ~100%. Para reduzir: "Execute as operações em sequência, com pausas breves entre cada passo."
- Em loops longos de alguns modelos, reenvie essa instrução como mensagem de sistema após cada rodada de resultados (F34).

## 8. Subagentes

- Modelos recentes delegam sozinhos; o risco é **excesso** (subagente para um grep).
```
Use subagentes quando as tarefas puderem rodar em paralelo, exigirem contexto isolado ou envolverem frentes independentes que não compartilham estado. Para tarefas simples, operações sequenciais, edições em um único arquivo ou quando precisar manter contexto entre passos, trabalhe diretamente.
```
- Briefing de subagente: objetivo, o que já foi descartado, onde procurar, formato e tamanho do retorno (resumo condensado de ~1–2k tokens — F30), limites.

## 9. Código: escopo, testes, alucinação (F34, F24)

- Anti-superengenharia: "Evite superengenharia. Faça apenas mudanças pedidas ou claramente necessárias. Sem features, refatorações ou 'melhorias' além do pedido; sem docstrings/comentários/tipos em código não alterado; sem tratamento de erro para cenários impossíveis — valide só nas fronteiras do sistema; sem abstrações para operações únicas. A complexidade certa é o mínimo necessário para a tarefa."
- Anti-gaming de testes: "Escreva uma solução geral e de alta qualidade que funcione para todas as entradas válidas, não só para os testes. Não fixe valores no código. Testes verificam correção, não definem a solução. Se a tarefa for inviável ou um teste estiver errado, informe em vez de contornar."
- Anti-alucinação: "Nunca especule sobre código que você não abriu. Se o usuário citar um arquivo, leia-o antes de responder. Não faça afirmações sobre o código antes de investigar."
- Exija validação: ferramentas como `apply_patch` podem retornar "Done" mesmo falhando (F24). Dê ferramentas de verificação (testes, browser, screenshots) para UI.
- Limpeza: "Se criar arquivos temporários para iteração, remova-os ao final."
- Frontend sem orientação tende ao visual genérico; especifique tipografia, cor, movimento e fundos, e peça explicitamente animações e interatividade (F34).

## 10. Trabalhos em várias janelas de contexto (F34)

1. Prompt diferente para a **primeira janela**: montar o framework (testes, scripts de setup); depois iterar sobre uma lista de tarefas.
2. Testes primeiro em formato estruturado (`tests.json`); "É inaceitável remover ou editar testes, pois isso pode esconder funcionalidade faltante ou com bug."
3. Scripts de conveniência (`init.sh`) para subir servidores, testes e linters.
4. Considere recomeçar do zero lendo estado do disco em vez de compactar.
5. "Esta é uma tarefa muito longa; planeje com clareza. Você pode usar todo o seu contexto de saída — só não fique sem contexto com trabalho significativo não commitado."

## 11. Skills (SKILL.md) — prompt engineering para agentes reutilizáveis (F32, F33)

- Estrutura: `nome-da-skill/SKILL.md` (+ `scripts/`, `references/`, `assets/`).
- Frontmatter: `name` (1–64 caracteres, minúsculas/dígitos/hífen, igual ao nome da pasta) e `description` (1–1024 caracteres; **o que faz e quando usar**, com palavras-gatilho). Opcionais: `license`, `compatibility`, `metadata`, `allowed-tools` (experimental).
- Divulgação progressiva: metadados (~100 tokens) sempre carregados → corpo do SKILL.md (< 5.000 tokens, < 500 linhas) quando ativada → arquivos de referência sob demanda (um nível de profundidade).
- A `description` decide o disparo: bom = "Extrai texto e tabelas de PDFs, preenche formulários e mescla PDFs. Use ao trabalhar com documentos PDF ou quando o usuário mencionar PDFs, formulários ou extração." Ruim = "Ajuda com PDFs."
- Código determinístico vai em `scripts/` (executa sem carregar no contexto); deixe claro se o agente deve **executar** ou **ler** o script.
- Comece por avaliação: rode tarefas representativas, ache lacunas, construa incrementalmente; peça ao agente para registrar abordagens bem-sucedidas e erros comuns na skill.
- Segurança: audite skills de terceiros (scripts, dependências, chamadas de rede).

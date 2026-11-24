# Changelog — filmcraft-agent

## 0.1.0 — 2026-11-12
- Versão inicial: SKILL.md (10 receitas, pré-checagem, confirmações, tabela de erros), references/{cli,mcp,limitacoes}.md,
  scripts/doctor.sh, scripts/fc_mcp.py. Baseada em filmcraft-cli 0.19.0, com evidências em docs/recon/.

## 0.2.0 — 2026-11-12 (Fase 6, rodada 1: 8/8 tarefas PASS; correções a partir dos problemas relatados pelo avaliador)
- R2 reescrita: dois cortes por faixa (`track` explícito em V1 e A1), de onde vêm os ids, religar o sync-lock (antes: razor sem
  track, que também cortava a música, e um corte só). Verificado em R11/R11b.
- Regra 3: resumo do `inspect` em uma linha; resultados `null`; legendas via `captions.list`.
- R1: `clip.fitToFrame` para clipes de tamanho diferente (verificado em R12).
- R3: `position` em pixels da sequência; exemplo para 720p; as propriedades de texto não aparecem no inspect.
- R5: keyframes acompanham o clipe movido (verificado em R09; corrige uma afirmação errada em limitacoes.md); `frame=`; definição de "fim do clipe".
- R9: `language=` no `captions.import` (R12); o OTIO não leva legendas (R13).
- R10: o export via MCP com `wait` ainda traz `job`/`poll`, e é o `result` que indica o fim; `FILMCRAFT_DATA_DIR` para o fc_mcp.py.
- §4: refazer um arquivo gerado na própria tarefa não exige confirmação.
- Tabela de erros: `timeline.move` sobrescreve (novo, R09); detecção de offline; arquivos `.lock`; a linha `exported` no stderr.

## 0.3.0 — 2026-11-12 (Fase 6, rodada 2: 4/4 PASS; correções)
- Regra 2: exceção para `timeline.move.moves[].time` (objeto `{seconds}` aceito; `seconds` solto rejeitado). Antes, a regra dizia
  "nunca" e induziu um erro.
- Nova receita R5b (mover um clipe com o áudio vinculado para outra faixa: `linked=false` + uma entrada por clipe; `overwritten[]` vazio).
- `render --frame` é ignorado em silêncio: documentado em R5 e cli.md (confirmado: renderizou 0 s, saída 0).
- R1: `probe` para saber o tamanho da mídia; `clip.fillFrame` além de `clip.fitToFrame`.
- R5: explica o "kept there even outside the clip" do describe.

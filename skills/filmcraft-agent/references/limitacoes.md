# Limitações e pontos frágeis

## Versões
- Verificado com **filmcraft-cli 0.19.0** (commit `d1af238b`). O app instalado na verificação era **0.20.1** (`cedf0c9b`); o bridge
  CLI 0.19.0 → app 0.20.1 funcionou. Outras combinações não foram testadas. `scripts/doctor.sh` avisa quando as versões diferem.
- Recursos não documentados (sintaxe `--opção=valor`, `-V`, `portable.txt`, `FILMCRAFT_DATA_DIR`, extensão acrescentada, progresso
  MCP…) podem mudar entre versões.

## Cobertura
- 35 dos 718 comandos do motor foram executados. Os demais seguem só a auto-descrição (`describe`). Confira os parâmetros e o
  resultado com `inspect` antes de confiar.
- Não executados: `--range inOut|workArea`, `--quality`, `--settings` válido, `inspect all` explícito, `FILMCRAFT_CONTROL_PORT`
  (app), a restauração do playhead pelo `render_frame` em bridge, e os formatos prores/dnxhr/apv/mjpeg/mxf/gif/aiff/aac/mp3 no export.
- Exemplos de bridge usaram `--data-dir` temporário e `--empty --no-recover`; o comportamento com o diretório de dados real do app
  não foi observado.

## Comportamentos frágeis
- **Params não validados:** chave errada → ignorada em silêncio (a edição cai no playhead/0). Sempre `inspect` depois.
- `time` como objeto é ignorado; use `seconds`/`timecode` no topo.
- Ripple esbarra em faixas com sync-lock; razor sem `track` corta **todas** as faixas (inclusive a música).
- Keyframes são criados no tempo da sequência, guardados relativos ao clipe e **acompanham** o clipe movido com `timeline.move`
  (verificado). Mudar a velocidade não foi verificado quanto ao reposicionamento dos keyframes.
- `timeline.move` sobrescreve clipes no destino, inclusive na faixa de áudio vinculada (`overwritten[]` no resultado).
- O OTIO não leva as legendas e não avisa; `inspect sequence` não mostra legendas nem as propriedades de texto.
- O undo não atravessa execuções do CLI.
- `ui_click` com id inexistente não diz "id desconhecido" (dá timeout); `ui_key Cmd+Z` com foco em texto não desfaz.
- O export com mídia offline **grava** o arquivo com placeholders e sai com 1: não use o arquivo antes de corrigir.

## Fora de escopo / não suportado
- Não há prompts MCP, nem transporte HTTP (só stdio).
- Não há sandbox de caminhos: o CLI e o MCP escrevem onde o comando mandar.
- O CLI não vem no `.app`; instalar ou atualizar exige compilar o código (cargo).

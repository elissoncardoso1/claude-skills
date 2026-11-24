# filmcraft-cli 0.19.0 — referência enxuta

`filmcraft-cli [OPÇÕES] <SUBCOMANDO> [ARGS]`. As opções valem em qualquer posição; `--opção=valor` também funciona; `--` encerra
as opções. `<sub> --help` mostra sempre a ajuda global.

## Subcomandos
| Subcomando | Uso | Notas |
|---|---|---|
| `exec <id> [k=v …]` ou `exec <id> '<json>'` | executa um comando do motor e imprime o resultado JSON | `k=v`: o valor é lido como JSON quando possível; `a.b=1` → `{"a":{"b":1}}` |
| `run <arq.jsonl \| ->` | uma linha `{"id","params"}` por comando; `#` comenta | sem `--keep-going`, a 1ª falha → saída 1 e nada é gravado; com ele, grava as boas e sai 1 |
| `commands [filtro] [--json]` | catálogo (id, rótulo, atalho, params) | o filtro procura no id e no rótulo |
| `describe <id>` | um comando em JSON, com `enabled` | id desconhecido → 1 |
| `inspect [project\|sequence]` | estado em JSON (os dois, por padrão) | outro valor → 2 |
| `import <arq>…` | importa (caminhos tornados absolutos) | falha parcial → 0 com `errors[]` |
| `export <saída> […]` | exporta a sequência ativa e espera | ver abaixo |
| `export --list-presets [consulta]` | presets (embutidos + do usuário no diretório de dados) | |
| `render [--seconds S] [--out f.png] [--scale F] [--allow-offline]` | um quadro do Program | padrões: 0 s, `frame.png`, 1.0; não funciona com `--bridge` |
| `probe <mídia> [--image-sequence]` | metadados JSON | |
| `bench-decode <mídia> [--frames N]` | fps de decodificação | padrão 120 quadros |
| `mcp [--project P \| --demo] [--data-dir D] \| --bridge ADDR` | servidor MCP em stdio | outra opção → 2 |
| `help`, `-h`, `--help` · `--version`, `-V`, `version` | | |

## Opções globais
`--project P` (abre) · `--demo` · `--save` (grava no `--project`; trava `.<nome>.fcproj.lock`; execuções concorrentes esperam) ·
`--save-as P` · `--bridge 127.0.0.1:PORTA` (+ `FILMCRAFT_CONTROL_TOKEN`; incompatível com `--project`/`--demo`) · `--data-dir D` ·
`--keep-going` · `--compact`.

## export
`--preset NOME` · `--format F` · `--range entire|inOut|workArea` · `--start S --end S` (sempre os dois) · `--settings '<ExportSettings JSON>'` ·
`--gpu-rendering auto|off` · `--scale F` · `--quality 0-100` · `--no-audio` · `--queue` · `--allow-offline`.

Formatos: `h264 hevc prores dnxhr apv mjpeg mxf-op1a mxf-opatom png tiff bmp gif wav aiff aac mp3`.
Deduzidos da extensão: mp4/m4v→h264 · mov→prores · mxf→mxf-op1a · png · gif · wav · tif/tiff · bmp · aif/aiff→aiff · m4a/aac→aac ·
mp3. Outra extensão sem `--format`/`--preset` → 2.
O resultado traz `path` (o arquivo real: pode ter uma extensão acrescentada, ex. `b.mov.mp4`), `offlineMedia[]` e `warnings[]`.
PNG/TIFF/BMP geram sequência numerada: `x.png` → `x000.png…` (`path` = primeiro, `lastPath` = último).
Comando `file.exportMedia` (via `exec`/MCP): também aceita `jpg tga dpx exr flac`; **não** deduz pela extensão (padrão h264).

## Códigos de saída
0 ok (também com stdout fechado) · 1 falha do comando, `run` com falha, export/render com mídia offline (o arquivo é gravado) ·
2 erro de uso.

## Ambiente e dados
- `FILMCRAFT_DATA_DIR`: diretório de dados se `--data-dir` faltar. Ordem: `--data-dir` → env → `<pasta do exe>/data` (se houver
  `portable.txt`) → `~/Library/Application Support/FilmCraft`.
- `FILMCRAFT_CONTROL_TOKEN`: 64 hex, igual no app.

## Tempo
254 016 000 000 ticks/s. Os params de comandos aceitam `seconds=`, `frame=` e `timecode=HH:MM:SS:FF` no topo, mesmo quando o `describe`
só mostra `time`. No topo, `time` aceita **apenas ticks** (um objeto é ignorado). Exceção: os itens de `timeline.move.moves[]` usam
`"time":{"seconds":n}` ou ticks. O subcomando `render` só tem `--seconds` (`--frame` é ignorado em silêncio).

## Comandos mais usados (params do catálogo)
| id | params essenciais |
|---|---|
| `file.newSequence` | `name, width, height, fps, sampleRate, video, audio` |
| `file.open` / `file.save` / `file.saveAs` | `path` |
| `timeline.place` | `item` ou `items[]`, `track` (`V1`, `A2`, `new`), `seconds`, `insert`, `sourceIn`, `duration`, `video`, `audio`, `matchSequence` |
| `timeline.razor` | `seconds`, `track?` (sem track = todas), `clip?` |
| `timeline.delete` | `clips[]`/`clip`, `ripple` |
| `timeline.setTrack` | `track`, `locked`, `syncLock`, `enabled`, `muted`, `solo`, `name`, `volumeDb`, `pan` |
| `timeline.select` | `clips[]`, `add`, `toggle`, `linked` |
| `graphics.newText` | `text, seconds (duração), track (índice 0), size, font, position, box` |
| `graphics.set` | `clip, props{font,font_style,size,align,fill_color,position,…}, time, keyframe` |
| `effects.list` / `effects.apply` | `kind` / `clips[], effect` |
| `effects.setParam` | `clip, effect (índice), param, value, seconds, keyframe` |
| `sequence.applyVideoTransition` | `clip, effect, frames, edge in/out, align` |
| `clip.audioGain` | `clips[], mode set/adjust/normalizeMax/normalizeAll, db` |
| `clip.speedDuration` | `clips[], speed (%), reverse, ripple, maintainPitch` |
| `clip.fitToFrame` / `clip.fillFrame` | `clips[]` (caber / preencher) |
| `timeline.move` | `moves[{clip, track, time:{seconds}\|ticks}]`, `insert`, `linked` (resultado: `moved[]`, `overwritten[]`) |
| `markers.add` | `target program/source, seconds, name, comment, color` |
| `media.relink` | `item, path, force` |
| `captions.import` / `captions.export` | `path` (formato pela extensão: srt vtt scc mcc stl ttml dfxp) |
| `file.exportInterchange` | `format edl/xml/fcpxml/otio/aaf/omf, path` |
| `export.presets.save` | `name, from, …overrides` (grava no diretório de dados) |
| `jobs.list` | — |

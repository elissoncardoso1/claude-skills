# Servidor MCP `filmcraft-cli mcp` — referência enxuta

stdio, JSON-RPC por linha; serverInfo `filmcraft 0.19.0`; capacidades `tools` e `resources` (sem prompts).
Início: `filmcraft-cli mcp [--project P | --demo] [--data-dir D]`, ou `FILMCRAFT_CONTROL_TOKEN=… filmcraft-cli mcp --bridge 127.0.0.1:PORTA`.
O projeto **não** é salvo sozinho. Quando o stdin fecha, o servidor termina (e exports em segundo plano se perdem).

## Ferramentas
| Ferramenta | Entrada | Resposta | Efeito |
|---|---|---|---|
| `command_list` | `filter?`, `enabled_only?` | `[{id,label,menu,shortcut,params,enabled}]` | leitura |
| `command_run` | `id`, `params?` | JSON do comando | escreve (undoable) |
| `command_batch` | `steps[{id,params?}]`, `stop_on_error?` (true) | `{completed, failed, results[{ok,result\|error}]}`; `isError` se algo falhou | escreve |
| `doc_inspect` | — | `{project, sequence}` | leitura |
| `project_inspect` | — | árvore (`root.children[{item,name,type,duration}]`, `activeSequence`, `path`) | leitura |
| `sequence_inspect` | — | `settings, video[], audio[] (items[{clip,start,duration,effects}]), markers, playhead, selection` | leitura |
| `media_import` | `paths[]` (**absolutos**), `bin?`, `image_sequence?` | `{errors[], items[]}` | escreve |
| `render_frame` / `render_preview` | `seconds?`, `max_side?` (960) | imagem PNG | leitura (em bridge: screenshot do Program) |
| `ui_inspect` | — | estado da UI | leitura, bridge |
| `ui_elements` | `prefix?` | `[{id,label,rect,enabled}]` (ex. `timeline.clip.19`, `tools.Razor`, `project.search`) | leitura, bridge |
| `ui_click` | `id` ou `x,y`; `button`, `count` 0–10, `modifiers` | `null` | bridge |
| `ui_drag` | `from`, `to` (`{id}` ou `{x,y}`), `steps` | `null` | bridge |
| `ui_key` | `key` (`Space`, `Cmd+K`…) | `null` | bridge |
| `ui_type` | `text` (no campo focado) | `null` | bridge |
| `ui_screenshot` | `panel?` (`Timeline`, `Program`…), `max_side?` (1600) | PNG | leitura, bridge |
| `ui_control` | `method`, `params?` | resultado do método | bridge |

Recursos: `filmcraft://document` (= doc_inspect) e `filmcraft://commands` (= command_list).

## Pontos críticos (verificados)
- `file.exportMedia` via `command_run`: passe **`format` e `wait:true`**. Sem `wait`, a resposta é `{job, poll:"jobs.list"}` e o
  arquivo não sai se a sessão terminar. Sem `format`, sai H.264 com `.mp4` acrescentado (`a.wav` → `a.wav.mp4`). Com
  `_meta.progressToken`, o servidor emite `notifications/progress` (quadros).
- Os argumentos de ferramentas são estritos (`-32602 unknown argument`); os `params` de comandos, não (chave errada é ignorada).
- Caminho relativo em `media_import` é gravado literalmente e resolvido a partir da pasta do `.fcproj`.
- Erros de comando vêm como `isError: true` + texto (ex.: `command 'timeline.razor' is not available right now: no sequence is open`).
- Em headless, as `ui_*` falham com "this tool drives the live app…".

## Bridge (app aberto)
1. Gere um token: `openssl rand -hex 32`.
2. Inicie o app (com confirmação do usuário):
   `FILMCRAFT_CONTROL_TOKEN=$TOK /Applications/FilmCraft.app/Contents/MacOS/FilmCraft --control 39871 [--data-dir D] [--empty --no-recover]`.
3. Espere a porta (`nc -z 127.0.0.1 39871`) e faça uma leitura (`ui_inspect`) antes de editar.
4. Servidor: `FILMCRAFT_CONTROL_TOKEN=$TOK filmcraft-cli mcp --bridge 127.0.0.1:39871`. Abra o projeto com
   `command_run file.open {path:"/abs/P.fcproj"}`.
5. Prefira `command_run` (motor) aos atalhos `ui_key`: `Cmd+Z` com foco num campo de texto não desfaz a timeline;
   `command_run edit.undo` desfaz.
6. Para encerrar: `ui_control {"method":"app.quit"}` fecha **sem perguntar** (o não salvo vai para Recovery). Salve antes.

Métodos de `ui_control` (canal de controle): `engine.execute {command, params}`, `engine.commands`, `ui.menu.list`/`ui.menu.invoke`,
`ui.inspect`, `ui.elements`, `ui.set {tool, workspace, …}`, `ui.click`, `ui.move`, `ui.drag`, `ui.scroll`, `ui.key`, `ui.type`,
`ui.timeline.hit {x,y}`, `ui.timeline.locate {clip, edge?}` → `{x,y}`, `ui.playback {action}`, `ui.panel.show/close {panel}`,
`ui.screenshot {path?, panel?}`, `ui.resize`, `ui.focus`, `app.quit`, `perf.stats`.

Erros de bridge: `control authentication failed` (token); `unknown key/method/panel`; `ui_click` com id inexistente →
`no UI pass ran before the control request deadline`.

## Script de apoio
`python3 scripts/fc_mcp.py [--project P | --demo | --bridge ADDR] [--list] chamadas.json`: uma sessão, uma linha JSON por
chamada (`{"i","tool","isError","result"}`); imagens salvas como `mcp_<i>.png`; `"$<i>.<chave>"` reaproveita resultados; sai 1
se alguma chamada falhou.

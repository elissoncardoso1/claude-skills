# MCP server (`designcraft-cli mcp`)

Newline-delimited JSON-RPC 2.0 on stdio; protocol `2025-06-18` (also `2025-03-26`, `2024-11-05`) [D][O].
`serverInfo.version` = CLI version; capabilities `tools` + `resources`; **no prompts**
(`prompts/list` → -32601) [O]. Logs on stderr.

## Register / run

```sh
claude mcp add designcraft -- designcraft-cli mcp                          # headless
claude mcp add designcraft -- designcraft-cli mcp \
   --automation-read-root /work/in --automation-write-root /work/out       # confined
claude mcp add designcraft-app -- designcraft-cli mcp --connect 7979       # desktop app
```
Without registration, drive it with the bundled client [O]:
```sh
python3 scripts/dc_mcp.py calls.json --out shots/            # headless
python3 scripts/dc_mcp.py calls.json --out shots/ -- --connect 7979
python3 scripts/dc_mcp.py --tools                            # list tools of this version
```
`calls.json` = `[{"tool": "new_document", "args": {...}}, ...]`; images land in `shots/call-N.png`.
Each call to `dc_mcp.py` is a fresh server: state lives only for that run — save with `save_document`.

## Tools (26 on 0.17.2) [O]

| Tool | Headless | Notes |
|---|---|---|
| `list_commands {filter?, enabledOnly?}` | ✓ | Same data as `commands` |
| `execute {command, params}` | ✓ | Any command. Unknown param → JSON-RPC **-32602** protocol error; other failures → `isError` result |
| `batch {commands:[{command,params}]}` or `{script}` | ✓ | Stops at first error; `$N` refs; checks every step's keys before running |
| `inspect_document {}` | ✓ | = `document.inspect`; takes no args (extra arg → -32602) |
| `get_story {story \| frame}` | ✓ | text, frames, lines, `overset` byte offset, `oversetChars` |
| `set_story_text {story \| frame, text}` | ✓ | keeps first paragraph/character formatting |
| `new_document {preset, width, height, pages, margins, columns, gutter, bleed, facingPages, …, sample}` | ✓ | = `file.new`; returns `{index}` |
| `open_document {path}` / `save_document {path}` | ✓ | native `.designcraft` |
| `place_image {path \| base64, frame?, x?, y?, width?, spread?, name?}` | ✓ | PNG JPEG WebP GIF TIFF |
| `render_page {page?, scale?=1, path?, bleed?}` | ✓ | returns PNG **image content** — use it to look |
| `export_png {page?, path, scale?=2}` | ✓ | `.jpg` path → JPEG |
| `select_tool`, `pointer`, `key`, `type_text`, `ime` | ✓ | simulated tool input (rarely needed: prefer commands) |
| `screenshot`, `click`, `drag`, `menu_list`, `ui_inspect`, `ui_set`, `dialog_set/confirm/cancel` | ✗ | connected only; headless returns an error telling how to connect |

Resources: `designcraft://document` (inspect JSON), `designcraft://commands` [O].

## Headless vs connected [O]

| | Headless `mcp` | Connected `mcp --connect PORT` |
|---|---|---|
| Start state | empty Letter doc (index 0) | whatever the app has open (may be none) |
| Rendering | CPU renderer | app renderer; window visible |
| UI commands (`view.*`, `window.*`, `help.*`) | error "is a UI command; it needs the desktop app" | work |
| Window screenshot / menus / dialogs | error | work (`screenshot` = full window PNG) |
| File-access roots | supported | **refused** with roots (app is not confined) |

A failed connected request is not resent; inspect the document before retrying [D].

## File-access roots [O][D]

With `--automation-read-root DIR` / `--automation-write-root DIR` (repeatable), any read/write
outside them fails as a tool error, e.g.
`automation path rejected: outside the write root /x/rw: /etc/x.png`. A kind not given grants none
of that access. Paths without roots: relative paths resolve against the server's working directory;
**prefer absolute paths** in MCP calls.

## Minimal MCP workflow [O]

```json
[{"tool":"new_document","args":{"preset":"A4","margins":36,"facingPages":false}},
 {"tool":"batch","args":{"script":"frame.create {\"rect\":[36,36,559,120],\"content\":\"text\",\"text\":\"Summer Fair\"}\nselection.set {\"ids\":[\"$0.id\"]}\ntype.char {\"attrs\":{\"size\":36}}"}},
 {"tool":"place_image","args":{"path":"/abs/photo.jpg","x":36,"y":140,"width":523}},
 {"tool":"render_page","args":{"page":0}},
 {"tool":"save_document","args":{"path":"/abs/out/fair.designcraft"}},
 {"tool":"execute","args":{"command":"file.exportPdf","params":{"path":"/abs/out/fair.pdf"}}}]
```
Warning: the docs' example `set_story_text {"story": 9}` and `type.char` straight after
`frame.create` do not work as written on 0.17.2 — ids differ (use returned ids) and `type.char`
needs a selection first [O].

# MCP tools (server `vectorcraft`, headless, 0.15.0)

Schemas: load with ToolSearch `+vectorcraft`. Command params: `command_list {filter:"<id>"}`.

| Tool | Key args | Returns / notes |
|---|---|---|
| `command_list` / `list_commands` | `filter`/`query`, `menu`, `brief`, `enabled_only` | array (list_commands: `{commands,count}`); `disabled_reason` when disabled |
| `command_run` / `run_command` | `id`/`command`, `params` | command result, often `null` |
| `command_batch` | `steps:[{id,params}]` ≤256, `atomic`, `label` (only with `atomic:true`, else error), `stop_on_error` | `{completed,failed,results,created}`; a step id is an **engine command or `draw_path`/`draw_shape` only** — other tools (`transform`, `pathfinder`, `add_text`…) fail as "unknown command": use their engine commands (`object.rotate`, `object.pathfinder.unite`, `text.create`); refs `"$N.id"`, `"$last.ids.0"`. On error earlier steps stay applied (atomic or not). A batch whose first step is `file.new` is **not** one undo step in the new document |
| `draw_shape` | `shape` + geometry, `fill`,`stroke`,`strokeWidth`,`dash`,`cap`,`join`,`opacity`,`name`,`effects` | `{id}`; one undo step |
| `draw_path` | `points` or `d`, `closed`, same styling | `{id}` |
| `set_paint` | `fill`,`stroke`,`strokeWidth`,`ids` | also sets the default for new art |
| `transform` | `dx,dy,rotate,scale,scaleX,scaleY,reflect,shear,origin,copy,ids` | `{applied}` only — with `copy:true` the new ids are NOT returned: use `run_command object.move {ids, dx, dy, copy:true}` (returns `{ids}`) or `document.find {name}` afterwards |
| `pathfinder` | `operation`, `ids` | `{ids}` destructive |
| `apply_effect` | `effect`, `params`, `ids` | never call without `effect` (80 KB) |
| `add_text` | `text`, `x`,`y`, `size`,`font`,`color`,`justify`, area `width`,`height`,`fit`; `path`+`mode` | `{id, overflow?}` |
| `text_wrap` | `ids`,`offset`,`invert`,`release` | area type below flows around |
| `create_graph` | `x,y,width,height`, `type`, `csv`|`series`/`categories`/`rows` | `{id}` |
| `open_file` | `path` | new active doc; `warnings`, `missingLinks` |
| `save_file` | `path` (.vectorcraft .vctemplate .pdf .svg .svgz .ai) | retargets the doc |
| `export` (does **not** create folders: "No such file or directory"; `range` names files `<stem>-<artboard name>.svg`) | `path`, `format`, `scale`, `artboard` (0-based), `range` ("1-3"), `selection`, `outlineText`, `options` | `{bytes,format,path,warnings,files?}`; no path → `dataBase64` |
| `inspect_document` / `doc_inspect` | `depth`, `childLimit`, `ids`, `kind`, `limit`, `offset` | artboards, layers/nodes, selection, history, `currentLayer`, default `paint` |
| `screenshot` | `scale`, `artboard`, `path` | sharp render at scale; `path` must be in write root |
| `render_preview` | `artboard`, `max_side` | upscales small artboards (blurry) |
| `undo` / `redo` | — | `{undone}` / `{redone}` |
| `invoke_menu` | `command`, `params` | headless: engine ids only |
| `pointer_gesture`, `press_key`, `select_tool` | | work headless but prefer commands (gesture uses last drag, ignores `up`) |
| `inspect_ui`, `ui_inspect`, `ui_screenshot`, `open_panel`, `type_text`, `screenshot {window}` | | live only: error in headless |

Resources: `vectorcraft://document`, `vectorcraft://document/json`, `vectorcraft://commands`, templates `vectorcraft://object/{id}`, `vectorcraft://command/{id}`, `vectorcraft://effect/{id}`, `vectorcraft://swatch/{name}` (ReadMcpResourceTool, server `vectorcraft`).

Useful query commands via `run_command`: `document.find {name|kind|text, limit}`, `document.node {id[, summary, depth]}`, `document.formats`, `file.list {path}`, `recolor.colors`, `swatch.list`, `symbol.list`, `text.fonts`, `text.missingFonts`, `text.fontList {family}`, `paint.proxies`, `effect.list`.

Errors come back as tool errors with a readable message: unknown key (with suggestion), unknown command, `not available right now: <reason>`, `automation path rejected: outside the … root`, `No such file or directory`.

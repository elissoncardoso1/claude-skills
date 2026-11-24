# MCP tools (server `photocraft`, headless)

Prefix in Claude Code: `mcp__photocraft__`. Paths: relative to the automation root or absolute inside it.

| Tool | Key args | Returns / notes |
|---|---|---|
| `session_list` | – | `{active, documents:[{index,name,path,width,height,dirty,revision}]}` |
| `doc_new` | width, height, background (`white`/`black`/`transparent`/`#rrggbb`), mode, depth, name | `{document: index}` |
| `doc_open` | path | `{index, width, height, layers, name, warnings}` — read `warnings` |
| `doc_place` | path, center [x,y], scale %, fit | smart object `{layer, bounds, scale}`; big files are fitted |
| `doc_select` / `doc_close` | index | close discards unsaved changes |
| `doc_inspect` | index? | layers (top→bottom, with `adjustment`, `smartFilters`, `text`, `effects`, `hasMask`, `clipped`), `history`, `canUndo`, `selectionBounds`, `warnings` |
| `command_list` | filter, enabled_only | `[{id,label,menu,params,enabled,disabledReason,needsDocument}]` |
| `command_run` | id, params, wait | command result; `wait:false` → `{job, pending}` |
| `command_batch` | steps `[{id,params,wait}]`, stop_on_error | `{completed, failed, results}`; stops at first error; **no rollback** |
| `jobs_list` / `jobs_cancel` | job? | progress 0..1, state running/done/failed/cancelled; job `document` is an internal id, not the session index |
| `render_preview` (= `doc_render_preview`) | max_side (default 1024, max 2048), index | flattened PNG |
| `doc_save` | path, format, quality 1..100, tiffLayers… | **without path overwrites the opened PSD/PSB/.pcraft** |
| `doc_export` | same as doc_save | overwrites an existing file silently |
| `doc_export_layers` | dir, format, prefix, visible_only | refuses existing files; adjustment layers produce no file |
| `doc_import_data_sets` / `doc_export_data_sets` | path CSV / dir, naming | templates (not verified) |
| `ui_inspect`, `ui_screenshot`, `ui_set`, `ui_pointer`, `ui_menu_invoke`, `control_call` | – | **bridge only**; in headless they return how to start bridge |

Resources: `photocraft://document` (live doc_inspect), `photocraft://commands` (~330 KB — prefer `command_list {filter}`).

Minimal session:
```
doc_open {path:"proj/in/photo.jpg"}
doc_inspect
command_list {filter:"newAdjustmentLayer.curves"}
command_run {id:"layer.newAdjustmentLayer.curves", params:{points:[[0,0],[64,50],[192,210],[255,255]]}}
render_preview {max_side:1024}
doc_save {path:"proj/out/photo-edit.pcraft"}
doc_export {path:"proj/out/photo-edit.jpg", quality:90}
doc_close
```

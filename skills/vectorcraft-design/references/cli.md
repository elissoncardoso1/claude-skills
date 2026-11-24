# vectorcraft-cli 0.15.0

```
vectorcraft-cli run [--in FILE] [--cmd ID [--params JSON] | --commands FILE|-]... [--export FILE]... [--scale N]
vectorcraft-cli convert IN OUT [--scale N] [--artboard I | --range R] [--outline-text] [--decimals N]
                               [--replace-lossy] [--editing-data] [--ai-version 7|pdf] [--hidden-objects layer|omit|visible]
                               [--transparent-images flatten|omit]
vectorcraft-cli info FILE          # artboards, kinds, fonts (status exact|substitute|missing), units, import warnings
vectorcraft-cli commands           # full catalogue JSON (~430 KB) — filter with python/jq
vectorcraft-cli mcp [...]          # the MCP server (already configured)
```

- `run` prints one JSON line per step (`open`, `cmd`, `export`); exit 1 on the first failure: `step N (id): message` (N from 0).
- `--params` belongs to the `--cmd` just before it. Refs: `"$1.id"`, `"$last.ids.0"`; `$$` = literal `$`.
- Host commands only in `run`: `file.open`, `file.save {path}` (absolute path), `file.export`, `file.exportForScreens`, `tool.select`.
- `--commands FILE`: JSON array or JSON Lines of `{"id": ID, "params": {...}}` (or `"command"`). `scripts/tokens_to_steps.py` emits `id`, so the same file feeds `command_batch`.
- `--export` format from extension; raster size by `--scale` (px per pt). A raster `--export` writes the first artboard only (an SVG `--export` writes one file with the first artboard's viewBox but **all** art); for another use `convert IN OUT.png --artboard I` (0-based) or `--cmd file.export --params '{"path":"/abs/x.png","artboard":k}'` [documented], or MCP `export {artboard|range}`.
- New art starts white fill + 1 pt black stroke: set `paint.setFill`/`paint.setStroke {none:true}` explicitly after each shape (selection-based).
- **No sandbox and silent overwrite** (`convert a.svg a.svg` overwrites). Check `test -e OUT` first.
- `SOURCE_DATE_EPOCH=<secs>` → byte-identical PNG/PDF across runs.

## MCP-equivalents on the CLI

| MCP | CLI |
|---|---|
| `command_list {filter}` | `vectorcraft-cli commands \| python3 -c "import json,sys;[print(c['id'],'\|',c['params'][:200]) for c in json.load(sys.stdin) if 'WORD' in c['id']]"` |
| `inspect_document` / `doc_inspect` | `vectorcraft-cli run --in F --cmd document.inspect` (or `--cmd document.find --params '{"name":"x"}'`, `--cmd document.node --params '{"id":5}'`) |
| `vectorcraft://effect/{id}`, effect catalogue | `vectorcraft-cli run --cmd effect.list` (115 ids; large) — filter by id |
| `imageTrace.presets`, `document.formats`, `text.fontList` | `vectorcraft-cli run --cmd <id>` |
| `render_preview` / `screenshot` | `--export x.png --scale N`, then Read the PNG |
| `save_file` | `--cmd file.save --params '{"path":"/abs/x.vectorcraft"}'` or `--export x.vectorcraft` |

- IDs are stable for the same saved `.vectorcraft` across separate `run` invocations (audit S8): inspect in one run, edit by id in the next. There is no select-by-name; get ids from `document.find {name}`.
- Many commands return `null` on success (`object.setProps`), and some ignore typo keys the same way: prove the change with `--cmd document.find --params '{"name":"x"}'` or `scripts/vc_tree.py` on the saved file (`document.node {summary:true}` is not compact).
- Export failures print `step N: export …` (no command id) and exit 1; nothing is written.

## Batch pattern

See `examples/batch-cli.md` (sample in its own folder, skip-if-exists, treat `"changed":0` as UNCHANGED, audit fills and strokes).

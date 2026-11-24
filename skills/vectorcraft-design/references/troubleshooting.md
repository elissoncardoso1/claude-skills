# Troubleshooting

| Symptom | Cause | Do |
|---|---|---|
| `unknown parameter X; did you mean Y?` | typo | use Y; re-read params |
| typo key accepted, nothing changed (`object.setProps {colour}`, `stroke.set {wieght}` → ok, null) | not every command checks keys | re-read params; measure the effect |
| export: `No such file or directory` | target folder missing (export/screenshot don't create folders; MCP has no mkdir) | `mkdir -p` with Bash inside the root, then export |
| `unknown command X` | not in 0.15.0, or UI-only (`view.*`, `window.*`) | `command_list {filter, brief:true}` |
| `not available right now: <reason>` | precondition (selection, object kind) | satisfy it; `command_list` shows `disabled_reason` |
| `automation path rejected: outside the … root <dir>` | path outside the server's roots (`vc_preflight.py` lists them) | copy into a read root (ask) or use the CLI |
| `No such file or directory` | wrong path | `run_command file.list {path}` |
| `unknown extension .x: pass format` (export) | unsupported output ext | `format` or `document.formats` (MCP `run_command`, CLI `run --cmd`) |
| `not a format VectorCraft reads` (open/info/convert) | unsupported input (.sketch, .fig, .xd…) | ask for SVG/PDF/AI export from the source app |
| `unknown command effect.X` | effects are not commands | `effect.list` / `vectorcraft://effect/{id}`, then `effect.apply {effect:"<group>.<name>"}` (e.g. `artistic.neonGlow`, `stylize.outerGlow`) |
| `Flat Logo` trace refused | image has gradients | use `6 Colors`/`16 Colors` |
| `needs the desktop app` | live-only tool in headless | use commands; live only on request |
| returns `null`, nothing changed | no-op: wrong/empty selection, layer not current, `ids` ignored (align/distribute) | check `selection`, `currentLayer`; `select.set`; `layer.setCurrent` |
| black outline / odd colour on new art | inherited default paint | pass fill+stroke(+color) explicitly |
| wrong font in render | missing font → Source Sans 3 | `text.missingFonts`, `text.fontList`, ask |
| blurry preview | render_preview upscaling a small artboard | `screenshot {scale}` |
| tool output too large | effect catalogue / presets / full inspect | resources by id, `depth:0`, `ids`, `kind`, `brief` |
| recolor fails "select artwork to recolour" | no selection | `select.all` first |
| chart labels cut | graph height = plot only | move/shrink graph, enlarge artboard |
| element missing in export | outside artboard, hidden, template layer | `vc_check.py`, inspect bounds/visible |
| reopened SVG lost live shapes | SVG limitation | edit the `.vectorcraft` master |
| `-32003 busy` [documented, not observed] | a call running > 2 s | wait, retry |
| batch stopped midway | stop_on_error; earlier steps stay applied even with `atomic` | read `results[i].error`; check `history`, then one `undo` (atomic) or several |
| `undo` reverted the wrong thing | the last call was a no-op (no history step) | always read `inspect_document.history` before `undo`; `redo` to recover |
| CLI `step N (id): …` exit 1 | step N (0-based) failed; nothing exported after it | fix that step |
| CLI `step N: export …` exit 1 | export failed (missing folder, bad extension) | `mkdir -p`, check extension |
| blank export after `run --commands steps.json` | the generator failed and left an empty file | check the generator's exit code / `test -s steps.json` |
| external `url()` fill rendered black | CSS reference to an external file | `vc_links.py --strip` |
| PDF warning "Preserve editing was left out" | single-artboard PDF | export the whole document for an editable PDF |
| negative/odd geometry | out-of-domain values accepted | validate inputs before calling |

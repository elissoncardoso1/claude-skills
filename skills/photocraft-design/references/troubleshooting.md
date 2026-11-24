# Troubleshooting

Diagnose first. Don't resend the same command with guessed variations.

| Message / symptom | Meaning | Do |
|---|---|---|
| `unknown command \`x\`` | wrong id | `command_list {filter}` / `commands --filter` |
| `not available right now: no document open` | no doc | `doc_open` / `doc_new` |
| `… no selection` | needs a selection | create one; mask commands consume it |
| `filters need a pixel layer (active layer is a Shape layer)` | wrong layer kind | `layer.select` a pixel layer or `filter.convertForSmartFilters` |
| other `disabledReason` (`no active layer`, `select three or more layers…`) | state | satisfy the stated reason |
| success but nothing changed | misspelled/unknown key, ignored | compare keys with `params` doc |
| success but odd values (1×1 doc) | out-of-range value clamped | respect ranges; verify dims |
| warning `font 'X' is not installed; text may render using a fallback face` | missing font | stop; list families (`run <img> --cmd type.fonts`), offer close installed ones, ask the user; for existing docs `type.resolveMissingFonts {map}` |
| `bad --params JSON` | shell quoting | wrap JSON in single quotes |
| `No such file or directory` / `(NotFound)` | wrong path | MCP paths are relative to the root |
| `automation path rejected …` / `a path led outside of the filesystem` | outside root, `..`, symlink | copy into the root or use CLI deliberately |
| `codec: unrecognized image format` | corrupt / not an image | skip and report |
| `unknown file format: xyz` | unsupported output ext | pcraft, psd, png, jpg, tif, webp, exr, tga, dpx, dds… |
| `(AlreadyExists)` on `doc_export_layers` | target files exist | new folder |
| `… needs bridge mode` | `ui_*` in headless | use `render_preview`; bridge only on request |
| batch `FAIL … / N succeeded, M failed` (exit 1) | partial failure | report, fix cause, rerun only failed files into the same new out dir |
| job `failed` in `jobs_list` | long command failed | read its `error`; cancel leaves the doc unchanged |
| `command_batch` `failed > 0` | stopped; earlier steps stay applied | inspect; `edit.undo` per applied step if needed |
| `unknown flag --x for <sub>` (exit 2) | wrong flag | `photocraft-cli <sub> --help` |
| huge/duplicated output from `type.fonts {family}` | engine repeats faces (1470 rows for 14) | use CLI `type.fonts` without params and filter locally |
| version differs from 0.12.0 | notes may be stale | trust live registry and `--help` |

# Reproducible deliveries

A delivery is a folder made by `scripts/vc_manifest.py`:

```
delivery/
├── steps.json      recipe: vectorcraft-cli `run --commands` array (schemas/steps.schema.json)
├── manifest.json   environment, epoch, inputs, outputs, fonts, hashes, replay status (schemas/manifest.schema.json)
├── inputs/         copy of the --in file, if any
├── outputs/        the exports (editable .vectorcraft first)
└── README.md       generated summary
```

## Recipe rules (enforced by `vc_common.validate_steps`)

- Step 0 `file.new {width,height,units,artboards…}`, then `select.none`, `paint.default`. On `--in FILE` the recipe starts with `select.none`, `paint.default`.
- Every object gets explicit paint: `paint.setFill`/`paint.setStroke` (`{none:true}` when unwanted), `stroke.set {weight,cap,join,dash}`, `object.setProps {opacity,name}`. These commands act on the selection, and a new object is selected, so put them right after the object they paint.
- References are `"$N.id"` with N the 0-based step index. Inserting a step shifts every later N, so regenerate the recipe; don't splice steps into it.
- Not allowed: any command that reads or writes files, runs other commands, or touches preferences, libraries, fonts, presets or the clipboard: `file.*` (except `file.new`), `document.open/save/export*`, `action.batch`/`command.batch` (they would run nested denied commands), `clipboard.*`, `dataset.*`, `links.*`, `library.*`, `prefs.*`, `plugin.*`, `script.*`, `print.*`, `assets.*`, `view.*`, `window.*`, and every id containing save/load/import/export/install/package/relink/recover/files/presets (`vc_common.DENIED`; `python3 -B scripts/vc_common.py --denied` lists the 185 ids of 0.15.0). Also no string that looks like a path (`/…`, `~`, `..`, `C:`, `file:`). Paths belong to the manifest, which only allows ones relative to the delivery folder.
- New-document recipes use `"$N.id"` references, never literal object ids (a literal id was copied from some session and can hit another object). Literal ids are allowed only in `--in` recipes, where they name objects of the input file (stable across runs, S08).
- From MCP: the steps of ONE `command_batch` that starts with the reset are the recipe (same `id`/`params` shape). `$N` refers to that batch only; work spread over several batches must be rewritten as one recipe and replayed before you call it reproducible. `draw_shape`/`draw_path` are MCP tools, not engine commands: for a recipe use `path.create {d}` + paint steps (`tokens_to_steps.py` does this).

## M31: paint leaks between MCP documents

Reproduced on 0.15.0, and kept as regression test M31: set fill red, stroke green and weight 7 with nothing selected, then `file.new` and `path.create`. The new path is red/green/7. After `select.none` + `paint.default` the same path gets the defaults (white fill, black 1 pt stroke, butt cap, no dash). Policy:
1. Every recipe and every MCP batch starts with the reset (rule 2 in SKILL.md).
2. Paint is explicit per object anyway (the reset gives defaults, not the design).
3. The CLI starts each `run` in a fresh session, so the replay never inherits MCP state. The MCP session cannot be restarted from inside a conversation, and nothing isolates two documents of one session except this reset.

## Replay statuses (`vc_replay.py`)

| Status | Meaning | Exit |
|---|---|---|
| REPRODUCED_BINARY | every output's SHA-256 equals the manifest | 0 |
| REPRODUCED_VISUAL | some PNG differs in bytes only: same size and no channel of any pixel differs by more than 2/255 (`vc_common.MAX_DIFF`) | 10 |
| REPRODUCED_STRUCTURAL | some vector/native file (`vectorcraft`, `svg`, `pdf`, `ai`, `eps`) differs in bytes but has the same artboards, kinds, font statuses, `vc_tree` lines (ids, names, bounds, fill, stroke, width, cap, join) **and** the same bytes when both are re-exported to SVG by the same CLI (geometry, dash, opacity, gradients, text) | 11 |
| FAILED | the recipe failed; an output, input or the recipe changed since the manifest; or no comparison holds | 1 |
| UNVERIFIED | no CLI, or a format with no comparison available (e.g. a 16-bit PNG) | 3 |

Overall = FAILED if any, else UNVERIFIED if any, else the weakest of BINARY > VISUAL > STRUCTURAL. Integrity (are the delivered files intact?) is reported separately from the replay, so a modified output is caught even when the replay matches. The format used to pick the comparison comes from the file extension, never from the manifest, and the manifest's outputs must be exactly the exports + derived files. Structural equality relies on SVG export; raster effects inside the artwork are compared as the embedded images the SVG holds. Visual is only measured for PNG outputs.

Replays run with `VECTORCRAFT_NO_PREFS=1`, so the user's VectorCraft preferences (default units, compression, user fonts folder) do not change the result.

## What is byte-identical (measured, CLI 0.15.0, macOS 27 arm64)

| Condition | .vectorcraft | SVG | PDF | PNG | EPS | AI |
|---|---|---|---|---|---|---|
| same recipe, same `SOURCE_DATE_EPOCH`, two clean folders | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| different folder / path with spaces and accents | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| without `SOURCE_DATE_EPOCH` | ✗ (dates) | ✓ | ✗ | ✗ bytes, ✓ pixels | ✗ | ✗ |
| another epoch | structural ✓ | ✓ | structural ✓ | visual ✓ | — | — |
| replay from a contaminated MCP session | n/a: the replay always uses a fresh CLI `run` | | | | | |
| image trace (`imageTrace.makeAndExpand`, S03) | ✓ | ✓ | | | | |

DXF is byte-identical too (S06, same epoch).

Not measured: another machine, another OS or architecture, another CLI version, other installed font versions. PDF/AI/EPS embed the font files of live text, so a different font file version changes the bytes. EMF/WMF/PSD have not been through the replay.

`vc_manifest.py` uses `SOURCE_DATE_EPOCH=946684800` (2000-01-01) unless `--epoch` says otherwise.

## Fonts in a delivery

`manifest.fonts[]`: family, style, status (`exact` | `substitute` | `missing`), resolved family. `file` and `file_sha256` stay `null`: the CLI doesn't expose font file paths. `font_strategy`:
- `editable`: live text; the receiver needs the fonts (listed in `dependencies.fonts`).
- `both`: plus an outlined SVG (`--outline-svg outputs/a.vectorcraft=outputs/a-outlined.svg`, made by `vectorcraft-cli convert --outline-text`) for visual fidelity without the fonts.
- `outlined`: only outlines (only when the user asked; text is no longer editable).
- `none`: no text.
Don't ship font files unless their license allows it. The bundled fallback is Source Sans 3.

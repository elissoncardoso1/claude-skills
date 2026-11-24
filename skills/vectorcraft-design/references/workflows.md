# Workflows

Common to all: explicit paint; one step → check → look; save `.vectorcraft` master in a work folder; exports to new names; `vc_check.py` on outputs; report.

## Icon (MCP)
1. `run_command file.new {width:24,height:24,units:"Pixels",name}`.
2. `draw_path` per stroke (`fill:"none"`, `stroke`, `strokeWidth`, `cap`, `join`, `name`), coordinates on the grid inside 2–22. Solid parts: `draw_shape`/`draw_path` with `fill` + `stroke:"none"`.
   Several proven steps → one `command_batch {atomic:true}`.
3. `object.group {ids}` + `object.setProps {id, name:"icon-x"}`.
4. `screenshot {scale:8}` + `render_preview {max_side:24}`; fix one defect at a time.
5. `save_file x.vectorcraft`; `export x.svg {options:{decimals:2}}`; `vc_check.py x.vectorcraft --icon --stroke 2 --cap round --join round`.
Example: `examples/icon-mcp.md`.

## Icon set
Tokens JSON (grid, stroke, colour; icon paths absolute M/L/C/Z — convert H/V/A/relative first) → reference icon (above) → user check if interactive (non-interactive: validate it yourself and say so) → remaining icons on artboards k (x offset k·44 for 24 + 20) → `vc_check.py --icon --pad 2` (consistency) → strip preview (`export png options.rect`) → name artboards (`artboard.setProps {index,name}`) so SVG `<title>`s are right → export per icon. `scripts/tokens_to_steps.py` turns tokens + path data into steps (CLI `run --commands` or `command_batch` as-is; ≤256 steps per batch).

## Logo / identity
2–3 concepts from primary shapes + `pathfinder` (live `pathfinder.*` effects while exploring); one artboard per concept/variant (colour, mono, inverted on a dark rect, symbol only). Duplicate the mark across artboards with `run_command object.move {ids, dx: k·(width+spacing), copy:true}` (returns the copies' `{ids}`; the `transform` tool with `copy` returns none), then recolour the copy. If the mono version fails the 16 px test (details fuse into a blob), that is a design problem: simplify the mark (fewer, larger elements, gaps ≥ 1/16 of the size) or report it and offer a simplified "small" variant; fonts confirmed; legibility at 16 and 256 px; export SVG + PDF. Never call it approved — present options and criteria.

## Recolor to a smaller palette
`select.all` → `recolor.colors` (all colour keys) → decide the mapping explicitly (several sources → one target is allowed: `{"map":{"#a":"#x","#b":"#x","#c":"#y"}}`), keep light/dark roles and check contrast after → `recolor.apply` → `recolor.colors` again. Off-artboard or hidden art is still recoloured or listed: decide (delete / leave) and say so.

## Improve / recolor an existing SVG (or AI/PDF/EPS)
1. Copy the input into the work folder (never edit the original); `vectorcraft-cli info` (kinds, fonts, warnings).
2. `open_file copy` → `inspect_document {depth:1}` → `recolor.colors` (after `select.all`) → `text.missingFonts` → screenshot.
3. List **verifiable** problems (objects off-artboard, stray/unpainted paths `object.path.cleanUp`, too many anchors, inconsistent strokes, missing fonts, low contrast, raster pieces). Separate from taste.
   Note: unpainted empty paths are dropped on import (no warning) — read the raw SVG if they matter.
3b. Name the document/artboards before exporting (`file.new {name}` / `artboard.setProps`), or the SVG `<title>` carries the working file name.
4. Fix incrementally, keeping structure (names, layers, groups); one change → inspect → look.
5. Compare: `info` before/after, screenshots side by side.
6. `save_file name-improved.vectorcraft` + `export name-improved.svg`. Report changes + what was left alone.
Example: `examples/improve-svg.md`.

## Vectorize a raster
MCP: copy into root → `open_file`. CLI: `vectorcraft-cli run --in img.png --cmd select.all --cmd imageTrace.makeAndExpand --params '{…}' --cmd file.save --params '{"path":"/abs/out.vectorcraft"}' --export out.svg --export out.png --scale 2`, then Read the PNG.
Check size (> 1500 px slow) → choose preset: truly flat logo → `Flat Logo` (it **refuses** art with gradients: "this isn't a flat-colour logo … use Color mode instead" → fall back to `6 Colors`/`16 Colors`); b&w → `Black and White Logo`, `Line Art`; photo → `Low/High Fidelity Photo` (heavy) → `select.all` → `imageTrace.makeAndExpand {preset, params:{ignoreWhite:true}}` → read `{paths,anchors,colors}` → optional `object.path.simplify` (check before/after; it can soften geometric corners — compare previews with and without) → preview vs source → export. Expect: gradients become bands, rounded corners get lumpy, text becomes outlines. Say plainly when a raster doesn't vectorize well; offer to redraw clean shapes instead.

## Diagram
Nodes/edges list → grid positions computed → `draw_shape rectangle {radius}` + `add_text {justify:"center"}` per node → connectors `draw_path` (arrowheads: `stroke.set {endArrow}`, check params live) → `select.set` + align/distribute → check text overflow, connector endpoints on box edges → export.

## Poster
Format (`file.new` in pt) → margins/columns computed → layers bg/art/text (`layer.new` + `layer.setCurrent` each time) → shapes/images → type (`add_text`, area + `fit:"autoHeight"`) → `text.missingFonts` → contrast computed → preview whole + details (≤3 iterations) → save `.vectorcraft` → `export pdf` (print) + `png scale:2` (screen).

## SVG for UI
Artboard = viewBox; simple paths, no raster effects; `export {options:{decimals:2, minify:true, objectIds:"minimal"}, outlineText:true if text}`; check `<image>`/`<filter>` absent, size, render 1× and 2×.

## Batch (CLI)
Inspect 1–2 samples (`info`) → steps (`--cmd` or `--commands file`) → run on one sample to a separate folder → verify (info + PNG) → loop with skip-if-exists, ok/FAIL log → audit counts and samples. See `examples/batch-cli.md`.

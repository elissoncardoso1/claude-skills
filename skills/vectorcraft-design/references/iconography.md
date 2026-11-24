# Icons

Defaults when the user gives none (state them in the report): 24×24 artboard, live area 2–22, stroke 2, `cap:"round"`, `join:"round"`, one colour, outline style.

| Rule | Value | Check |
|---|---|---|
| grid | 24 (or 16/20/32), padding 2 | `vc_check.py FILE --icon --pad 2` (doc_inspect bounds are geometric: add strokeWidth/2 yourself) |
| stroke | same width/cap/join everywhere | `vc_check.py FILE --icon --stroke 2 --cap round --join round` |
| keylines | circle Ø20, square 18, landscape rect 20×16, portrait 16×20 | compare bounds |
| corner radius | one value per set (e.g. 2) | `document.node` → `live.radii` |
| pixel snapping | odd stroke → coords at .5; even stroke → integers | inspect `d`/points |
| optical size | circles/triangles slightly larger than squares to look equal | visual |
| small sizes | legible at 16 and 24 px; no details < 2 px apart | `render_preview {max_side:24}` + `screenshot {scale:8}` |
| fills vs outline | filled shapes: `fill` + `stroke:"none"` | paint labels |

Set workflow: tokens JSON (see `examples/icon-tokens.json`) → reference icon → validate → others → compare.
- One document, N artboards: `file.new {width:24,height:24,artboards:N}`; artboard k origin x = k·44 (24 + 20 spacing). Draw icon k with x offset k·44 (`scripts/tokens_to_steps.py` does this).
- Export individually: `export {path:"set.svg", range:"1-N"}` → `set-Artboard-k.svg` (reply `files`), then rename to icon names; or one `export {artboard:k}` per icon with the final name.
- Name groups `icon-<name>`; don't outline (no text in icons anyway); keep `.vectorcraft` master.
- Strip view: MCP `export {path:"strip.png", scale:4, options:{rect:[0,0,W,24], background:"white"}}`; CLI `--cmd file.export --params '{"path":"strip.png","scale":4,"rect":[0,0,W,24]}'` — on the engine command `rect` is **top-level**; inside `options` it is silently ignored and you get artboard 0 (C34). Check the PNG size, then Read it.

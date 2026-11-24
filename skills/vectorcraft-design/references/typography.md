# Typography

- Before: `run_command text.fontList {family:"Inter"}` (or without family for all; large) — confirm the family exists. Style names via `text.fontList {family}` result.
- Create: `add_text {text, x, y, size, font, color, justify}`; point type `y` is the first **baseline** (top of caps ≈ y − 0.7·size). Area type: `width`, `height`, `fit:"autoHeight"|"shrinkText"`; check `overflow` in the reply.
- After: `run_command text.missingFonts` must return `count: 0`. A missing font is silent and falls back to **Source Sans 3** (also the default when `font` is omitted). If missing: stop, offer installed alternatives, ask.
- Ranges: `text.setRangeStyle {id, start, end, style|size|fill|tracking…}`; offsets are **UTF-8 bytes** (é = 2 bytes). Compute with `len(s[:i].encode())`.
- Whole object: `text.setStyle {ids, font, style, size, leading, tracking (1/1000 em), justify, fill}`.
- Hierarchy: modular scale 1.25/1.333 (e.g. 12/16/20/28/40); leading 1.2–1.5× for body; slight negative tracking on big titles.
- Keep live type in the editable file. Outlines only for delivery: `export {outlineText:true}` (SVG/DXF), PDF `options:{advanced:{outlineText:true}}`, CLI `convert --outline-text`. `type.createOutlines` converts in the document (destructive) — do it in a copy.
- SVG export keeps text as `<text>` with `font-family` — fine for web if the font is available; otherwise outline or `options:{embedFonts:true}` [documented].

## Fonts in deliveries

- Preflight the families first: `vc_preflight.py --font "Inter:Bold"` (FAIL = not installed).
- `vc_manifest.py` records every font with its status and the `font_strategy` (references/reproducibility.md). A `missing`/`substitute` font fails `vc_check.py`: fix it or get the user's OK for the fallback.
- For files that leave this machine: keep the editable file with live text and add an outlined SVG (`--outline-svg FROM=TO`, i.e. `vectorcraft-cli convert --outline-text`). Tested in S11: the editable SVG keeps `<text>`, the outlined SVG has none.
- Embedding: SVG `options:{embedFonts:true}` [documented]; PDF embeds the fonts it uses. Do it only when the font license allows it. Never copy font files into a delivery.

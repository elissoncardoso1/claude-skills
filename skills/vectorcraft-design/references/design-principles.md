# Design principles → decisions you can check

Rules are general design knowledge; VectorCraft has commands only for some. Where no command exists, compute coordinates yourself and verify numerically/visually.

**Composition**
- Pick a base unit (4/8 pt UI; columns for layouts). Margins ≥ 1 unit; space between groups > space inside groups.
- Every edge aligns with something; few axes. Tools: `select.set` + `object.align {to:"selection"|"artboard"}`; `object.distributeSpacing`.
- One dominant element; 2–3 size/weight levels. Leave negative space; judge balance on the preview (subjective → propose, don't impose).
- Symmetry: build half, `transform {reflect:"vertical", copy:true, origin:[cx,cy]}`.
- Formats: A4 595×842, A3 842×1191, Letter 612×792, square post 1080×1080, story 1080×1920 (pt = px for screen).

**Colour**
- Limit the palette (3–5); register as global swatches if the user may recolour later (`swatch.new {colors, global:true}`).
- Contrast is computed, not eyeballed: WCAG ratio ≥ 4.5 body text, ≥ 3 large text/icons (compute from hex in Python).
- Provide monochrome and inverted variants for marks:
  - **mono = one ink only.** Details that read as "holes" must be real holes (knockouts), not shapes painted in the background colour. Stroked details: `object.path.outlineStroke` first (returns `{ids}`), then `pathfinder {operation:"minusFront", ids:[body, outlined]}` (or `object.compoundPath.make` for filled shapes). Check: `select.all` + `recolor.colors` returns exactly one colour (verified C33: coffee bean with a knocked-out crease → 1 path, 1 colour).
  - **inverted = the same single-ink mark in a light ink over a dark background** (background as its own rectangle on a `bg` layer); the knockouts then show the dark background through.
  - Test both at 16 px and 256 px.

**Illustration**
- Decompose back→front into simple shapes; one layer per plane (`layer.new` + `layer.setCurrent`).
- Booleans for silhouettes: live `pathfinder.*` effects while iterating; destructive `pathfinder` at the end.
- Few gradient stops, consistent light direction. Fewer anchors = cleaner curves.

**Data visualisation**
- Values must be right: bars from zero, no 3D, labels ≥ 12 px on screen. Check numbers against the input.
- `create_graph` gives editable axes/legend; restyle series (black by default) and keep labels inside the artboard.
- Don't encode meaning by colour alone; check greyscale legibility.

**Brand / identity**: deliver options + criteria; never declare a mark approved — that's a human decision.

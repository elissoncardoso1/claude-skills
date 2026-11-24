# Validation

Order: structure (cheap, objective) → visual.

Structural (after each step / before delivery)
- Return value: id present, `overflow` absent, `changed` > 0, `before/after`, `files`. `null` proves nothing.
- `doc_inspect {ids:[…]}` or `{kind:"Path"}`: bounds inside the artboard, paint labels, strokeWidth/cap/join, anchors.
- `run_command text.missingFonts` → count 0. `doc_inspect {kind:"Image"}` empty unless raster was intended.
- `recolor.colors` (select.all first) → palette as planned.
- Compact structure: `python3 -B scripts/vc_tree.py FILE` (one line per object).
- Files: `python3 -B scripts/vc_check.py OUT.vectorcraft [--icon] [--stroke W --cap C --join J] [--no-raster]` (`--icon` turns on stroke-consistency checks; off for general art) (exit 1 on problems: outside artboard, missing font, raster, inconsistent strokes). `vectorcraft-cli info` on every export; compare kinds with the master.

Visual
- `screenshot {scale:N}` for zoom (sharp); `render_preview {max_side}` for large artboards; real size check (`render_preview {max_side: real px}`).
- Icons: 1×, 2×, 8×. Posters: whole + detail (`export png options.rect`).
- CLI: export PNG, then Read the image.

Objective defects (always fix): clipped/out-of-artboard elements, fallback fonts, overflow, unintended outlines/colours, inconsistent strokes, low contrast (computed), wrong values in charts, banding/stray anchors in traces.
Aesthetic notes (report, offer options): balance, palette taste, spacing feel, corner style.

Stop: objective checklist clean, or budget spent (3 iterations per element, 2 for the whole). Each iteration names one defect and changes one thing. When stopping with leftovers, list them.

Report: separate "verified structurally", "verified visually", "not verified".

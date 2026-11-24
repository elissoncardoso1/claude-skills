# Example: "Melhore este SVG" (verified 2026-10-23, skill audit S4, MCP)

Input `badge-messy.svg` (red badge, check mark, ring, "APPROVED"). Original left untouched (same md5 after the run).

1. Copy into the work folder: `badge-messy-copy.svg`. `vectorcraft-cli info` → kinds `{Layer 1, Path 4, Type 1}`, font `Comic Neue Fantasy: missing`.
2. `open_file` copy → `inspect_document {depth:1}` → `select.all` + `recolor.colors` → `text.missingFonts` → `screenshot {scale:2}`.
   `python3 -B scripts/vc_check.py badge-messy-copy.svg` → PROBLEM outside artboards (`stray`), PROBLEM missing font.
3. Verifiable problems found → fix, one at a time, checking after each:

| Problem (how measured) | Fix | Check |
|---|---|---|
| green `stray` rect at x=230, outside the 200×120 artboard (bounds, vc_check) | `select.set {ids}` + `edit.clear` | gone from `doc_inspect` |
| font missing → Source Sans 3 (`text.missingFonts`) | `text.fontList` → `text.setStyle {font:"Comic Sans MS", style:"Bold"}` (closest installed; would ask the user first) | `missingFonts` count 0 |
| text contrast `#ffcdd2` on `#e53935` = 3.0:1 (computed WCAG) | text white, background `#c62828` → 5.62:1 | recomputed; **background colour is a brand decision: flag it** |
| text 2.5 pt from the badge edge (bounds) | `transform {dy:-4}` | bounds |
| check mark butt cap / miter join (strokeOptions) | `stroke.set {cap:"round", join:"round"}` | strokeOptions |
| unpainted `empty` path | already dropped on import, no warning | read raw SVG to know |

Left alone (taste, reported): stroke widths 7 vs 4, horizontal text placement.

4. `save_file badge-improved.vectorcraft`, `export badge-improved.svg`, preview PNG. vc_check on outputs → no problems; font status `exact`.
5. Report: list of changes with reasons, what was left alone and why, the brand-colour question.

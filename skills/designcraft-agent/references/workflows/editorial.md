# Editorial / magazine spread / diagrammed page

Generator: `scripts/recipes/editorial_gen.py OUT.dcs IMAGE` (A4 facing, bleed 9 pt; pages 2–3:
full-bleed photo left, kicker + headline + deck, rule, 3-column body with drop cap, pull quote with
text wrap). Verified after one fix iteration (first version overset by 505 chars) [O].

- Standalone spread (no blank page 1): `file.new {facingPages:true, pages:2, startPage:2}` → spread 0
  holds pages 2–3; adapt the recipe's `spread=1` to `spread=0`. Short real copy: add
  `balanceColumns: true` to `object.textFrameOptions`.
- Spread geometry (recipe): spread 1 holds page 2 (x 0..W) and page 3 (x W..2W). Full-bleed photo rect
  `[-bleed, -bleed, W, H+bleed]` on the left page (stop at the spine).
- Image: graphic frame → `file.place {path, frame}` → `object.fit {mode:"fillProportionally"}`.
- Headline block: one story with Kicker / Headline / Deck paragraphs (apply Deck to all, then
  Kicker and Headline at their byte offsets).
- Body: `object.textFrameOptions {columns:3, gutter:12}`; first paragraph style `basedOn` Body with
  `dropCapLines:3, dropCapChars:1, firstLineIndent:0`.
- Pull quote: separate frame over columns 2–3 + `object.textWrap {mode:"boundingBox", offset:[8,8,8,8]}`
  on the quote frame; keep its height tight to the text or it leaves a hole.
- Caption over the photo in `[Paper]` colour.
- VERIFY: overset (cut copy or add a continuation frame with `text.thread`), wrap gap, drop cap
  alignment, rag/hyphenation in narrow columns, photo crop (subject not cut by spine).
- Page PNGs from `run` include the bleed area (you'll see a sliver of the facing page at the spine) —
  that's the bleed, not a layout error [O].

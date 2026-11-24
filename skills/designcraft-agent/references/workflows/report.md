# Report / multi-page document / ebook

Generator: `scripts/recipes/report_gen.py OUT.dcs` (A4 facing, cover with full-bleed panel,
contents page, body autoflowed with headings, folios on the parent). Verified: 5 pages, 0 overset,
TOC page numbers correct [O].

1. **INSPECT** content: count sections, estimate length (≈ 450 words per A4 page at 10.5/15 pt).
2. **PLAN**: `file.new {preset, facingPages:true, pages:3, margins:{top,bottom,inside,outside}}`;
   swatches (CMYK for print) and styles: Title, H1, H2, Body, Caption, Folio.
3. **CREATE**
   - Parent folios: frames on `spread:{kind:"parent",index:0}` with text `"\ue000"`; right page at x+W.
   - Cover without folio: `layout.pages.applyParent {pages:[0], parent:null}`; full-bleed shapes use
     the page rect (or extend by `bleed`). Page 1 of a facing doc is a **right** page: its inside
     (spine) margin is on the left, and extending to x = -bleed reaches into the spine side.
   - Body: one text frame on the first body page with the whole text; `selection.set` + Body style,
     then each heading's paragraph start (`text.select` byte offset) + H1.
   - `layout.pages.insert {count:1}` then `text.thread {from, spread, rect, autoflow:true}` — pages are
     added until the story fits.
   - Contents: `toc.generate {styles:["H1"], page: 2, createBookmarks:true}` after the body exists.
4. **RENDER** `run --in report.designcraft --scale 0.5 --all-pages review/`.
5. **VERIFY** `dc_check.py` (overset!), headings not orphaned at page bottoms (if they are: add
   `"keepWithNext": 2` to the H1 style's `para`, or adjust text), TOC numbers match pages, last page not nearly empty (adjust text/size).
6. **EXPORT** `--export report.pdf` (screen) · `--pdf-options '{"standard":"x4","bleed":true,"marks":true}'` (print)
   · `--export report.epub` (reflowable ebook; `file.exportFixedEpub` for fixed layout) [O file written].

# Paginated presentation (16:9)

Generator: `scripts/recipes/slides_gen.py OUT.dcs IMAGE` (preset `Web 1920 × 1080` = 1920×1080 pt,
non-facing, parent page with accent bar + footer + right-aligned page number, title / bullet /
image slides). Exported PDF (4 pages, 1920×1080 pt) and PPTX (4 slides) [O].

- One page per slide: `file.new {preset:"Web 1920 × 1080", facingPages:false, pages:N}`; slide i = spread i.
- Sizes are points on a large page: titles ~88 pt, bullets ~48 pt, footer ~20 pt.
- Bullets: plain text `"• item"` paragraphs (list commands `list.bullets` exist [D], not exercised).
- Footer page number: separate right-aligned frame with `"\ue000"` (a tab alone does not push it to
  the right edge — first attempt failed) [O].
- EXPORT: `--export deck.pdf` and `--export deck.pptx` (editable shapes/text; `file.exportPptx`
  options `lineBreaks`, `rasterize`, `embedFonts`). Check PPTX by slide count; PowerPoint fidelity
  was not inspected visually [U].

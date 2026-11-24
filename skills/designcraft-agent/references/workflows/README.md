# Workflows

Every recipe follows **INSPECT → PLAN → CREATE/EDIT → RENDER → VERIFY → SAVE/EXPORT** and is backed
by a runnable generator in `scripts/recipes/` that was executed, rendered and checked on 0.17.2.

## The generator pattern (use it for anything over ~10 steps)
Write a small Python script that emits a `.dcs` script: JSON escaping is automatic, you can loop
over content, compute coordinates from page size/margins, and compute UTF-8 byte offsets.
```python
import json
steps = []
def s(cmd, **p):                       # returns the step index for "$N" references
    steps.append(f"{cmd} {json.dumps(p, ensure_ascii=False)}"); return len(steps) - 1
def r(i, key): return f"${i}.{key}"     # "$3.id", "$3.story"
t = s("frame.create", rect=[48, 48, 547, 120], content="text", text="Title")
s("selection.set", ids=[r(t, "id")]); s("style.paragraph.apply", name="H1")
open("doc.dcs", "w").write("\n".join(steps) + "\n")
```
```sh
python3 gen.py && designcraft-cli script doc.dcs --save doc.designcraft
designcraft-cli run --in doc.designcraft --scale 0.5 --all-pages review/      # look at every page
python3 <skill>/scripts/dc_check.py doc.designcraft --margins
```
Write `"\ue000"` as an escape in Python source (an invisible raw character is hard to edit).
`from` is a Python keyword: pass it as `**{"from": ...}`.

## Recipes
| File | Covers | Generator |
|---|---|---|
| report.md | reports, multi-page documents, ebooks (EPUB), TOC, folios | `recipes/report_gen.py` |
| editorial.md | magazine spreads, diagrammed pages, image + text, columns, drop cap, pull quote | `recipes/editorial_gen.py` |
| marketing.md | flyers, posters, commercial material, print with bleed, PDF/X-4 | `recipes/flyer_gen.py` |
| presentation.md | paginated 16:9 presentations, PDF + PPTX | `recipes/slides_gen.py` |

## Visual acceptance criteria (check on the rendered PNGs)
- **Alignment:** related elements share edges (same x0 for title/body/captions); use the grid from
  `document.inspect.pages[].columnRects`; `object.align`/`distribute` for rows.
- **Spacing:** equal gaps between repeated elements; consistent space above/below headings (styles' spaceBefore/After).
- **Hierarchy:** ≥ 1.5× size step between levels; one dominant element per page.
- **Overset:** none (`dc_check` error). **Legibility:** body ≥ 9 pt print / ≥ 24 pt slides, contrast.
- **Proportions:** images filled with `fillProportionally`; confirm content scaleX == scaleY with
  `select.content` + `transform.info` (images.md).
- **Margins:** content inside margins; only intentional bleed art outside (`--margins` warnings explained).
- **Consistency:** recurring elements on parent pages; same styles across pages.
- **Export fidelity:** render the exported PDF (`pdftoppm`) and compare with the PNG review; check page count/size.

# Formats and fidelity (measured with `vectorcraft-cli info` round-trips)

| Format | Read | Write | Editability when reopened in VectorCraft | Notes |
|---|---|---|---|---|
| .vectorcraft | ✓ | ✓ | full (native) | master file; always keep one |
| PDF | ✓ | ✓ | full (preserve editing in default preset) | other apps see plain PDF; `range` pages |
| AI (PDF-compatible) | ✓ | ✓ | full | `--ai-version 7` for legacy |
| EPS | ✓ | ✓ | full (editing data) | |
| SVG / SVGZ | ✓ | ✓ | partial: layers, groups, names, text, gradients, clips, symbols kept; **live shapes → Path**, units → Pixels | `options:{decimals, minify, objectIds, responsive, embedFonts, preserveEditing}` |
| DXF | ✓ | ✓ | low: shapes split into paths, mm; text outlined; artboard becomes the content extents (off-artboard art included); warns on wide line weights | CAD/cutting |
| PSD | ✓ | ✓ | raster, one layer per document layer (names kept) | not vector |
| PNG/JPG/WebP/GIF/TIFF/BMP/TGA | ✓ | ✓ | raster | `scale` px/pt; `options:{background, ppi, rect, useArtboards}` |
| EMF | ✓ | ✓ | vector write; opacity masks dropped (warning) | read not verified |
| WMF | ✓ | ✓ | low: gradients → average colour, patterns → one colour, masks dropped (warnings) | read not verified |
| TXT | — | ✓ | text only | |
| .vctemplate | ✓ | ✓ | native template (opens untitled) | |
| PNG8 (`format:"png8"`) | — | ✓ | indexed PNG | |
| AIT | ✓ | via `file.saveAsTemplate` / CLI `--export x.ait` (template of every artboard) | opens untitled | |
| Affinity (.af/.afdesign/.afpub), PSB, PS | ✓ | — | | |
| TGA (+ aliases .vda .icb .vst) | ✓ | ✓ | raster | |
| **Sketch, Figma, XD, CDR** | ✗ | ✗ | not supported: "not a format VectorCraft reads" | ask for an SVG/PDF export |

Export rules
- Artboards: `artboard` (0-based) or `range` ("1-3", 1-based). SVG with `range` writes `<path-stem>-<artboard name>.svg` (spaces → `-`; default names give `-Artboard-k`): use a short stem (`out/logo.svg` + artboards named `color` → `logo-color.svg`) and read the reply's `files`. PDF/AI: one page per artboard.
- PDF **preserve editing needs every artboard**: a PDF of one artboard (`artboard:k`, `--artboard`) warns "Preserve editing was left out" and reopens as imported PDF art (live shapes → paths; type stays live type, U5). Keep the editable master as `.vectorcraft` or a full-document PDF.
- Rasters write one artboard unless `options:{useArtboards:true}`. Any page area: MCP tool `export {options:{rect:[x,y,w,h]}}`; engine command `document.export`/`file.export` (CLI, `run_command`) takes `rect` **top-level** — `options.rect` is silently ignored there (C34). Verify the output pixel size.
- Text: SVG/DXF `outlineText:true`; PDF `options:{advanced:{outlineText:true}}`.
- Raster-ish content inside vector exports: shadows/blur become SVG `<filter>`; other raster effects (e.g. `artistic.neonGlow`) become an embedded `<image>` **without a warning**; perceptual/dithered/freeform gradients become images. Check `info.kinds` for `Image`.
- Every export reply has `warnings` — read them, but they are not complete: SVG export does **not** warn about a missing font (PDF/EPS do: "written in Source Sans 3"). Run `vectorcraft-cli info OUT` and compare kinds/fonts with the source.
- Import can silently drop empty paths (no fill, no stroke): compare object counts with the source if it matters. SVG import puts top-level elements (e.g. a `<text>` outside groups) into the first layer.
- SVG export outlines stroked paths that carry **arrowheads** (line → filled path + triangle); keep the `.vectorcraft` for edits.
- SVG `<title>` = the artboard name for per-artboard exports ("Artboard 1"), else the document title (which can leak a working file name): `artboard.setProps {index, name}` / `file.new {name}` before exporting.
- CLI `run --export x.svg` on a multi-artboard document writes ONE SVG with the first artboard's viewBox containing **all** art (others off-canvas). Per artboard: `convert IN out.svg --range 1-N` or MCP `export {range}`.
- Exports overwrite silently: choose new names.

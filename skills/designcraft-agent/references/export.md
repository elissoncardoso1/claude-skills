# Rendering and export

## Look at pages (do this every iteration)
| How | Default scale | Pages |
|---|---|---|
| `run --in F --all-pages DIR [--scale S]` | 1 px/pt | all → `DIR/page-001.png` [O] |
| `run --in F --page N --export p.png` | 1 | page N (0-based) [O] |
| `script … --export x.png` | **2** | page 1 only [O][S] |
| MCP `render_page {page, scale?}` | 1 | returns the image inline [O] |
| MCP `export_png {page, path, scale?}` | 2 | file [O][S] |
Renders show printing items only (no guides/frame edges); hidden layers are omitted [O].
**Bleed:** `run --export/--all-pages` PNGs include the document bleed area (A5 + 3 mm → 437×612 px
at 1×) [O][S `render_page(..., bleed=true)`]; `script --export` / `export_png` show the trimmed page
[S]; `render_page {bleed:true}` opts in.
`.jpg` path → JPEG (quality 90) [S].

## Formats [O t03, t07]
| Ext | Command behind it | Checked |
|---|---|---|
| `.pdf` | `file.exportPdf` | `pdfinfo` pages/size; rendered with pdftoppm |
| `.designcraft` | `file.saveACopy` (script `--export`) / `file.saveAs` (`--save`) | reopened |
| `.idml` | `file.exportIdml` | reopened in DesignCraft: same items |
| `.epub` | `file.exportEpub` (reflowable; `file.exportFixedEpub` fixed) | file written |
| `.html` | `file.exportHtml` | file written |
| `.pptx` | `file.exportPptx {lineBreaks?, rasterize?, embedFonts?}` | file written, N slides |
| `.rtf` `.txt` | `file.exportText` (story being edited / selected frame) | [D] |
Other targets via commands: `file.package`, `file.printBooklet`, `book.exportPdf`, `snippet.export` [D].

## PDF options — `file.exportPdf` / `--pdf-options` [O]
`{path?, pages?: "1-3,5", spreads?, bleed?: bool, marks?: bool|{crop,bleed,pageInfo,…}, standard?: none|x4|x1a|a2b,
flatten?, compressImages?, tagged?, title?, author?, created?}` → `{path, bytes, pages, warnings}`.
- Bleed must exist in the document: `file.new {bleed}` or, for an existing doc,
  `layout.documentSetup {bleed: 8.504}` (3 mm) [O agent validation]; then extend edge art to
  `[-bleed, -bleed, W+bleed, H+bleed]` (e.g. `transform.set {ids, x:-b, y:-b, width:W+2b, height:H+2b, ref:0}`).
- `marks:true` prints crop + bleed marks **and a page-info line** (title, page, date); pass an object
  `marks: {crop:true, bleed:true, pageInfo:false}` to choose [O page-info seen; object form D].
- `bleed:true` + `marks:true` on A4 with 9 pt bleed gave MediaBox 661×908, TrimBox = A4 [O t07].
- `standard:"x4"` writes PDF/X-4; RGB **swatches** on fills/strokes/gradients produce warnings (CMYK output intent) [O]; a placed sRGB
  JPEG produced none [O agent validation].
- `spreads: true` writes one PDF page per spread — render it with `pdftoppm` to get a trimmed PNG of a
  whole spread (page PNGs from `run` are per page and include bleed) [O agent validation].
- `pages` is **1-based** here; page indices in `render_page`/`--page` are 0-based.

## Validate [O]
```sh
designcraft-cli validate-pdf out.pdf            # JSON {valid, issues}; exit 1 when invalid
pdfinfo out.pdf ; pdfinfo -box out.pdf          # page count, size, trim/bleed boxes
pdftoppm -r 50 -png out.pdf check               # render the PDF itself and look at it
designcraft-cli run --in doc.designcraft --cmd 'preflight.run={"minPpi":300}'
python3 scripts/dc_check.py doc.designcraft --margins
```
A normal (non-X) PDF always "fails" `validate-pdf` — it only checks PDF/X conformance [O].
Compare the PDF render to the PNG render: fidelity, fonts (`pdffonts`), page count.

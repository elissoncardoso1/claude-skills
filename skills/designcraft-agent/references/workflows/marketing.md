# Flyer / poster / commercial material (print)

Generator: `scripts/recipes/flyer_gen.py OUT.dcs IMAGE` (A5 single page, 3 mm bleed, CMYK swatches,
photo top, display title, 3 aligned info blocks, accent bar). Exported PDF/X-4 validated
`valid: true` [O].

- `file.new {preset:"A5", facingPages:false, margins, bleed}`; background and photo extend to
  `[-bleed, -bleed, W+bleed, …]`.
- Colours: `swatch.create` with CMYK values; RGB swatches cause preflight/PDF-X warnings.
- Display type: big size with tight leading (`leading` < size), forced line break `\u2028` to break
  a title without a new paragraph.
- Info row: compute equal columns `(W - 2M - 2*gutter)/3`; `object.align {edge:"top", to:"selection", ids}`.
- Business card / postcard / posters: same recipe with presets `Business Card`, `Postcard`, `A3`…`A0`.
- VERIFY: `dc_check.py --margins` → only the bleed items may warn (`pastPageEdge`); text ≥ 8 pt.
- EXPORT print: `run --in F --pdf-options '{"standard":"x4","bleed":true,"marks":true}' --export print.pdf`
  then `designcraft-cli validate-pdf print.pdf` (must be `valid: true`) and `pdfinfo -box` (TrimBox = page size).
  Digital: `--pdf-options '{}' --export web.pdf` and `--export flyer.png`.

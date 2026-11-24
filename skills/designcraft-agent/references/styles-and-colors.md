# Swatches, colours, gradients, strokes, effects

## Colour values accepted [O]
`"#rrggbb"` · `[r,g,b]` (0–255) · `{"c","m","y","k"}` (0–100) · `{"model": "rgb"|"cmyk"|"gray", …}` (0–1).

## Two ways to colour an object [O]
| | Command | Result |
|---|---|---|
| Unnamed colour (quick) | `object.color {color, target?: fill|stroke, text?: bool, ids}` | creates swatch `R=31 G=78 B=121` → `{swatch}` |
| Named swatch (preferred for consistent docs) | `swatch.create {name, color, spot?}` then `object.fill {swatch, tint?: 0..1, ids}` | reusable, editable in one place |

Built-in swatches: `[None]`, `[Registration]`, `[Paper]`, `[Black]` plus CMYK process defaults
(`C=100 M=0 Y=0 K=0`, `C=0 M=100 Y=0 K=0`, `C=0 M=0 Y=100 K=0`, `C=15 M=100 Y=100 K=0`,
`C=75 M=5 Y=100 K=0`, `C=100 M=90 Y=10 K=0`). Unknown swatch name → error
`no swatch named \`X\`; create one with \`swatch.create\`` [O].
With nothing selected and no `ids`, `object.fill`/`object.color` set the default for **new** shapes [D].

Print intent: RGB swatches trigger preflight warnings (`rgbColor`) and PDF/X-4 issues; define CMYK
swatches for print jobs [O t05].

## Strokes [O]
`object.stroke {swatch?, tint?, weight?, align?: center|inside|outside, type?: {kind: solid|dashed|dotted|…, pattern?: [dash,gap]}, cap?, join?, start?/end? (arrowheads), ids}`.
Lines (`line.create`) get `[Black]` 1 pt by default; frames get no stroke [O].

## Gradients [O]
- On an object: `object.gradient {kind: linear|radial, stops: [{location 0–100, color | swatch, opacity?, midpoint?}], angle?, ids}`.
  `angle: 90` ran the first stop at the **bottom** → last stop at top (t03: black bottom, white top).
  Verify direction in a render.
- As swatch: `swatch.create {name, gradient: {kind, stops: [{location, swatch}]}}` then `object.fill {swatch: name}`.

## Transparency & effects [O / D]
- `object.opacity {opacity: 0..1, blend?, ids}` [O].
- `object.dropShadow {on?, distance?, angle?, opacity?, size?, color?, mode?, ids}` [O applied].
  Also `object.innerShadow`, `object.outerGlow`, `object.innerGlow`, `object.bevel`, `object.feather`,
  `object.gradientFeather` [D]. Effects are flattened/rasterised in some exports (warnings on stderr).
- Object styles: `style.object.create/apply/edit` [D].

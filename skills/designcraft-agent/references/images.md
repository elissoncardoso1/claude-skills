# Images

Formats for `file.place`/`place_image`: PNG, JPEG, WebP, GIF, TIFF (also BMP, PSD composite, EPS
preview, PDF pages per architecture docs [D]). JPEG and PNG exercised [O].

## Place [O t03, t06]
| Goal | Call |
|---|---|
| New frame at a position, height from aspect ratio | `file.place {path, x, y, width, spread?}` → `{asset, id}` |
| Into an existing frame | `frame.create {rect, content:"graphic"}` → `file.place {path, frame: id}` → `object.fit {mode, ids:[id]}` |
| From MCP | `place_image {path | base64, frame? | x,y,width}` |

- Relative `path` resolves against the **process working directory** (script: where you ran the CLI).
  Use absolute paths in MCP.
- Placed images are **embedded** in the saved `.designcraft` (`assets/`) [O].
- The image item `kind` is `<image>`; placing into a frame keeps the frame id [O].

## Fit — `object.fit {mode, ids}` [O fillProportionally; others D]
`fillProportionally` (cover, crops) · `fitProportionally` (contain) · `fitContentToFrame` (stretch) ·
`centerContent` · `fitFrameToContent`. Crop/position the content with
`transform.set {content: true, …}` [D].

## Quality checks [O]
- No distortion: `selection.set {ids:[frame]}` → `select.content {}` → `transform.info {}` → read
  `content.scaleX == content.scaleY` (the top-level scale is the frame's) [O agent validation].
- Print needs ≥ 300 ppi effective (≥ 150 acceptable for screen): run `dc_check.py --min-ppi 300` for print jobs.
- `preflight.run {minPpi: 300}` reports `lowResolution` with effective ppi per image.
- HTML/EPUB export warns about missing alt text; set it with `object.altText` [D] (`describe`).
- Text wrap around images: `object.textWrap` on the image (see typography.md).
- Colour palette from an image: `color.extractTheme {id}` → `swatch.addColorTheme {colors, name}` [D].

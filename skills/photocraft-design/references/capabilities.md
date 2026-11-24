# Capabilities: intent → commands → verification

Params are intentionally not listed. Before running anything, read the live doc:
MCP `command_list {filter:"imageSize"}` · CLI `photocraft-cli commands --json --filter imageSize`.
`params` doc syntax: `"key":min..max=default`, `"a|b"` enum, `?` optional, `id` = layer id, `index` = document index, `→ {…}` = result shape.

Status: ✅ verified on 0.12.0 · 📄 documented only · ❔ not verified.

| Intent | Engine commands (search words) | Preconditions | Destructive | Verify with | Status |
|---|---|---|---|---|---|
| open / create | MCP `doc_open`, `doc_new`; CLI `run <file>` / `run --new '<file.new json>'` | MCP: under root | – | return size/layers | ✅ |
| inspect | `doc_inspect`, `layer.list {flat:true}`, `type.info`, `shape.info`, `document.sampleColor {x,y}`, `file.fileInfo {}`; CLI `info` | doc open | – | – | ✅ |
| resize | `image.imageSize` (one side keeps ratio) · `file.automate.fitImage` 📄 | doc | pixels | result `{width,height}` + info | ✅ |
| crop / new aspect | `image.crop {x,y,width,height,targetWidth,targetHeight}` · `image.canvasSize {width,height,anchor,extensionColor}` · `image.trim` 📄 | doc | pixels | dims + look at framing | ✅ |
| layers | `layer.new.layer`, `layer.select {layer\|name}`, `layer.setProps {opacity 0..1, blend, visible, name}`, `layer.duplicate`, `layer.delete`, `layer.arrange.*`, `layer.align.* {to:"canvas"}`, `layer.distribute.*` (≥3) | doc | no | `layer.list` | ✅ (align/new/select/setProps) |
| selection | `select.rect`, `select.lasso`, `select.magicWand`, `select.colorRange`, `select.modify.*`, `select.refineEdge`; `select.subject/sky/object` ❔ | doc | no | `doc_inspect.selectionBounds` | ✅ rect |
| colour, editable | `layer.newAdjustmentLayer.<kind>` (curves, levels, hueSaturation, colorBalance, vibrance, exposure, photoFilter, blackWhite, gradientMap, selectiveColor, colorLookup…); edit with `layer.setAdjustment {layer,…}`; limit to one layer with `layer.createClippingMask` | doc; a selection becomes its mask | no | inspect `adjustment.params` + preview | ✅ |
| colour, baked | `image.adjustments.<kind>` | pixel layer active | yes | preview | ✅ |
| filter | `filter.<group>.<name>`; editable: `filter.convertForSmartFilters` (new layer id!) then the filter; edit with `layer.smartFilter.setParams {layer,index,params}` | pixel layer or smart object | pixel: yes / smart: no | `smartFilters[]` + preview | ✅ |
| text | `type.create {x,y,text,font,fontStyle,size,color,align,box?}`, `type.edit {layer,text}`, `type.setStyle {layer,size,tracking,…}`, `type.info`, `type.fonts {family}`, `type.resolveMissingFonts {}` | font installed | no | `type.info`, result `warnings`, preview | ✅ |
| shapes / fills | `shape.create {kind:rect\|roundedRect\|ellipse\|polygon\|star\|line\|path, rect:[x,y,w,h], fill, stroke}`, `shape.edit`, `layer.newFillLayer.solidColor\|gradient` | doc | no | `shape.info` + preview | ✅ |
| layer styles | `layer.layerStyle.dropShadow\|stroke\|outerGlow\|colorOverlay\|gradientOverlay\|…` (opacity 0..100) | active layer | no | `effects.items[]` + preview | ✅ dropShadow |
| masks | `layer.layerMask.revealSelection\|hideSelection\|revealAll\|hideAll\|fromTransparency\|edit`, `layer.vectorMask.*`, `layer.createClippingMask` | layer (+ selection) | no | `hasMask`, `clipped` + preview | ✅ |
| place asset | MCP `doc_place {path, center, scale, fit}` → smart object; CLI `file.placeEmbedded` ❔ | asset under root | no | `{layer,bounds,scale}` | ✅ MCP |
| transform layer | `edit.transform {layer, dx, dy, scaleX, scaleY, rotate}` | layer | pixel layer: resampled | bounds + preview | 📄 |
| save editable | MCP `doc_save {path:"x.pcraft"\|"x.psd"}`; CLI `--out x.pcraft`, `convert a.pcraft b.psd` | – | – | info / type.info on the file | ✅ |
| export flat | MCP `doc_export {path, quality}`, `doc_export_layers {dir}`; CLI `convert in out.png\|jpg\|webp [--quality]` | – | – | warnings, info dims, view PNG | ✅ |
| batch | CLI `batch --actions a.json --in D --out D2` | out ≠ in | – | ok/FAIL, exit, sample audit | ✅ |
| preview | MCP `render_preview {max_side ≤2048}`; CLI: export PNG + view | – | – | – | ✅ |
| undo | `edit.undo`, `edit.redo`, `history.newSnapshot`, `history.selectState` | history | – | `doc_inspect.history` | ✅ undo |
| templates | `image.variables.define`, `doc_import_data_sets`, `doc_export_data_sets` | variables | – | – | 📄 |
| live app | `ui_*`, `control_call` | bridge | – | `ui_screenshot` | ❔ |

Typical result shapes seen: `layer.new.layer` → `{layer}`; `type.create` → `{layer, bounds:[x0,y0,x1,y1], warnings?}`; `doc_place` → `{layer, bounds, scale, smartObject}`; `image.crop` → `{documentWidth, documentHeight, …}`; `command_batch` → `{completed, failed, results[]}`.

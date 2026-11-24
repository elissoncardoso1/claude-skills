# Capabilities (intent → commands → verification)

Status: ✅ confirmed on 0.15.0 · 📄 documented only · ⚠️ works with a caveat. Full catalogue with evidence: `references/data/capabilities-0.15.0.json` (snapshot of the validated CLI; `vc_preflight.py` checks that every engine command it names still exists in the installed CLI). Always read params live.

| Intent | Tool / engine commands | Verify | Caveat |
|---|---|---|---|
| new document / artboards ✅ | `run_command file.new {width,height,units,artboards,artboardLayout,colorMode}`; `artboard.new/setProps/fitToArt` | `inspect_document {depth:0}` artboards | new doc becomes active; old ones stay open |
| inspect ✅ | `inspect_document`/`doc_inspect {depth,ids,kind,limit}`; `document.find {name,kind,text}`; `document.node {id}` (full JSON); resource `vectorcraft://object/{id}` | — | full inspect is verbose; summary omits effects |
| primitives ✅ | `draw_shape` (rectangle radius, ellipse, polygon, star, line) | bounds, kind | explicit fill+stroke |
| paths ✅ | `draw_path {points|d, closed}`; `path.create/setAnchors/appendAnchor/close/curvature` | anchors, closed | handles absolute |
| edit anchors ✅ | `path.moveAnchor/setHandle/insertAnchor/removeAnchor/convertAnchor/split/join/reverse`, `object.path.simplify {tolerance|level}` → `{before,after}`, `offsetPath`, `outlineStroke`, `cleanUp` | anchors before/after | simplify/offsetPath/outlineStroke take no `ids`: select first; simplify keeps corners past the tolerance |
| paint ✅ | `set_paint` (also sets default!), `paint.setFill/setStroke`, `stroke.set {weight,cap,join,dash,align}`, `object.setProps {opacity,blend,name,data}` | fill/stroke/strokeOptions | colours [r,g,b] 0..1; opacity 0..100 |
| gradient ✅ linear | `fill:{gradient:{kind,angle,stops:[{offset,color}]}}`; `paint.editGradient`, `paint.setGradientGeom` | fill "Linear gradient"; SVG `<linearGradient>` | perceptual/dither/freeform export as images |
| transform ✅ | `transform {dx,dy,rotate,scale,reflect,shear,origin,copy,ids}`; `object.rotate/scale/move/reflect/setBounds` | bounds, rotation | CCW degrees |
| align/distribute ⚠️ | `select.set {ids}` → `object.align {horizontal|vertical, to}` / `object.distribute` / `object.distributeSpacing` | compare edges/centres | no `ids` param; ignored silently |
| booleans ✅ | `pathfinder {operation, ids}` (destructive); live: `apply_effect {effect:"pathfinder.add"…}` on a group 📄 | returned ids, anchors | result named after back object |
| group/order ✅ | `object.group/ungroup`, `object.arrange.*`, `object.compoundPath.make` | children order (first = front) | |
| layers ⚠️ | `layer.new {name}` → `layer.setCurrent {id}` → `object.arrange.sendToCurrentLayer {ids}`; `layer.setProps` | `currentLayer`, childCount | without setCurrent: silent no-op |
| text ✅ | `add_text {text,x,y,size,font,color,justify,width,height,fit,path,mode}`; `text.setStyle`, `text.setRangeStyle {start,end}` | bounds, `overflow`, `text.missingFonts` | y = baseline; bytes offsets |
| fonts ✅ | `text.fontList {family}`, `text.fonts`, `text.missingFonts`, `text.replaceFont` | status exact | missing = silent fallback |
| outlines ✅ export | `export {outlineText:true}` / `convert --outline-text`; doc: `type.createOutlines` 📄 | no Type kinds, fonts [] | PDF: `options.advanced.outlineText` |
| live effects ✅ | `apply_effect {effect, params, ids}`, `draw_* {effects:[…]}`, `effect.setParams/remove` | `document.node` appearance.effects + preview | 115 ids; read `vectorcraft://effect/{id}` |
| clipping ✅ | `object.clippingMask.make {ids}` (topmost clips) | kind Clip Group; SVG `<clipPath>` | mask path loses paint |
| recolor ✅ | `select.all` (or `select.set`) → `recolor.colors` → `recolor.apply {map:{"#old":"#new"}}`; `recolor.reduce`; `swatch.list/new/edit` | recolor.colors after | needs a selection ("select artwork to recolour") |
| symbols ✅ | `symbol.new {name,ids,registration}`, `symbol.place {name,x,y}`, `symbol.list` | instances; SVG `<symbol>/<use>` | x,y = registration point |
| charts ✅ | `create_graph {type,x,y,width,height,csv}`; `graph.setData/setType` | values vs input; labels inside artboard | default black; labels outside plot |
| image trace ✅ | `open_file img` → `select.all` → `imageTrace.makeAndExpand {preset, params}`; presets via `imageTrace.presets` (~15 KB) | `{paths,anchors,colors}` + preview vs source | big images slow; gradients band |
| save editable ✅ | `save_file {path:".vectorcraft"|".pdf"|".ai"}` | `vectorcraft-cli info` kinds equal | retargets the document |
| export ✅ | `export {path,format,scale,artboard,range,selection,outlineText,options}`; CLI `convert` | reply bytes/warnings/files; info; view PNG | overwrites silently |
| open/import ✅ | `open_file {path}`; `run_command file.list {path}`; `document.pdfInfo` | warnings, missingLinks | inside read root |
| preview ✅ | `screenshot {scale,artboard,path}`, `render_preview {artboard,max_side}` | — | small artboard → use screenshot |
| undo ✅ | `undo`, `redo`, `command_batch {atomic:true}` | `history` | no-op calls add no step |
| batch ✅ | `command_batch`; CLI `run --commands file`; shell loops | completed/failed; exit code | |
| discover ✅ | `command_list {filter|menu, brief}`; resources `vectorcraft://commands|command/{id}` | — | full catalogue ~430 KB |
| live UI ❌ not verified | `inspect_ui`, `open_panel`, `type_text`, `ui_screenshot` | — | headless: error |

Tested outside the table (M35): opacity masks `transparency.makeOpacityMask {ids}` (top object = mask, white = opaque), patterns `object.pattern.make {ids,name,width,height,edit:false}` then `fill:{swatch}`, blends `object.blend.make {ids,steps}`, warp envelopes `object.envelope.makeWithWarp {ids,style,bend}`, type on path `text.createInPath {path,mode:"onPath",text}`. Export paths must be in an existing folder.

Not mapped but present (discover live): perspective grid, mesh, Live Paint, Shape Builder, brushes, graphic styles, char/para styles, variables/datasets, Export for Screens, slices, CSS export, print.

# Document model (0.15.0)

- Units: points; y down; origin = top-left of artboard 0. New doc default 612×792. `units` only changes display. In SVG 1 pt = 1 px.
- Artboards: `inspect_document.artboards[] {x,y,width,height,name}`; `info.artboards[].rect [x,y,w,h]`. `file.new {artboards:N}` → row, 20 pt apart.
- Tree: `layers[]` top of stack first; each node `{id, kind, name, bounds{x,y,width,height}, visible, locked, children?}`; shapes add `fill`, `stroke`, `strokeWidth`, `strokeOptions{cap,join,dash,align,…}`, `anchors`, `closed`, `rotation?`; type adds `text`.
- Kinds seen: Layer, Group, Clip Group, Path, Compound Path, Rectangle, Rounded Rectangle, Ellipse, Line, Type, Image, Symbol. Use them in `doc_inspect {kind}` / `document.find {kind}` (exact label).
- Paint labels in summaries: `"#rrggbb"`, `"None"`, `"Linear gradient"`, swatch labels. Full paint: `document.node {id}` or `paint.proxies`.
- Inspect state too: `selection`, `currentLayer`, `history`, `redo`, `paint` (the current default for new art — check it if you rely on defaults), `revision`, `path` (file the doc saves to), `dirty`.

Full object JSON (`document.node {id}`):

```json
{"id":2,"name":"a",
 "kind":{"type":"path",
   "live":{"shape":"rectangle","w":60,"h":60,"radii":[0,0,0,0],"xf":[1,0,0,1,30,30]},
   "path":{"subpaths":[{"anchors":[{"p":[30,30]},{"p":[90,30],"in":[..],"out":[..]}],"closed":true}]}},
 "appearance":{"items":[{"kind":"fill","paint":{"type":"solid","color":{"model":"rgb","r":0.9,"g":0.22,"b":0.2}}},
                        {"kind":"stroke","paint":{"type":"none"},"width":4}],
               "effects":[{"id":"stylize.dropShadow","params":{…},"visible":true}]}}
```

- `xf` = affine [a,b,c,d,e,f]; anchors absolute; colours 0..1. Appearance can hold several fills/strokes (`appearance.addFill/addStroke`, `item` param).
- IDs are per open document and not kept by SVG round-trips; names are (`id="name"` in SVG).
- Objects may sit outside artboards; exports crop to the artboard.

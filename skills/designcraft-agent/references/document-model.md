# Document model, pages, spreads, geometry

## Session and documents [O]
- A session holds several documents; `file.new`/`file.open`/`open_document` add one and make it
  active (`{"index": n}`). `document.list` lists them, `file.activate` switches, `file.close` closes.
- Headless CLI/MCP sessions start with an empty Letter doc (index 0), so your first `file.new` is index 1.
- Ids are document-wide integers assigned in creation order; they are **not** stable across
  documents or versions. Always use returned ids or `document.inspect`.

## Creating a document — `file.new` [O]
`{preset?, intent?: print|web|mobile, units?, width?, height?, pages?, startPage?, facingPages?,
columns?, gutter?, margins?: n | {top,bottom,inside,outside}, bleed?, slug?, title?, primaryTextFrame?}`
- Presets (`file.presets`, 0.17.2): Letter, Legal, Tabloid, Letter - Half, A0–A6, B5, Business Card,
  Postcard, Web 1920 × 1080, Web 1366 × 768, Web 1024 × 768, Mobile 1080 × 1920, Mobile 390 × 844,
  Tablet 1024 × 1366. Custom: `width`/`height` in **points**.
- `facingPages` defaults to **true** for print presets: page 1 alone on spread 0 (right page), then
  spreads of two (left+right). Set `false` for independent pages.
- `startPage: 2` with `facingPages: true, pages: 2` makes a standalone spread: spread 0 = left page 2
  (x 0..W) + right page 3 (x W..2W) — no blank page 1 [O agent validation].
- `units` only changes UI display; command coordinates stay in points [O t06].
- Read back bleed/slug: `layout.documentSetup {}` (no params) returns the setup incl. `bleed: [t,b,in,out]`;
  `document.inspect` has no bleed key [O agent validation].
- `bleed` (points) extends the export area when exported with `bleed: true` [O t07].
- Default gutter 12 pt; default margins 36 pt; facing pages on for Letter [O t08].

## Coordinates [O][D]
- Points (1/72 in), y down, **per spread**: spread origin = top-left of its first page.
- Facing spread: left page x ∈ [0, W], right page x ∈ [W, 2W] (e.g. A4 W = 595.276).
- Page 1 of a facing doc is alone on spread 0 at x ∈ [0, W].
- `document.inspect` → `spreads[].pages[].bounds`, `margins`, `columnRects`, `side` — read them
  instead of computing by hand.
- `rect` is `[x0, y0, x1, y1]` (corners, not x/y/w/h). `transform.set` uses x/y/width/height measured
  from the ruler zero point and a reference point `ref` 0..8.
- Common sizes (pt): Letter 612×792 · A4 595.276×841.89 · A5 419.528×595.276 · 16:9 slide e.g. 960×540.

## Pages [O]
| Task | Command |
|---|---|
| Add pages | `layout.pages.insert {count?, after?/before? (0-based), parent?}` → `{pages, total}` |
| Delete / move / duplicate | `layout.pages.delete`, `layout.pages.move`, `layout.pages.duplicateSpread` (`describe` first) |
| Margins & columns | `layout.marginsAndColumns {pages?, margins?, columns?, gutter?}` |
| Page size | `layout.pageSize` (`describe`) |
| Sections / numbering | `layout.section {page (1-based), startNumber?, style?, prefix?}` |
| Guides | `guide.add {orientation: horizontal|vertical, position, spread?, page?}` |

A command addressing a spread that doesn't exist fails with `no spread Doc(N)` — insert pages first.

## Parent pages (masters) [O t04]
- Every new doc has parent `A-Parent` (id in `document.inspect.parents`), applied to all pages.
- Create items on a parent: any creation command with `"spread": {"kind": "parent", "index": 0}`.
  Parent spreads of facing docs are two pages wide: right-page items at x + W.
- Page number marker: text `\ue000` (current page), `\ue007` next, `\ue008` previous.
- `layout.parents.new {prefix?, name?}`, `layout.pages.applyParent {pages:[idx], parent:"B"|null}`,
  `layout.overrideParentItems`, `layout.parents.delete {id}`.

## Layers [O t03, t06]
- Default `Layer 1`. `layer.new {name}` → `{id}`; it becomes **active and topmost**.
- New items go on the **active** layer. Switch with `layer.activate {id}`.
- `layer.set {id, name?, color?, visible?, locked?, printable?}`; hidden layers don't render/export.
- `object.setLayer {layer: <id>, ids}` (a name string fails with "missing layer").
- Order: `document.inspect.layers` lists top first.

## Items in `document.inspect` [O]
`{id, kind: "<text frame>"|"<rectangle>"|"<ellipse>"|"<polygon>"|"<line>"|"<image>"|"<group>", bounds,
fill, stroke {swatch, weight}, layer, locked, hidden, name, story?, columns?, children? (groups)}`.
Items are listed back-to-front per spread. Stories: `{id, frames, length (bytes), lines, overset, paragraphs, preview}`.
Selection: `selection {items, content, text?: {story, anchor, focus}}`.

## Native file [O]
`.designcraft` = zip: `mimetype` (application/vnd.designcraft+zip), `document.json` (full model),
`meta.json` (`{"format":"designcraft","generator":"DesignCraft 0.17.2","version":2}`), `preview.png`,
`assets/<id>.<ext>` (placed images are **embedded**). Edit it only through commands, never by
rewriting the JSON (no schema guarantee) [S format crate is versioned].

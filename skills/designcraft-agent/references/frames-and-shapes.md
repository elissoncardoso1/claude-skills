# Frames, shapes, lines, paths, arrangement

## Create [O]
| Object | Command | Returns |
|---|---|---|
| Text frame | `frame.create {rect, content: "text", text?, spread?, vertical?}` | `{id, story}` |
| Graphic frame / shape | `frame.create {rect, content: "graphic"\|"unassigned", shape?: rectangle\|ellipse\|polygon, sides?, starInset? (0–100 %)}` | `{id}` |
| Line | `line.create {a: [x,y], b: [x,y], spread?}` | `{id}` |
| Path | `path.create` (+ `path.appendAnchor`, `path.close`) — `describe` first [U: not exercised] | |
| Table | `table.insert` (in a text frame; `describe`) [U] | |
| QR code | `object.qrCode` [U] | |

Type on a path [O]: `type.onPath {id: <ellipse/path/line id>, text?, start?, flip?, align?}` → `{story}`;
options via `type.pathOptions` (`describe`). Works directly on an ellipse frame (text runs clockwise
from ~9 o'clock). Format it with `selection.set` on the shape + `type.char`. Search the registry for
`onPath`/`path`, not "curved".

A star = polygon with `starInset` (5 sides + 50 % tested). An "unassigned" frame is an empty frame.

## Transform & geometry [O]
- Move/resize: `transform.set {x?, y?, width?, height?, rotation?, scaleX?, scaleY?, shear?, ref?: 0..8, ids?}`
  (absolute; rotation in degrees; `inspect` bounds become the rotated bounding box).
- Relative: `transform.move`, `transform.rotate`, `transform.scale`, `transform.flip` (`describe`).
- `transform.info {ids?}` → scale/rotation/shear of the first target.
- Corners: `object.cornerOptions {shape: none|rounded|inverseRounded|inset|bevel|fancy, size, corners?, ids?}`.

## Arrange [O]
- `object.align {edge: left|hcenter|right|top|vcenter|bottom, to?: selection|keyObject|margins|page|spread, ids?}`
- `object.distribute {axis: horizontal|vertical, by?: centers|spacing, spacing?, ids?}`
  (`by: "spacing"` without `spacing` = equal gaps between the outer objects).
- `object.group {ids}` → `{id}`, `object.ungroup`; rename with `object.rename {id, name}`.
- Z-order: `object.arrange {to: front|forward|backward|back, ids?}` (within the layer).
- Lock/hide: `object.lock`, `object.hide`, `object.showAll`, `object.unlockAll`.
- Selection: `selection.set {ids, add?}`, `edit.deselectAll`, `edit.selectAll`.
- Duplicate: `edit.duplicate`, `edit.stepAndRepeat` (`describe`).

## Text frame options [O]
`object.textFrameOptions {columns?, gutter?, inset?, verticalJustification?: top|center|bottom|justify,
autoSize?: off|heightOnly|widthOnly|heightAndWidth…, autoSizeReference?, ids?}` — columns=2/3 tested. `balanceColumns: true` evens out column heights when copy is short [O agent validation].
`autoSize: heightOnly` grows the frame around its **center** by default [O t08]; add
`"autoSizeReference": "topLeft"` to keep the top edge fixed [D: from `describe`, not exercised].
Text wrap: `object.textWrap {mode: none|boundingBox|contour|jumpObject|jumpToNextColumn, offset?, ids?}`
on the **obstacle** (e.g. the image) [O t07].

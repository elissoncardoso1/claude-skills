# Example: 24 px "home" icon via MCP (verified 2026-10-23, test M32)

```json
command_batch {"atomic": true, "label": "icon home", "steps": [
 {"id": "file.new", "params": {"width": 24, "height": 24, "name": "icon-home", "units": "Pixels"}},
 {"id": "draw_path", "params": {"points": [[3,10.5],[12,3],[21,10.5]], "fill": "none", "stroke": "#111111", "strokeWidth": 2, "cap": "round", "join": "round", "name": "roof"}},
 {"id": "draw_path", "params": {"d": "M5 9 L5 20 L19 20 L19 9", "fill": "none", "stroke": "#111111", "strokeWidth": 2, "cap": "round", "join": "round", "name": "walls"}},
 {"id": "draw_path", "params": {"d": "M10 20 L10 14 L14 14 L14 20", "fill": "none", "stroke": "#111111", "strokeWidth": 2, "cap": "round", "join": "round", "name": "door"}},
 {"id": "object.group", "params": {"ids": ["$1.id", "$2.id", "$3.id"]}},
 {"id": "object.setProps", "params": {"id": "$4.id", "name": "icon-home"}}]}
→ completed 6, failed 0, created [2,3,4]
```

Look: `screenshot {scale: 8}` (sharp) and `render_preview {max_side: 24}` (real size). `render_preview {max_side: 192}` on this 24 pt artboard is blurry — don't judge from it.

Save/export (new names, inside the write root that `vc_preflight.py` reports):

```json
save_file {"path": "<write root>/<project>/icon-home.vectorcraft"}
export    {"path": "<write root>/<project>/icon-home.svg", "options": {"decimals": 2}}   → 717 bytes, no warnings
```

Check: `python3 scripts/vc_check.py icon-home.vectorcraft --stroke 2 --cap round --join round --no-raster` → no problems.

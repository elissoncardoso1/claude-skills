#!/usr/bin/env python3
"""Translate a design-token + icon-spec JSON into VectorCraft steps (JSON array).

VectorCraft has no native design tokens; this keeps them outside and emits only verified commands
(file.new, select.none + paint.default [reset of inherited paint, M31], swatch.new, path.create, paint.setFill/setStroke, stroke.set, object.group, object.setProps).
Colours are also saved as global swatches, but the strokes are painted with the hex value (NOT linked
to the swatch), so swatch.edit will not recolour them; recolor.apply does.

Icon path data must be ABSOLUTE M/L/C/Z (commas or spaces; Z/z close). H/V/S/Q/A and relative
commands are refused with an error naming the icon: convert them first.

Steps use the key "id", which both accept as-is:
  tokens_to_steps.py TOKENS.json > steps.json
  vectorcraft-cli run --commands steps.json --export OUT.vectorcraft      (CLI)
  command_batch {"steps": <steps>, "atomic": true}                         (MCP, max 256 steps)

Icon k is drawn on artboard k, offset by k * (grid.size + grid.artboardSpacing) on x, which is
where file.new {artboards:N, artboardLayout:{layout:"row", spacing}} places it.
Required keys: name, grid{size, artboardSpacing}, stroke{width, cap, join}, color{ink,...}, icons[{name, paths}].
"""
import json, re, sys

NUM = r"-?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?"

def offset_d(d, dx):
    """Shift every x of an absolute SVG path (M/L/C/Z) by dx; raise ValueError on anything else."""
    tokens = re.findall(rf"[A-Za-z]|{NUM}|\S", d.replace(",", " "))
    out, i = [], 0
    for t in tokens:
        if t in "MLCZz":
            i = 0; out.append(t.upper()); continue
        if re.fullmatch(NUM, t) is None:
            raise ValueError(f"unsupported path command {t!r}: only absolute M/L/C/Z")
        v = float(t) + (dx if i % 2 == 0 else 0); i += 1
        out.append(f"{v:g}")
    return " ".join(out)

def steps(tok):
    g, s, icons = tok["grid"], tok["stroke"], tok["icons"]
    step = g["size"] + g["artboardSpacing"]
    out = [{"id": "file.new", "params": {"name": tok["name"], "width": g["size"], "height": g["size"],
            "units": "Pixels", "artboards": len(icons),
            "artboardLayout": {"layout": "row", "spacing": g["artboardSpacing"]}}},
           {"id": "select.none", "params": {}}, {"id": "paint.default", "params": {}},   # M31: drop inherited paint
           {"id": "swatch.new", "params": {"colors": list(tok["color"].values()), "global": True}}]
    for k, icon in enumerate(icons):
        first = len(out)
        for d in icon["paths"]:
            try:
                shifted = offset_d(d, k * step)
            except ValueError as e:
                raise ValueError(f"icon {icon['name']!r}, path {d!r}: {e}") from None
            out.append({"id": "path.create", "params": {"d": shifted}})
            out.append({"id": "paint.setFill", "params": {"none": True}})
            out.append({"id": "paint.setStroke", "params": {"color": tok["color"]["ink"]}})
            out.append({"id": "stroke.set", "params": {"weight": s["width"], "cap": s["cap"], "join": s["join"]}})
        ids = [f"${i}.id" for i in range(first, len(out), 4)]
        out.append({"id": "object.group", "params": {"ids": ids}})
        out.append({"id": "object.setProps", "params": {"id": "$last.id", "name": f"icon-{icon['name']}"}})
    return out

def selftest():
    assert offset_d("M3 10.5 L12 3", 44) == "M 47 10.5 L 56 3", offset_d("M3 10.5 L12 3", 44)
    assert offset_d("M1 2 C3 4 5 6 7 8 Z", 10) == "M 11 2 C 13 4 15 6 17 8 Z"
    assert offset_d("M1e1 2 L3,4z", 1) == "M 11 2 L 4 4 Z"
    for bad in ("M3 10 H 20 V 5", "M3 10 l5 5", "M0 0 A 5 5 0 0 1 10 10"):
        try: offset_d(bad, 44); raise AssertionError(f"accepted {bad}")
        except ValueError: pass
    try:
        steps({"name": "t", "grid": {"size": 24, "artboardSpacing": 20}, "stroke": {"width": 2, "cap": "round", "join": "round"},
               "color": {"ink": "#000000"}, "icons": [{"name": "bad", "paths": ["M1 1 H 5"]}]})
        raise AssertionError("bad icon accepted")
    except ValueError as e:
        assert "icon 'bad'" in str(e), e
    import vc_common
    good = steps(json.load(open(vc_common.SKILL_DIR / "examples/icon-tokens.json")))
    assert [s["id"] for s in good[:3]] == ["file.new", "select.none", "paint.default"], good[:3]
    assert vc_common.validate_steps(good) == [], vc_common.validate_steps(good)
    refs = [r for s in good for r in vc_common.walk_strings(s.get("params", {})) if r.startswith("$")]
    assert all(good[int(r[1:].split(".")[0])]["id"] == "path.create" for r in refs if r[1].isdigit()), refs
    print("selftest ok")

if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        selftest(); sys.exit(0)
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    try:
        print(json.dumps(steps(json.load(open(sys.argv[1]))), indent=1))
    except (ValueError, KeyError, OSError) as e:
        sys.exit(f"tokens_to_steps: {type(e).__name__}: {e}")

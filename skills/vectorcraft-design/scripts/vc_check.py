#!/usr/bin/env python3
"""Structural check of a VectorCraft-readable file through `vectorcraft-cli` (no MCP needed).

Usage: vc_check.py FILE [--icon] [--pad P] [--stroke W] [--cap C] [--join J] [--no-raster] [--json]
Prints artboards, kinds, fonts, and PROBLEMS:
  - objects whose bounds leave every artboard (cut on export)
  - missing/substituted fonts
  - Image objects when --no-raster
  - with --pad P: art (stroke included: bounds grown by strokeWidth/2) closer than P to its artboard edge
  - stroked paths whose width/cap/join differ from the expected, or from each other with --icon
    (stroke checks are off for general art, where mixed strokes are normal)
NOTES (printed, not failures): hidden objects/layers and template layers, which exports leave out.
Exit 1 when there are problems. Self-test: vc_check.py --selftest
"""
import argparse, json, subprocess, sys

def load(path):
    from vc_common import cli_path
    cli = cli_path()
    if cli is None:
        sys.exit("vectorcraft-cli not found (set VECTORCRAFT_CLI or put it on PATH; see vc_preflight.py)")
    import os
    if not os.path.isfile(path):
        sys.exit(f"no such file: {path}")
    r = subprocess.run([cli, "run", "--in", path, "--cmd", "document.inspect"],
                       capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"vectorcraft-cli failed: {r.stderr.strip()}")
    lines = [json.loads(l) for l in r.stdout.splitlines() if l.startswith("{")]
    info = subprocess.run([cli, "info", path], capture_output=True, text=True)
    if info.returncode:
        sys.exit(f"vectorcraft-cli info failed: {info.stderr.strip()}")
    return lines[-1]["result"], json.loads(info.stdout)

def walk(nodes):
    for n in nodes:
        yield n
        yield from walk(n.get("children") or [])

def inside(b, boards, tol=0.01):
    return any(b["x"] >= a["x"] - tol and b["y"] >= a["y"] - tol and
               b["x"] + b["width"] <= a["x"] + a["width"] + tol and
               b["y"] + b["height"] <= a["y"] + a["height"] + tol for a in boards)

def problems(doc, info, stroke=None, cap=None, join=None, no_raster=False, icon=False, pad=None):
    out, boards = [], doc["artboards"]
    leaves = [n for n in walk(doc["layers"]) if n["kind"] not in ("Layer", "Group", "Clip Group")]
    for n in leaves:
        if n.get("bounds") and not inside(n["bounds"], boards):
            out.append(f"outside artboards: id {n['id']} {n['kind']} {n.get('name')} {n['bounds']}")
        if pad is not None and n.get("bounds"):
            h = (n.get("strokeWidth") or 0) / 2 if n.get("stroke") not in (None, "None") else 0
            b = n["bounds"]; g = {"x": b["x"] - h, "y": b["y"] - h, "width": b["width"] + 2 * h, "height": b["height"] + 2 * h}
            live = [{"x": a["x"] + pad, "y": a["y"] + pad, "width": a["width"] - 2 * pad, "height": a["height"] - 2 * pad} for a in boards]
            if inside(n["bounds"], boards) and not inside(g, live):
                out.append(f"inside padding {pad}: id {n['id']} {n.get('name')} (stroke-inclusive bounds {g})")
        if no_raster and n["kind"] == "Image":
            out.append(f"raster image: id {n['id']}")
    for f in info.get("fonts", []):
        if f["status"] != "exact":
            out.append(f"font {f['family']} {f['style']}: {f['status']} -> {f['resolved']['family']}")
    stroked = [n for n in leaves if n.get("stroke") not in (None, "None") and n.get("strokeWidth")]
    seen = {(n["strokeWidth"], n["strokeOptions"]["cap"], n["strokeOptions"]["join"]) for n in stroked}
    if icon and stroke is None and len(seen) > 1:
        out.append(f"inconsistent strokes (width, cap, join): {sorted(seen)}")
    for n in stroked:
        o = n["strokeOptions"]
        if (stroke is not None and abs(n["strokeWidth"] - stroke) > 1e-6) or (cap and o["cap"] != cap) or (join and o["join"] != join):
            out.append(f"stroke id {n['id']} {n.get('name')}: {n['strokeWidth']} {o['cap']} {o['join']}")
    return out

def notes(doc):
    return [f"{'template layer' if n.get('template') else 'hidden'}: id {n['id']} {n['kind']} {n.get('name')} (left out of exports)"
            for n in walk(doc["layers"]) if n.get("visible") is False or n.get("template")]

def selftest():
    b = [{"x": 0, "y": 0, "width": 24, "height": 24}]
    so = {"cap": "round", "join": "round"}
    doc = {"artboards": b, "layers": [{"kind": "Layer", "id": 1, "children": [
        {"kind": "Path", "id": 2, "bounds": {"x": 2, "y": 2, "width": 20, "height": 20}, "stroke": "#000", "strokeWidth": 2, "strokeOptions": so},
        {"kind": "Path", "id": 3, "bounds": {"x": 20, "y": 2, "width": 10, "height": 2}, "stroke": "#000", "strokeWidth": 1.5, "strokeOptions": so},
        {"kind": "Image", "id": 4, "bounds": {"x": 0, "y": 0, "width": 1, "height": 1}},
        {"kind": "Path", "id": 5, "visible": False, "bounds": {"x": 2, "y": 2, "width": 2, "height": 2}}]}]}
    info = {"fonts": [{"family": "X", "style": "Regular", "status": "missing", "resolved": {"family": "Source Sans 3"}}]}
    p = problems(doc, info, no_raster=True, icon=True)
    assert not any("inconsistent" in x for x in problems(doc, info)), "stroke check must be opt-in"
    assert any("outside artboards: id 3" in x for x in p), p
    assert any("raster image" in x for x in p) and any("font X" in x for x in p), p
    assert any("inconsistent strokes" in x for x in p), p
    assert any("stroke id 3" in x for x in problems(doc, info, stroke=2)), "expected width check"
    assert any("inside padding 2: id 2" in x for x in problems(doc, info, pad=2)), problems(doc, info, pad=2)
    assert notes(doc) == ["hidden: id 5 Path None (left out of exports)"], notes(doc)
    print("selftest ok")

if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        selftest(); sys.exit(0)
    ap = argparse.ArgumentParser(description="Structural check of a VectorCraft-readable file")
    ap.add_argument("file"); ap.add_argument("--icon", action="store_true"); ap.add_argument("--pad", type=float)
    ap.add_argument("--stroke", type=float); ap.add_argument("--cap"); ap.add_argument("--join")
    ap.add_argument("--no-raster", action="store_true"); ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    doc, info = load(a.file)
    p = problems(doc, info, a.stroke, a.cap, a.join, a.no_raster, a.icon, a.pad)
    n = notes(doc)
    if a.json:
        print(json.dumps({"artboards": len(doc["artboards"]), "kinds": info["kinds"], "problems": p, "notes": n}, indent=1))
    else:
        print(f"{a.file}: {len(doc['artboards'])} artboard(s), kinds {info['kinds']}")
        print("\n".join([f"PROBLEM {x}" for x in p] + [f"NOTE {x}" for x in n]) or "no problems")
    sys.exit(1 if p else 0)

#!/usr/bin/env python3
"""Compact layer tree of a saved file: one short line per node instead of inspect's full JSON.

Usage: vc_tree.py FILE [--depth N]      Self-test: vc_tree.py --selftest
Line: <indent>id kind "name" x,y wxh fill=… stroke=…/width cap/join [hidden] [locked] [rot=…] [text=…]
Nodes print in document order (top of stack first), so the same file always gives the same lines.
For an MCP session: save_file the working copy (inside the root), then run this on it.
"""
import argparse, sys
from vc_check import load

def line(n):
    b = n.get("bounds")
    parts = [str(n["id"]), n["kind"], f'"{n.get("name")}"']
    if b: parts.append(f'{b["x"]:g},{b["y"]:g} {b["width"]:g}x{b["height"]:g}')
    if n.get("fill") not in (None, "None"): parts.append(f'fill={n["fill"]}')
    if n.get("stroke") not in (None, "None"):
        o = n.get("strokeOptions") or {}
        parts.append(f'stroke={n["stroke"]}/{n.get("strokeWidth") or 0:g} {o.get("cap")}/{o.get("join")}')
    if n.get("visible") is False: parts.append("hidden")
    if n.get("locked"): parts.append("locked")
    if n.get("rotation"): parts.append(f'rot={n["rotation"]:g}')
    if n.get("text"): parts.append(f'text={n["text"][:40]!r}')
    return " ".join(parts)

def tree(nodes, depth, level=0):
    for n in nodes:
        yield "  " * level + line(n)
        if depth is None or level < depth:
            yield from tree(n.get("children") or [], depth, level + 1)

def selftest():
    import os, subprocess, tempfile
    nodes = [{"id": 1, "kind": "Layer", "name": "Layer 1", "children": [
        {"id": 3, "kind": "Group", "name": "ícone-casa", "bounds": {"x": 2, "y": 2.5, "width": 20, "height": 19}, "children": [
            {"id": 2, "kind": "Path", "name": None, "bounds": {"x": 3, "y": 3, "width": 18, "height": 7.5},
             "fill": "None", "stroke": "#111827", "strokeWidth": 2, "strokeOptions": {"cap": "round", "join": "round"}}]},
        {"id": 4, "kind": "Type", "name": "t", "text": "Olá, mundo — 世界 " * 5, "visible": False, "locked": True, "rotation": 15},
        {"id": 5, "kind": "Path", "name": "no bounds", "stroke": "#000000"}]}]
    out = list(tree(nodes, None))
    assert out[0] == '1 Layer "Layer 1"', out
    assert out[1] == '  3 Group "ícone-casa" 2,2.5 20x19', out
    assert out[2] == '    2 Path "None" 3,3 18x7.5 stroke=#111827/2 round/round', out
    assert out[3].startswith('  4 Type "t" hidden locked rot=15 text=') and len(out[3]) < 120, out[3]
    assert out[4] == '  5 Path "no bounds" stroke=#000000/0 None/None', out
    assert list(tree(nodes, 0)) == out[:1] and list(tree(nodes, 1)) == [out[0], out[1], out[3], out[4]]
    assert list(tree(nodes, None)) == out, "order must be deterministic"
    assert list(tree([], None)) == []
    try:
        line({"kind": "Path"}); raise AssertionError("node without id accepted")
    except KeyError:
        pass
    # error contract: missing file / missing CLI end with a message and exit != 0, never a traceback
    with tempfile.TemporaryDirectory() as d:
        here = os.path.dirname(os.path.abspath(__file__))
        env = dict(os.environ, VECTORCRAFT_CLI=os.path.join(d, "absent-cli"))
        r = subprocess.run([sys.executable, "-B", os.path.join(here, "vc_tree.py"), os.path.join(d, "x.svg")],
                           capture_output=True, text=True, env=env)
        assert r.returncode == 1 and "not found" in r.stderr and "Traceback" not in r.stderr, r.stderr
        fake = os.path.join(d, "cli")
        open(fake, "w").write("#!/bin/sh\nexit 0\n"); os.chmod(fake, 0o755)
        env["VECTORCRAFT_CLI"] = fake
        r = subprocess.run([sys.executable, "-B", os.path.join(here, "vc_tree.py"), os.path.join(d, "missing.svg")],
                           capture_output=True, text=True, env=env)
        assert r.returncode == 1 and "no such file" in r.stderr and "Traceback" not in r.stderr, r.stderr
    print("selftest ok")

if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        selftest(); sys.exit(0)
    ap = argparse.ArgumentParser(); ap.add_argument("file"); ap.add_argument("--depth", type=int)
    a = ap.parse_args()
    doc, info = load(a.file)
    for i, ab in enumerate(doc["artboards"]):
        print(f'artboard {i} "{ab["name"]}" {ab["x"]:g},{ab["y"]:g} {ab["width"]:g}x{ab["height"]:g}')
    print("\n".join(tree(doc["layers"], a.depth)))
    bad = [f for f in info.get("fonts", []) if f["status"] != "exact"]
    if bad: print("fonts not exact: " + ", ".join(f'{f["family"]}->{f["resolved"]["family"]}' for f in bad))

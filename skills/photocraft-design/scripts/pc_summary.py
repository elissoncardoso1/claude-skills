#!/usr/bin/env python3
"""Compact structural summary of an image/document via `photocraft-cli info`.
Usage: pc_summary.py <file> [<file>…]   Exit 1 if any file fails to load."""
import json, subprocess, sys

def details(path, layers):
    """Font face and shape fill need type.info / shape.info: one extra `run` for all of them."""
    flat, todo = [], []
    def collect(ls):
        for l in ls:
            flat.append(l); collect(l.get("children") or [])
    collect(layers)
    args = ["photocraft-cli", "run", path]
    for l in flat:
        cmd = {"Type": "type.info", "Shape": "shape.info"}.get(l["kind"])
        if cmd:
            args += ["--cmd", cmd, "--params", json.dumps({"layer": l["id"]})]; todo.append(l["id"])
    if not todo: return {}
    r = subprocess.run(args, capture_output=True, text=True)
    out = {}
    for lid, line in zip(todo, [x for x in r.stdout.splitlines() if x.startswith("{")]):
        res = json.loads(line).get("result") or {}
        if "runs" in res:
            st = res["runs"][0]["style"] if res["runs"] else {}
            out[lid] = f'face={st.get("font_family")} {st.get("font_style") or ""}'.rstrip()
        elif "fill" in res:
            out[lid] = f'fill={res.get("fill")} stroke={res.get("stroke")}'
    return out

def walk(layers, info, depth=0):
    for l in layers:
        extra = []
        if l.get("text"): extra.append(f'text={l["text"].get("text")!r} font={l["text"].get("font")} {l["text"].get("sizePt")}pt')
        if l["id"] in info: extra.append(info[l["id"]])
        if l.get("adjustment"): extra.append(f'adjustment={l["adjustment"].get("kind")}')
        if l.get("smartFilters"): extra.append("smartFilters=" + ",".join(f["command"] for f in l["smartFilters"]))
        if (l.get("effects") or {}).get("items"): extra.append("effects=" + ",".join(e["kind"] for e in l["effects"]["items"]))
        if l.get("hasMask"): extra.append("mask")
        if l.get("hasVectorMask"): extra.append("vectorMask")
        if l.get("clipped"): extra.append("clipped")
        if not l.get("visible", True): extra.append("hidden")
        print(f'{"  " * depth}- [{l["id"]}] {l["kind"]} "{l["name"]}" bounds(x,y,w,h)={l.get("bounds")} '
              f'opacity={l.get("opacity")} blend={l.get("blend")} {" ".join(extra)}')
        walk(l.get("children") or [], info, depth + 1)

status = 0
for path in sys.argv[1:]:
    r = subprocess.run(["photocraft-cli", "info", path, "--compact"], capture_output=True, text=True)
    if r.returncode:
        print(f"{path}: ERROR {r.stderr.strip()}"); status = 1; continue
    d = json.loads(r.stdout)
    print(f'{path}: {d["width"]}x{d["height"]} {d["mode"]} {d["depth"]}-bit {d.get("resolution")}ppi')
    walk(d["layers"], details(path, d["layers"]))
    for w in dict.fromkeys(d.get("warnings") or []):
        print(f"  WARNING: {w}")
sys.exit(status)

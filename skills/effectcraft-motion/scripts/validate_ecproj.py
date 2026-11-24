#!/usr/bin/env python3
"""Validate an EffectCraft .ecproj (schema 2, EffectCraft 0.17.0) without opening it in the engine.

usage: validate_ecproj.py FILE.ecproj [--engine]
  --engine  also run `effectcraft-cli info --project FILE` (the real loader) and fail if it errors.
Exit 0 = valid; 1 = problems (printed one per line). Structure from crates/project/src/lib.rs,
props.rs and crates/keyframe/src (see references/ecproj-schema.md).
"""
import json, subprocess, sys

TICKS = 254_016_000_000  # Tick per second
SOURCES = {"Footage", "Comp", "Solid", "Text", "Shape", "Null", "Camera", "Light", "Model", "Primitive"}
WITH_ITEM = {"Footage", "Comp", "Solid", "Model"}
ITEM_KINDS = {"Folder", "Comp", "Footage", "Solid"}
VALUE_TAGS = {"Scalar", "Vec2", "Vec3", "Color", "Bool", "Enum", "Path", "Text", "Layer", "Gradient", "Str"}
INTERP = {"Linear", "Bezier", "Hold"}
MATTES = {"Alpha", "AlphaInverted", "Luma", "LumaInverted"}


def validate(p):
    errs = []
    e = errs.append
    if not isinstance(p, dict):
        return ["root is not an object"]
    for k in ("schema", "settings", "items", "next_id"):
        if k not in p: e(f"missing top-level `{k}`")
    if p.get("schema") != 2: e(f"schema {p.get('schema')} (this skill targets schema 2 / EffectCraft 0.17.0)")
    items = p.get("items") or {}
    if not isinstance(items, dict): return errs + ["`items` must be an object keyed by item id"]
    for iid, it in items.items():
        where = f"item {iid} ({it.get('name')!r})"
        if str(it.get("id")) != str(iid): e(f"{where}: id {it.get('id')} != key {iid}")
        kind = (it.get("kind") or {}).get("type")
        if kind not in ITEM_KINDS: e(f"{where}: kind.type {kind!r} not in {sorted(ITEM_KINDS)}"); continue
        if it.get("parent") is not None and str(it["parent"]) not in items: e(f"{where}: parent folder {it['parent']} missing")
        if kind == "Comp": check_comp(it["kind"], where, items, e)
    if items and isinstance(p.get("next_id"), int):
        biggest = max(int(k) for k in items)
        if p["next_id"] <= biggest: e(f"next_id {p['next_id']} <= largest item id {biggest}")
    return errs


def check_comp(c, where, items, e):
    for k in ("width", "height", "frame_rate", "duration", "layers", "background"):
        if k not in c: e(f"{where}: comp missing `{k}`")
    fr = c.get("frame_rate") or {}
    if not (isinstance(fr, dict) and fr.get("num", 0) > 0 and fr.get("den", 0) > 0): e(f"{where}: frame_rate must be {{num>0, den>0}}")
    if not (isinstance(c.get("duration"), int) and c["duration"] > 0): e(f"{where}: duration must be a positive Tick integer ({TICKS}/s)")
    ids = {l.get("id") for l in c.get("layers", [])}
    for l in c.get("layers", []):
        lw = f"{where} layer {l.get('id')} ({l.get('name')!r})"
        src = (l.get("source") or {}).get("type")
        if src not in SOURCES: e(f"{lw}: source.type {src!r} not in {sorted(SOURCES)}")
        elif src in WITH_ITEM and str((l["source"] or {}).get("item")) not in items: e(f"{lw}: source item {(l['source'] or {}).get('item')} missing")
        for k in ("start_time", "in_point", "out_point"):
            if not isinstance(l.get(k), int): e(f"{lw}: `{k}` must be a Tick integer")
        if isinstance(l.get("in_point"), int) and isinstance(l.get("out_point"), int) and l["out_point"] <= l["in_point"]: e(f"{lw}: out_point <= in_point")
        if l.get("parent") is not None and l["parent"] not in ids: e(f"{lw}: parent layer {l['parent']} is not in this comp")
        if l.get("parent") == l.get("id"): e(f"{lw}: parented to itself")
        tm = l.get("track_matte")
        if tm:
            if tm.get("layer") not in ids: e(f"{lw}: track matte layer {tm.get('layer')} not in this comp")
            if tm.get("kind") not in MATTES: e(f"{lw}: track matte kind {tm.get('kind')!r}")
        props = l.get("props")
        if not isinstance(props, dict): e(f"{lw}: missing props tree"); continue
        walk(props, "", lw, e, 0)


def walk(g, path, lw, e, depth):
    if depth > 64: e(f"{lw}: property tree deeper than 64"); return
    for n in g.get("children", []):
        p = f"{path}/{n.get('match')}" if path else str(n.get("match"))
        if n.get("node") == "Group": walk(n, p, lw, e, depth + 1); continue
        if n.get("node") != "Prop": e(f"{lw} {p}: node must be Prop or Group"); continue
        v = n.get("value") or {}
        if v.get("t") not in VALUE_TAGS: e(f"{lw} {p}: value tag {v.get('t')!r}")
        last = None
        for k in n.get("keys", []):
            if not isinstance(k.get("time"), int): e(f"{lw} {p}: key time must be a Tick integer"); continue
            if last is not None and k["time"] <= last: e(f"{lw} {p}: keys not strictly increasing in time")
            last = k["time"]
            if (k.get("value") or {}).get("t") != v.get("t"): e(f"{lw} {p}: key value type {(k.get('value') or {}).get('t')} != property type {v.get('t')}")
            for side in ("in_interp", "out_interp"):
                if k.get(side, "Linear") not in INTERP: e(f"{lw} {p}: {side} {k.get(side)!r}")
            for side in ("in_ease", "out_ease"):
                for ez in k.get(side, []):
                    if not (0 < ez.get("influence", 0) <= 1): e(f"{lw} {p}: ease influence {ez.get('influence')} outside (0,1]")
        ex = n.get("expr")
        if ex is not None and not isinstance(ex.get("text"), str): e(f"{lw} {p}: expr.text must be a string")


def main():
    if len(sys.argv) < 2: sys.exit(__doc__)
    path = sys.argv[1]
    try:
        doc = json.load(open(path, encoding="utf-8"))
    except (OSError, ValueError) as x:
        print(f"cannot read {path}: {x}"); sys.exit(1)
    errs = validate(doc)
    if "--engine" in sys.argv:
        r = subprocess.run(["effectcraft-cli", "info", "--project", path], capture_output=True, text=True)
        if r.returncode: errs.append("engine refused it: " + (r.stderr or r.stdout).strip())
    for x in errs: print(x)
    print("OK" if not errs else f"{len(errs)} problem(s)")
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()

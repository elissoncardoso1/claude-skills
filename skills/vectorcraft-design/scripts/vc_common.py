"""Shared helpers for vc_manifest.py, vc_replay.py and vc_preflight.py (stdlib only).

Contracts live in ../schemas/*.schema.json; validate_steps() and validate_manifest() enforce the
same rules in code (no jsonschema dependency). Self-test: python3 -B vc_common.py --selftest
"""
import hashlib, json, os, pathlib, platform, re, shutil, struct, subprocess, sys, zlib

PLUGIN_VERSION = "1.0.1"
SKILL_VERSION = "1.0.1"
MANIFEST_SCHEMA = "vectorcraft-delivery/1"
STEPS_SCHEMA = "vectorcraft-steps/1"
VALIDATED_CLI = ["0.15.0", "0.16.0"]          # SUPPORTED; anything else is UNTESTED until tests/golden/<v> exists
INCOMPATIBLE_CLI = []               # versions where the regression suite demonstrably fails
HERE = pathlib.Path(__file__).resolve().parent
SKILL_DIR = HERE.parent

# Commands that read or write files, run other commands, or touch preferences/libraries/fonts/clipboard.
# A recipe never needs them: inputs come in through `run --in`, outputs through `--export`, both decided
# by the manifest. Built from the 0.15.0 catalogue: the rule matches 185 of 802 ids (list them with
# `python3 -B vc_common.py --denied`); RECIPE_ALLOWED are in-document exceptions. action.batch and
# command.batch are denied because they run nested commands that would bypass this check.
DENIED = re.compile(r"^(file|action|command|plugin|script|prefs|library|print|links|app|window|view|clipboard|dataset|"
                    r"importMatches|assets|webExport|flattener|pdf|perspective\.presets|svgInteractivity)\.|"
                    r"^document\.(open|save|export)|save|load|import|export|install|package|relink|recover|"
                    r"files?\b|profile$|presets?\.", re.I)
RECIPE_ALLOWED = {"file.new", "object.pattern.saveCopy", "select.save", "select.editSaved"}
PATHLIKE = re.compile(r"^(/|~|[A-Za-z]:|file:)|(^|[\\/])\.\.([\\/]|$)")
PREFS_ENV = {"VECTORCRAFT_NO_PREFS": "1"}    # replays ignore the user's preferences (units, compression, fonts folder)


def cli_path():
    """VECTORCRAFT_CLI, else vectorcraft-cli on PATH, else ~/.local/bin/vectorcraft-cli; None if absent."""
    env = os.environ.get("VECTORCRAFT_CLI")
    if env:
        return env if shutil.which(env) or os.access(env, os.X_OK) else None
    found = shutil.which("vectorcraft-cli")
    if found:
        return found
    home = pathlib.Path.home() / ".local/bin/vectorcraft-cli"
    return str(home) if os.access(home, os.X_OK) else None


def cli_version(cli):
    r = subprocess.run([cli, "--version"], capture_output=True, text=True, timeout=30)
    m = re.search(r"(\d+\.\d+\.\d+\S*)", r.stdout)
    return m.group(1) if r.returncode == 0 and m else None


def compat(version):
    if version is None:
        return "UNAVAILABLE"
    if version in INCOMPATIBLE_CLI:
        return "INCOMPATIBLE"
    return "SUPPORTED" if version in VALIDATED_CLI else "UNTESTED"


def app_version():
    """Desktop app version (macOS bundle) or None: informational only, the CLI does the work."""
    plist = pathlib.Path("/Applications/VectorCraft.app/Contents/Info.plist")
    if not plist.exists():
        return None
    m = re.search(r"<key>CFBundleShortVersionString</key>\s*<string>([^<]+)</string>", plist.read_text("utf-8", "replace"))
    return m.group(1) if m else None


def environment(cli):
    return {"cli": "vectorcraft-cli", "cli_version": cli_version(cli) if cli else None, "app_version": app_version(),
            "os": f"{platform.system()} {platform.release()}", "arch": platform.machine(),
            "python": platform.python_version()}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def redact(text):
    """Hide the home folder in anything printed or stored."""
    return str(text).replace(str(pathlib.Path.home()), "~")


def safe_rel(rel):
    """A path the manifest may name: relative, no '..', no drive or scheme. Returns it or raises."""
    if not isinstance(rel, str) or not rel or PATHLIKE.search(rel) or "\\" in rel or "\0" in rel:
        raise ValueError(f"unsafe path {rel!r}: must be relative to the delivery folder, without '..'")
    return rel


def inside(base, rel):
    p = (pathlib.Path(base) / safe_rel(rel)).resolve()
    if not p.is_relative_to(pathlib.Path(base).resolve()):
        raise ValueError(f"{rel!r} leaves the delivery folder")
    return p


def walk_strings(v):
    if isinstance(v, str):
        yield v
    elif isinstance(v, dict):
        for x in v.values():
            yield from walk_strings(x)
    elif isinstance(v, list):
        for x in v:
            yield from walk_strings(x)


def validate_steps(steps, opened=False):
    """Errors for a `vectorcraft-cli run --commands` recipe (JSON array of {id|command, params}).
    opened=True: the run starts from `--in FILE`, so the recipe starts with the reset, not file.new."""
    errs = []
    if not isinstance(steps, list) or not steps:
        return ["recipe must be a non-empty JSON array"]
    for i, s in enumerate(steps):
        if not isinstance(s, dict):
            errs.append(f"step {i}: not an object"); continue
        if "id" in s and "command" in s:
            errs.append(f"step {i}: give id or command, not both (the CLI refuses it)"); continue
        cid = s.get("id", s.get("command"))
        if not isinstance(cid, str) or not cid:
            errs.append(f"step {i}: missing id"); continue
        extra = set(s) - {"id", "command", "params"}
        if extra:
            errs.append(f"step {i}: unknown keys {sorted(extra)}")
        if "params" in s and not isinstance(s["params"], dict):
            errs.append(f"step {i} ({cid}): params must be an object")
        if cid not in RECIPE_ALLOWED and DENIED.search(cid):
            errs.append(f"step {i} ({cid}): commands that touch files, preferences or run other commands are not allowed in a recipe")
        for v in walk_strings(s.get("params", {})):
            if PATHLIKE.search(v) and not v.startswith("$"):
                errs.append(f"step {i} ({cid}): path-like value {v!r} (recipes carry no paths)")
        if not opened and isinstance(s.get("params"), dict):
            # a new document's object ids come from earlier steps; a literal id was copied from some session
            for k in ("id", "ids"):
                vals = s["params"].get(k)
                vals = vals if isinstance(vals, list) else [vals] if k in s["params"] else []
                if any(not (isinstance(x, str) and x.startswith("$")) for x in vals):
                    errs.append(f"step {i} ({cid}): literal {k} {s['params'][k]!r}; use \"$N.id\" references to earlier steps")
    ids = [s.get("id", s.get("command")) if isinstance(s, dict) else None for s in steps]
    if opened:
        if ids[:2] != ["select.none", "paint.default"]:
            errs.append("a recipe run on --in must start with select.none, paint.default (reset inherited paint, M31)")
    elif ids[:1] != ["file.new"]:
        errs.append("step 0 must be file.new (explicit document setup)")
    elif ids[1:3] != ["select.none", "paint.default"]:
        errs.append("steps 1-2 must be select.none, paint.default (reset inherited paint, M31)")
    return errs


def validate_manifest(m):
    if not isinstance(m, dict):
        return ["manifest must be a JSON object"]
    errs = []
    req = {"schema": str, "plugin": dict, "skill": dict, "environment": dict, "source_date_epoch": int,
           "recipe": dict, "run": dict, "derived": list, "inputs": list, "outputs": list, "fonts": list,
           "font_strategy": str, "external_resources": list, "dependencies": dict, "determinism": dict,
           "reproduction": dict}
    for k, t in req.items():
        if k not in m:
            errs.append(f"missing {k}")
        elif not isinstance(m[k], t):
            errs.append(f"{k} must be {t.__name__}")
    if errs:
        return errs
    if isinstance(m["source_date_epoch"], bool) or m["source_date_epoch"] < 0:
        errs.append("source_date_epoch must be an integer >= 0")
    if not isinstance(m["run"].get("exports"), list) or not m["run"]["exports"]:
        return errs + ["run.exports must be a non-empty list"]
    for sect in ("inputs", "outputs", "derived", "fonts"):
        if any(not isinstance(e, dict) for e in m[sect]):
            return errs + [f"{sect} entries must be objects"]
    if not re.fullmatch(r"[0-9a-f]{64}", str(m["recipe"].get("sha256"))):
        errs.append("recipe.sha256 must be 64 hex digits")
    if m["recipe"].get("format", STEPS_SCHEMA) != STEPS_SCHEMA:
        errs.append(f"recipe.format must be {STEPS_SCHEMA}")
    for f in m["fonts"]:
        if f.get("status") not in ("exact", "substitute", "missing"):
            errs.append(f"font {f.get('family')}: status must be exact|substitute|missing")
    produced = [*m["run"]["exports"], *[d.get("to") for d in m["derived"]]]
    listed = [o.get("path") for o in m["outputs"]]
    if sorted(map(str, produced)) != sorted(map(str, listed)):
        errs.append(f"outputs {listed} must be exactly the exports + derived files {produced}")
    if m["schema"] != MANIFEST_SCHEMA:
        errs.append(f"schema {m['schema']!r} is not {MANIFEST_SCHEMA}")
    if m["font_strategy"] not in ("none", "editable", "outlined", "both"):
        errs.append("font_strategy must be none|editable|outlined|both")
    if m["reproduction"].get("status") not in STATUSES:
        errs.append(f"reproduction.status must be one of {STATUSES}")
    for sect in ("inputs", "outputs"):
        for e in m[sect]:
            try:
                safe_rel(e.get("path"))
            except ValueError as x:
                errs.append(f"{sect}: {x}")
            if not re.fullmatch(r"[0-9a-f]{64}", str(e.get("sha256"))):
                errs.append(f"{sect}: {e.get('path')}: bad sha256")
    for k in ("path",):
        try:
            safe_rel(m["recipe"].get(k))
        except ValueError as x:
            errs.append(f"recipe: {x}")
    for e in m["run"].get("exports", []):
        try:
            safe_rel(e)
        except ValueError as x:
            errs.append(f"run.exports: {x}")
    if m["run"].get("in") is not None:
        try:
            safe_rel(m["run"]["in"])
        except ValueError as x:
            errs.append(f"run.in: {x}")
    sc = m["run"].get("scale")
    if sc is not None and not isinstance(sc, (int, float)):
        errs.append("run.scale must be a number or null")
    for d in m["derived"]:
        if set(d) - {"from", "to", "options"}:
            errs.append(f"derived: unknown keys {sorted(set(d) - {'from', 'to', 'options'})}")
        if set(d.get("options", {})) - set(CONVERT_OPTIONS):
            errs.append(f"derived: options limited to {sorted(CONVERT_OPTIONS)}")
        for k in ("from", "to"):
            try:
                safe_rel(d.get(k))
            except ValueError as x:
                errs.append(f"derived.{k}: {x}")
    return errs


STATUSES = ["REPRODUCED_BINARY", "REPRODUCED_VISUAL", "REPRODUCED_STRUCTURAL", "FAILED", "UNVERIFIED"]
# derived files are made by `vectorcraft-cli convert FROM TO <flags>`; only these flags exist in a manifest
CONVERT_OPTIONS = {"outline_text": ("--outline-text", bool), "scale": ("--scale", (int, float)),
                   "artboard": ("--artboard", int), "decimals": ("--decimals", int)}


def run_recipe(cli, workdir, steps_rel, exports, scale=None, in_rel=None, epoch=0, derived=()):
    """Run the recipe inside workdir (paths relative to it). Returns (ok, log). No shell anywhere."""
    for rel in list(exports) + [d["to"] for d in derived]:
        inside(workdir, rel).parent.mkdir(parents=True, exist_ok=True)   # export does not create folders
    env = dict(os.environ, SOURCE_DATE_EPOCH=str(epoch), **PREFS_ENV)
    args = [cli, "run"] + (["--in", safe_rel(in_rel)] if in_rel else []) + ["--commands", safe_rel(steps_rel)]
    for rel in exports:
        args += ["--export", safe_rel(rel)]
    if scale is not None:
        args += ["--scale", str(scale)]
    log = []
    r = subprocess.run(args, cwd=workdir, env=env, capture_output=True, text=True, timeout=600)
    log.append(redact((r.stdout[-4000:] + r.stderr[-4000:]).strip()))
    if r.returncode:
        return False, log
    for d in derived:
        a = [cli, "convert", safe_rel(d["from"]), safe_rel(d["to"])]
        for k, v in sorted(d.get("options", {}).items()):
            flag, typ = CONVERT_OPTIONS[k]
            if not isinstance(v, typ):
                return False, log + [f"derived option {k}: bad value {v!r}"]
            if typ is bool:
                a += [flag] if v else []
            else:
                a += [flag, str(v)]
        r = subprocess.run(a, cwd=workdir, env=env, capture_output=True, text=True, timeout=600)
        log.append(redact((r.stdout[-2000:] + r.stderr[-2000:]).strip()))
        if r.returncode:
            return False, log
    return True, log


def cli_json(cli, args, cwd=None):
    r = subprocess.run([cli] + args, cwd=cwd, capture_output=True, text=True, timeout=300, env=dict(os.environ, **PREFS_ENV))
    if r.returncode:
        raise RuntimeError(redact(r.stderr.strip() or r.stdout.strip()))
    return r.stdout


def info(cli, path, cwd=None):
    return json.loads(cli_json(cli, ["info", str(path)], cwd))


def structure(cli, path, cwd=None):
    """Comparable structural summary: artboards, kinds, fonts, one line per node (vc_tree format) and the
    SHA-256 of the file re-exported as SVG by the same CLI (SVG export carries no dates and holds every
    path's geometry, paint, dash, opacity and text, so two files with the same artwork give the same bytes)."""
    import tempfile
    sys.path.insert(0, str(HERE))
    from vc_tree import tree
    out = cli_json(cli, ["run", "--in", str(path), "--cmd", "document.inspect"], cwd)
    doc = [json.loads(l) for l in out.splitlines() if l.startswith("{")][-1]["result"]
    i = info(cli, path, cwd)
    with tempfile.TemporaryDirectory() as t:
        svg = pathlib.Path(t) / "s.svg"
        r = subprocess.run([cli, "convert", str(pathlib.Path(cwd or ".") / path), str(svg)], capture_output=True,
                           text=True, timeout=300, env=dict(os.environ, SOURCE_DATE_EPOCH="0", **PREFS_ENV))
        if r.returncode:
            raise RuntimeError(redact(r.stderr.strip()))
        art = sha256(svg)
    return {"artboards": [[a["x"], a["y"], a["width"], a["height"]] for a in doc["artboards"]],
            "kinds": i.get("kinds"),
            "fonts": sorted((f["family"], f["style"], f["status"]) for f in i.get("fonts", [])),
            "tree": list(tree(doc["layers"], None)), "artwork_svg_sha256": art}


def png_pixels(path):
    """(width, height, rows of RGBA bytes) for 8-bit RGB/RGBA non-interlaced PNG, else None."""
    data = open(path, "rb").read()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    pos, idat, hdr = 8, b"", None
    while pos < len(data):
        n, typ = struct.unpack(">I4s", data[pos:pos + 8])
        body = data[pos + 8:pos + 8 + n]
        if typ == b"IHDR":
            hdr = struct.unpack(">IIBBBBB", body)
        elif typ == b"IDAT":
            idat += body
        pos += 12 + n
    w, h, depth, ctype, _, _, interlace = hdr
    if depth != 8 or ctype not in (2, 6) or interlace:
        return None
    bpp = 4 if ctype == 6 else 3
    raw, stride, rows, prev = zlib.decompress(idat), w * bpp, [], bytearray(w * bpp)
    for y in range(h):
        f, line = raw[y * (stride + 1)], bytearray(raw[y * (stride + 1) + 1:(y + 1) * (stride + 1)])
        for x in range(stride):
            a = line[x - bpp] if x >= bpp else 0
            b, c = prev[x], prev[x - bpp] if x >= bpp else 0
            if f == 1: line[x] = (line[x] + a) & 255
            elif f == 2: line[x] = (line[x] + b) & 255
            elif f == 3: line[x] = (line[x] + (a + b) // 2) & 255
            elif f == 4:
                p = a + b - c; pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                line[x] = (line[x] + (a if pa <= pb and pa <= pc else b if pb <= pc else c)) & 255
        prev = line                      # the next row's filters read this row in its own layout
        rows.append(line if bpp == 4 else bytearray(v for i in range(w) for v in (*line[i * 3:i * 3 + 3], 255)))
    return w, h, rows


# VISUAL equivalence: same size and no channel of any pixel differs by more than MAX_DIFF (of 255).
# No fraction of pixels may be ignored. Documented in references/reproducibility.md.
MAX_DIFF = 2


def png_equivalent(a, b):
    pa, pb = png_pixels(a), png_pixels(b)
    if pa is None or pb is None:
        return None, "unsupported PNG (needs 8-bit RGB/RGBA, non-interlaced)"
    if pa[:2] != pb[:2]:
        return False, f"size {pa[:2]} vs {pb[:2]}"
    worst, over = 0, 0
    for ra, rb in zip(pa[2], pb[2]):
        d = [abs(x - y) for x, y in zip(ra, rb)]
        worst = max(worst, max(d, default=0))
        over += sum(1 for i in range(0, len(d), 4) if max(d[i:i + 4]) > MAX_DIFF)
    return over == 0, f"max channel diff {worst}/255, {over} pixel(s) over {MAX_DIFF}"


def selftest():
    assert compat("0.15.0") == "SUPPORTED" and compat("0.16.0") == "SUPPORTED" and compat("9.9.9") == "UNTESTED" and compat(None) == "UNAVAILABLE"
    for bad in ("/etc/x", "../x", "a/../b", "~/x", "C:\\x", "file:///x", ""):
        try:
            safe_rel(bad); raise AssertionError(bad)
        except ValueError:
            pass
    assert safe_rel("outputs/a b/ícone.svg") == "outputs/a b/ícone.svg"
    good = [{"id": "file.new", "params": {"width": 24}}, {"id": "select.none"}, {"id": "paint.default"},
            {"id": "path.create", "params": {"d": "M1 1 L2 2"}}, {"command": "object.group", "params": {"ids": ["$3.id"]}}]
    assert validate_steps(good) == [], validate_steps(good)
    bad = [{"id": "path.create"}, {"id": "file.save", "params": {"path": "/tmp/x"}}, {"id": "x", "foo": 1}]
    e = validate_steps(bad)
    assert any("file.new" in x for x in e) and any("not allowed" in x for x in e) and any("path-like" in x for x in e) \
        and any("unknown keys" in x for x in e), e
    assert any("M31" in x for x in validate_steps([{"id": "file.new"}, {"id": "path.create"}]))
    head = [{"id": "file.new"}, {"id": "select.none"}, {"id": "paint.default"}]
    for cid in ("action.batch", "file.print", "file.saveAs", "file.list", "document.open", "dataset.import",
                "color.loadProfile", "text.addFontFiles", "swatch.library.save", "graphicStyle.saveLibrary",
                "file.newPresets.save", "file.recovery.save", "command.batch", "clipboard.importSvg", "prefs.set"):
        assert any("not allowed" in x for x in validate_steps(head + [{"id": cid}])), cid
    for cid in ("path.create", "object.group", "paint.setFill", "recolor.apply", "imageTrace.makeAndExpand",
                "object.pattern.saveCopy", "text.create", "swatch.new"):
        assert validate_steps(head + [{"id": cid}]) == [], cid
    assert any("not both" in x for x in validate_steps(head + [{"id": "a.b", "command": "a.b"}]))
    assert any("literal id" in x for x in validate_steps(head + [{"id": "object.setProps", "params": {"id": 7}}]))
    assert any("literal ids" in x for x in validate_steps(head + [{"id": "object.group", "params": {"ids": ["$3.id", 4]}}]))
    assert validate_steps([{"id": "select.none"}, {"id": "paint.default"}, {"id": "object.setProps", "params": {"id": 2}}], opened=True) == []
    try:
        safe_rel("C:foo"); raise AssertionError("C:foo")
    except ValueError:
        pass
    m = {"schema": MANIFEST_SCHEMA, "plugin": {}, "skill": {}, "environment": {}, "source_date_epoch": True,
         "recipe": {"path": "steps.json", "sha256": "x"}, "run": {"exports": ["outputs/a.svg"]}, "derived": [],
         "inputs": [], "outputs": [{"path": "steps.json", "sha256": "0" * 64}], "fonts": [{"family": "F", "status": "?"}],
         "font_strategy": "none", "external_resources": [], "dependencies": {}, "determinism": {}, "reproduction": {"status": "UNVERIFIED"}}
    e = " | ".join(validate_manifest(m))
    for want in ("source_date_epoch", "recipe.sha256", "status must be", "exactly the exports"):
        assert want in e, (want, e)
    assert validate_manifest({**m, "run": {}}) and validate_manifest({**m, "inputs": ["x"]}) and validate_manifest([])
    assert validate_steps([{"id": "select.none"}, {"id": "paint.default"}, {"id": "select.all"}], opened=True) == []
    assert any("--in" in x for x in validate_steps([{"id": "select.all"}], opened=True))
    # PNG round trip through a tiny encoder (filter 0 and 1 rows)
    import tempfile
    def png(rows, w, h):
        raw = b"".join(bytes([f]) + bytes(r) for f, r in rows)
        ch = lambda t, b: struct.pack(">I", len(b)) + t + b + struct.pack(">I", zlib.crc32(t + b) & 0xffffffff)
        return b"\x89PNG\r\n\x1a\n" + ch(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0)) + ch(b"IDAT", zlib.compress(raw)) + ch(b"IEND", b"")
    with tempfile.TemporaryDirectory() as d:
        a, b, c = (os.path.join(d, n) for n in "abc")
        open(a, "wb").write(png([(0, [10, 20, 30, 255, 10, 20, 30, 255]), (1, [10, 20, 30, 255, 0, 0, 0, 0])], 2, 2))
        open(b, "wb").write(png([(0, [10, 20, 30, 255, 10, 20, 30, 255]), (0, [10, 20, 30, 255, 10, 20, 30, 255])], 2, 2))
        open(c, "wb").write(png([(0, [10, 20, 30, 255, 10, 20, 30, 255]), (0, [10, 20, 30, 255, 99, 20, 30, 255])], 2, 2))
        assert png_pixels(a)[2] == png_pixels(b)[2], (png_pixels(a), png_pixels(b))
        assert png_equivalent(a, b)[0] is True and png_equivalent(a, c)[0] is False, png_equivalent(a, c)
        assert sha256(a) != sha256(b)          # same pixels, different bytes: binary differs, visual holds
    print("selftest ok")


if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        selftest()
    elif sys.argv[1:] == ["--denied"]:
        ids = (SKILL_DIR / "references/data/command-ids-0.15.0.txt").read_text().split()
        print("\n".join(i for i in ids if i not in RECIPE_ALLOWED and DENIED.search(i)))
    else:
        sys.exit(__doc__)

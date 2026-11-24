#!/usr/bin/env python3
"""Build a reproducible delivery: run a recipe with vectorcraft-cli, hash everything, write manifest.json.

Usage:
  vc_manifest.py STEPS.json --out NEW_DIR --export outputs/NAME.EXT [--export ...] [--scale N]
                 [--in INPUT_FILE] [--epoch SECONDS] [--outline-svg FROM=TO] [--no-replay]
Self-test: vc_manifest.py --selftest

NEW_DIR must not exist (nothing is ever overwritten). It receives steps.json, inputs/<name> (copy of
--in), the exports, README.md and manifest.json. --outline-svg outputs/a.vectorcraft=outputs/a-outlined.svg
adds an outlined-text SVG made by `vectorcraft-cli convert --outline-text` (font_strategy "both").
Then the delivery is replayed in a temporary folder (vc_replay.py) and manifest.reproduction records
the measured result, never an assumed one. Exit 0 only for REPRODUCED_BINARY.
"""
import argparse, datetime, json, pathlib, shutil, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import vc_common as C
import vc_replay
from vc_links import external, read as read_text

DEFAULT_EPOCH = 946684800          # 2000-01-01T00:00:00Z: fixed so PNG/PDF/EPS/AI/.vectorcraft dates do not vary
VECTOR_INFO = (".vectorcraft", ".pdf", ".ai", ".eps", ".svg")
# Measured on CLI 0.15.0, macOS arm64 (tests/run_regression.py, references/reproducibility.md)
BINARY_VERIFIED = ["vectorcraft", "svg", "pdf", "png", "eps", "ai"]


def build(steps_file, out, exports, scale=None, in_file=None, epoch=DEFAULT_EPOCH, outline=(), replay=True, cli=None):
    cli = cli or C.cli_path()
    if not cli:
        raise SystemExit("vectorcraft-cli not found: run vc_preflight.py")
    steps = json.loads(pathlib.Path(steps_file).read_text("utf-8"))
    errs = C.validate_steps(steps, opened=bool(in_file))
    if errs:
        raise SystemExit("recipe rejected:\n  " + "\n  ".join(errs))
    out = pathlib.Path(out)
    if out.exists():
        raise SystemExit(f"{out} exists: choose a new folder (deliveries are never overwritten)")
    for rel in exports:
        C.safe_rel(rel)
    derived = []
    for spec in outline:
        src, _, dst = spec.partition("=")
        derived.append({"from": C.safe_rel(src), "to": C.safe_rel(dst), "options": {"outline_text": True}})
    out.mkdir(parents=True)
    (out / "steps.json").write_text(json.dumps(steps, indent=1, ensure_ascii=False) + "\n", "utf-8")
    inputs, in_rel, ext_refs = [], None, []
    if in_file:
        in_rel = "inputs/" + pathlib.Path(in_file).name
        (out / "inputs").mkdir()
        shutil.copy2(in_file, C.inside(out, in_rel))
        inputs.append({"path": in_rel, "sha256": C.sha256(C.inside(out, in_rel)), "bytes": C.inside(out, in_rel).stat().st_size})
        if in_rel.lower().endswith((".svg", ".svgz")):
            ext_refs = [{"in": in_rel, "ref": C.redact(r)} for r in external(read_text(C.inside(out, in_rel)))]
    ok, log = C.run_recipe(cli, out, "steps.json", exports, scale, in_rel, epoch, derived)
    if not ok:
        raise SystemExit("recipe failed:\n" + "\n".join(log))
    outputs = []
    for rel in list(exports) + [d["to"] for d in derived]:
        p = C.inside(out, rel)
        outputs.append({"path": rel, "sha256": C.sha256(p), "bytes": p.stat().st_size,
                        "format": p.suffix.lstrip(".").lower()})
    fonts = []
    src = next((C.inside(out, r) for r in exports if r.lower().endswith(VECTOR_INFO)), None)
    if src:
        for f in C.info(cli, src.name, cwd=src.parent).get("fonts", []):
            fonts.append({"family": f["family"], "style": f["style"], "status": f["status"],
                          "resolved": f.get("resolved"), "file": None, "file_sha256": None})
    has_text = bool(fonts)
    strategy = "none" if not has_text else "both" if derived else "editable"
    env = C.environment(cli)
    m = {
        "schema": C.MANIFEST_SCHEMA,
        "plugin": {"name": "vectorcraft", "version": C.PLUGIN_VERSION},
        "skill": {"name": "vectorcraft-design", "version": C.SKILL_VERSION},
        "created": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "environment": env,
        "source_date_epoch": epoch,
        "recipe": {"path": "steps.json", "sha256": C.sha256(out / "steps.json"), "steps": len(steps),
                   "format": C.STEPS_SCHEMA},
        "run": {"in": in_rel, "exports": list(exports), "scale": scale},
        "derived": derived,
        "inputs": inputs,
        "outputs": outputs,
        "fonts": fonts,
        "font_strategy": strategy,
        "external_resources": ext_refs,
        "dependencies": {"vectorcraft-cli": env["cli_version"], "python": ">=3.9",
                         "fonts": sorted({f["family"] for f in fonts})},
        "determinism": {
            "binary_verified_formats": BINARY_VERIFIED,
            "conditions": ["same vectorcraft-cli version", "same SOURCE_DATE_EPOCH (this manifest)",
                           "same input bytes", "same installed font files for live text (PDF/AI/EPS embed them)",
                           "any folder: outputs do not record the delivery path"],
            "notes": ["file.new + select.none + paint.default reset inherited paint (M31)",
                      "font file paths and hashes are not exposed by vectorcraft-cli: file/file_sha256 stay null",
                      "other OS/arch and other CLI versions: not measured"]},
        "reproduction": {"status": "UNVERIFIED", "checked": None, "by": "vc_replay.py"},
    }
    if any(f["status"] != "exact" for f in fonts):
        m["determinism"]["notes"].append("fonts not exact here: " + ", ".join(
            f"{f['family']} {f['style']} ({f['status']})" for f in fonts if f["status"] != "exact"))
    (out / "manifest.json").write_text(json.dumps(m, indent=1, ensure_ascii=False) + "\n", "utf-8")
    if replay:
        rep = vc_replay.verify(out, cli=cli)
        m["reproduction"] = {"status": rep["status"], "checked": m["created"], "by": "vc_replay.py",
                             "cli_version": rep["cli_version"],
                             "outputs": {o["path"]: o["status"] for o in rep["outputs"]}}
        (out / "manifest.json").write_text(json.dumps(m, indent=1, ensure_ascii=False) + "\n", "utf-8")
    (out / "README.md").write_text(readme(m), "utf-8")
    return m


def readme(m):
    rows = "\n".join(f"| `{o['path']}` | {o['format']} | `{o['sha256'][:16]}…` |" for o in m["outputs"])
    fonts = ", ".join(f"{f['family']} {f['style']} ({f['status']})" for f in m["fonts"]) or "none"
    return f"""# VectorCraft delivery

Made with vectorcraft-cli {m['environment']['cli_version']} on {m['environment']['os']} {m['environment']['arch']}, \
SOURCE_DATE_EPOCH={m['source_date_epoch']}. Reproduction when delivered: **{m['reproduction']['status']}**.

| File | Format | SHA-256 |
|---|---|---|
{rows}

Fonts: {fonts} · strategy: {m['font_strategy']}

Rebuild and verify (needs vectorcraft-cli; nothing here is overwritten):

    python3 -B <skill>/scripts/vc_replay.py .

`steps.json` is a plain `vectorcraft-cli run --commands` recipe; `manifest.json` lists inputs, outputs, hashes,
fonts and the conditions under which the bytes are expected to match.
"""


def selftest():
    import tempfile
    with tempfile.TemporaryDirectory() as t:
        t = pathlib.Path(t)
        fake = t / "fakecli"
        fake.write_text("#!" + sys.executable + "\nimport sys,pathlib,json\na=sys.argv[1:]\n"
                        "if a==['--version']: print('vectorcraft-cli 0.15.0'); sys.exit(0)\n"
                        "if a[0]=='info': print(json.dumps({'fonts':[{'family':'Nope','style':'Regular','status':'missing','resolved':{'family':'Source Sans 3'}}]})); sys.exit(0)\n"
                        "if a[0]=='run':\n"
                        "  for i,x in enumerate(a):\n"
                        "    if x=='--export': pathlib.Path(a[i+1]).write_bytes(a[i+1].encode())\n"
                        "  sys.exit(0)\nsys.exit(1)\n")
        fake.chmod(0o755)
        s = t / "s.json"
        s.write_text(json.dumps([{"id": "file.new"}, {"id": "select.none"}, {"id": "paint.default"}]))
        m = build(s, t / "d", ["outputs/x.svg"], cli=str(fake))
        assert m["reproduction"]["status"] == "REPRODUCED_BINARY", m["reproduction"]
        assert m["fonts"][0]["status"] == "missing" and m["font_strategy"] == "editable"
        assert any("not exact" in n for n in m["determinism"]["notes"])
        assert C.validate_manifest(json.loads((t / "d/manifest.json").read_text())) == []
        assert "Traceback" not in (t / "d/README.md").read_text()
        for bad_out, bad_exports in ((t / "d", ["outputs/y.svg"]), (t / "e", ["../y.svg"])):
            try:
                build(s, bad_out, bad_exports, cli=str(fake)); raise AssertionError((bad_out, bad_exports))
            except (SystemExit, ValueError):
                pass
        s.write_text(json.dumps([{"id": "file.new"}, {"id": "path.create"}]))
        try:
            build(s, t / "f", ["outputs/z.svg"], cli=str(fake)); raise AssertionError("M31 preamble not enforced")
        except SystemExit as e:
            assert "M31" in str(e)
    print("selftest ok")


if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        selftest(); sys.exit(0)
    ap = argparse.ArgumentParser(description="Build a reproducible VectorCraft delivery")
    ap.add_argument("steps"); ap.add_argument("--out", required=True)
    ap.add_argument("--export", action="append", required=True, help="path relative to --out, e.g. outputs/icon.svg")
    ap.add_argument("--scale", type=float); ap.add_argument("--in", dest="in_file")
    ap.add_argument("--epoch", type=int, default=DEFAULT_EPOCH)
    ap.add_argument("--outline-svg", action="append", default=[], metavar="FROM=TO")
    ap.add_argument("--no-replay", action="store_true")
    a = ap.parse_args()
    try:
        m = build(a.steps, a.out, a.export, a.scale if a.scale is None or a.scale % 1 else int(a.scale),
                  a.in_file, a.epoch, a.outline_svg, not a.no_replay)
    except ValueError as e:
        sys.exit(f"vc_manifest: {e}")
    print(f"{a.out}: {len(m['outputs'])} output(s), reproduction {m['reproduction']['status']}")
    for o in m["outputs"]:
        print(f"  {o['sha256'][:16]}  {o['path']}  {m['reproduction'].get('outputs', {}).get(o['path'], '')}")
    sys.exit(0 if m["reproduction"]["status"] == "REPRODUCED_BINARY" else 1)

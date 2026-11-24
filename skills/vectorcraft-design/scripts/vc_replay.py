#!/usr/bin/env python3
"""Replay a delivery (manifest.json + steps.json) with vectorcraft-cli and compare the results.

Usage: vc_replay.py DELIVERY_DIR [--json] [--keep]      Self-test: vc_replay.py --selftest

Read-only on DELIVERY_DIR: the recipe runs in a temporary folder (--keep prints it and leaves it).
Per output, the strongest result that holds:
  REPRODUCED_BINARY      SHA-256 of the replayed file == manifest
  REPRODUCED_VISUAL      PNG only: same size, no channel of any pixel differs by more than 2/255
  REPRODUCED_STRUCTURAL  vector/native formats: same artboards, kinds, fonts, node tree (vc_tree lines) and
                         the same bytes when both files are re-exported to SVG (geometry, paint, dash, opacity)
  FAILED                 none of the above, the recipe failed, or a delivered file/recipe/input was altered
  UNVERIFIED             no vectorcraft-cli, or no comparison possible for that format
Overall = FAILED if any FAILED, else UNVERIFIED if any, else the weakest of BINARY > VISUAL > STRUCTURAL.
Exit codes: 0 BINARY · 10 VISUAL · 11 STRUCTURAL · 1 FAILED · 3 UNVERIFIED · 2 invalid manifest/recipe/usage.
"""
import json, pathlib, shutil, sys, tempfile
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import vc_common as C

EXIT = {"REPRODUCED_BINARY": 0, "REPRODUCED_VISUAL": 10, "REPRODUCED_STRUCTURAL": 11, "FAILED": 1, "UNVERIFIED": 3}
RANK = ["REPRODUCED_BINARY", "REPRODUCED_VISUAL", "REPRODUCED_STRUCTURAL"]
STRUCTURAL_FORMATS = {"vectorcraft", "svg", "svgz", "pdf", "ai", "eps"}


class Invalid(Exception):
    pass


def load(delivery):
    d = pathlib.Path(delivery)
    try:
        m = json.loads((d / "manifest.json").read_text("utf-8"))
    except (OSError, ValueError) as e:
        raise Invalid(f"manifest.json: {e}")
    errs = C.validate_manifest(m)
    if errs:
        raise Invalid("manifest.json: " + "; ".join(errs))
    try:
        steps_path = C.inside(d, m["recipe"]["path"])
        steps = json.loads(steps_path.read_text("utf-8"))
    except (OSError, ValueError) as e:
        raise Invalid(f"recipe: {e}")
    errs = C.validate_steps(steps, opened=m["run"].get("in") is not None)
    if errs:
        raise Invalid("recipe: " + "; ".join(errs))
    return d, m, steps_path


def overall(statuses):
    if not statuses:
        return "UNVERIFIED"
    if "FAILED" in statuses:
        return "FAILED"
    if "UNVERIFIED" in statuses:
        return "UNVERIFIED"
    return max(statuses, key=RANK.index)


def verify(delivery, keep=False, cli=None):
    d, m, steps_path = load(delivery)
    rep = {"delivery": C.redact(d.resolve()), "manifest_cli": m["environment"].get("cli_version"),
           "integrity": [], "outputs": [], "log": []}
    # 1. integrity of what was delivered: recipe, inputs, outputs
    if C.sha256(steps_path) != m["recipe"].get("sha256"):
        rep["integrity"].append({"path": m["recipe"]["path"], "problem": "recipe changed since the manifest was written"})
    for sect in ("inputs", "outputs"):
        for e in m[sect]:
            p = C.inside(d, e["path"])
            if not p.is_file():
                rep["integrity"].append({"path": e["path"], "problem": "missing"})
            elif C.sha256(p) != e["sha256"]:
                rep["integrity"].append({"path": e["path"], "problem": "sha256 differs from manifest (file or manifest modified)"})
    cli = cli or C.cli_path()
    rep["cli_version"] = C.cli_version(cli) if cli else None
    rep["compatibility"] = C.compat(rep["cli_version"])
    if rep["cli_version"] and rep["cli_version"] != rep["manifest_cli"]:
        rep["log"].append(f"CLI {rep['cli_version']} != manifest {rep['manifest_cli']}: binary equality is not expected")
    if not cli:
        rep["log"].append("vectorcraft-cli not found: nothing replayed")
        rep["status"] = "FAILED" if rep["integrity"] else "UNVERIFIED"
        return rep
    # 2. replay in a clean temporary folder
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="vc-replay-"))
    try:
        dst = C.inside(tmp, m["recipe"]["path"]); dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(steps_path, dst)
        for e in m["inputs"]:
            dst = C.inside(tmp, e["path"]); dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(C.inside(d, e["path"]), dst)
        ok, log = C.run_recipe(cli, tmp, m["recipe"]["path"], m["run"]["exports"], m["run"].get("scale"),
                               m["run"].get("in"), m["source_date_epoch"], m["derived"])
        rep["log"] += log
        if not ok:
            rep["status"] = "FAILED"
            rep["outputs"] = [{"path": e["path"], "status": "FAILED", "detail": "recipe did not run"} for e in m["outputs"]]
            return rep
        delivered_ok = {e["path"] for e in m["outputs"]} - {i["path"] for i in rep["integrity"]}
        for e in m["outputs"]:
            new = C.inside(tmp, e["path"])
            r = {"path": e["path"], "expected": e["sha256"]}
            if not new.is_file():
                r.update(status="FAILED", detail="not produced by the replay")
            else:
                r["observed"] = C.sha256(new)
                fmt = new.suffix.lstrip(".").lower()      # from the file name, never from the manifest
                if r["observed"] == e["sha256"]:
                    r["status"] = "REPRODUCED_BINARY"
                elif e["path"] not in delivered_ok:
                    r.update(status="FAILED", detail="hash differs and the delivered copy is not intact to compare with")
                elif fmt == "png":
                    same, why = C.png_equivalent(C.inside(d, e["path"]), new)
                    r.update(status="UNVERIFIED" if same is None else "REPRODUCED_VISUAL" if same else "FAILED", detail=why)
                elif fmt in STRUCTURAL_FORMATS:
                    try:
                        a, b = C.structure(cli, C.inside(d, e["path"])), C.structure(cli, new)
                        diff = [k for k in a if a[k] != b[k]]
                        r.update(status="FAILED" if diff else "REPRODUCED_STRUCTURAL",
                                 detail=f"differs in {diff}" if diff else "same artboards, kinds, fonts, tree and re-exported SVG artwork")
                    except RuntimeError as x:
                        r.update(status="UNVERIFIED", detail=f"could not read: {x}")
                else:
                    r.update(status="FAILED", detail=f"hash differs; no structural/visual comparison for {fmt}")
            rep["outputs"].append(r)
    finally:
        if keep:
            rep["workdir"] = C.redact(tmp)
        else:
            shutil.rmtree(tmp, ignore_errors=True)
    st = overall([o["status"] for o in rep["outputs"]])
    rep["status"] = "FAILED" if rep["integrity"] else st
    return rep


def selftest():
    import os, subprocess
    with tempfile.TemporaryDirectory() as t:
        t = pathlib.Path(t)
        # fake CLI: `run ... --export X` writes the bytes "<X>" so hashes are predictable; --version prints 0.15.0
        fake = t / "fakecli"
        fake.write_text("#!" + sys.executable + "\nimport sys,pathlib\na=sys.argv[1:]\n"
                        "if a==['--version']: print('vectorcraft-cli 0.15.0'); sys.exit(0)\n"
                        "if a and a[0]=='run':\n"
                        "  for i,x in enumerate(a):\n"
                        "    if x=='--export': pathlib.Path(a[i+1]).write_bytes(a[i+1].encode())\n"
                        "  sys.exit(0)\nsys.exit(1)\n")
        fake.chmod(0o755)
        d = t / "delivery"; (d / "outputs").mkdir(parents=True)
        steps = [{"id": "file.new", "params": {}}, {"id": "select.none"}, {"id": "paint.default"}]
        (d / "steps.json").write_text(json.dumps(steps))
        (d / "outputs/a.bin").write_bytes(b"outputs/a.bin")
        h = C.sha256(d / "outputs/a.bin")
        m = {"schema": C.MANIFEST_SCHEMA, "plugin": {}, "skill": {}, "environment": {"cli_version": "0.15.0"},
             "source_date_epoch": 1, "recipe": {"path": "steps.json", "sha256": C.sha256(d / "steps.json")},
             "run": {"in": None, "exports": ["outputs/a.bin"], "scale": None}, "derived": [], "inputs": [],
             "outputs": [{"path": "outputs/a.bin", "sha256": h, "format": "bin"}], "fonts": [], "font_strategy": "none",
             "external_resources": [], "dependencies": {}, "determinism": {}, "reproduction": {"status": "UNVERIFIED"}}
        (d / "manifest.json").write_text(json.dumps(m))
        assert verify(d, cli=str(fake))["status"] == "REPRODUCED_BINARY"
        # G: a modified delivered output is reported even though the replay itself matches
        (d / "outputs/a.bin").write_bytes(b"tampered")
        r = verify(d, cli=str(fake))
        assert r["status"] == "FAILED" and r["integrity"][0]["path"] == "outputs/a.bin", r
        (d / "outputs/a.bin").write_bytes(b"outputs/a.bin")
        # a replay producing other bytes, for a format with no deeper comparison -> FAILED
        m2 = dict(m, outputs=[{"path": "outputs/a.bin", "sha256": "0" * 64, "format": "bin"}])
        (d / "manifest.json").write_text(json.dumps(m2))
        assert verify(d, cli=str(fake))["status"] == "FAILED"
        # recipe edited after the manifest -> FAILED (integrity)
        (d / "manifest.json").write_text(json.dumps(m))
        (d / "steps.json").write_text(json.dumps(steps + [{"id": "paint.default"}]))
        assert any("recipe changed" in i["problem"] for i in verify(d, cli=str(fake))["integrity"])
        (d / "steps.json").write_text(json.dumps(steps))
        # no CLI -> UNVERIFIED, never a success
        os.environ["VECTORCRAFT_CLI"] = str(t / "none")
        try:
            assert verify(d)["status"] == "UNVERIFIED"
        finally:
            del os.environ["VECTORCRAFT_CLI"]
        # hostile manifests are rejected before anything runs
        for bad in ({"outputs": [{"path": "../x", "sha256": h}]}, {"run": {"in": "/etc/passwd", "exports": []}},
                    {"outputs": [{"path": "steps.json", "sha256": h}]}, {"run": {}}, {"inputs": ["x"]},
                    {"derived": [{"from": "a", "to": "b", "options": {"shell": "rm -rf /"}}]}, {"schema": "other/9"}):
            (d / "manifest.json").write_text(json.dumps({**m, **bad}))
            try:
                load(d); raise AssertionError(bad)
            except Invalid:
                pass
        (d / "manifest.json").write_text(json.dumps(m))
        (d / "steps.json").write_text(json.dumps(steps + [{"id": "file.save", "params": {"path": "/tmp/x"}}]))
        try:
            load(d); raise AssertionError("file.save accepted")
        except Invalid:
            pass
        r = subprocess.run([sys.executable, "-B", __file__, str(t / "nowhere")], capture_output=True, text=True)
        assert r.returncode == 2 and "Traceback" not in r.stderr, r.stderr
    assert overall(["REPRODUCED_BINARY", "REPRODUCED_STRUCTURAL"]) == "REPRODUCED_STRUCTURAL"
    assert overall(["REPRODUCED_BINARY", "UNVERIFIED"]) == "UNVERIFIED" and overall([]) == "UNVERIFIED"
    print("selftest ok")


def main(argv):
    if argv == ["--selftest"]:
        selftest(); return 0
    args = [a for a in argv if not a.startswith("--")]
    if len(args) != 1:
        print(__doc__, file=sys.stderr); return 2
    try:
        rep = verify(args[0], keep="--keep" in argv)
    except (Invalid, ValueError, KeyError, TypeError, AttributeError) as e:
        print(f"vc_replay: invalid delivery: {type(e).__name__}: {C.redact(e)}", file=sys.stderr); return 2
    if "--json" in argv:
        print(json.dumps(rep, indent=1, ensure_ascii=False))
    else:
        print(f"{rep['status']}  (CLI {rep['cli_version']} [{rep['compatibility']}], manifest {rep['manifest_cli']})")
        for i in rep["integrity"]:
            print(f"  INTEGRITY {i['path']}: {i['problem']}")
        for o in rep["outputs"]:
            print(f"  {o['status']:<22} {o['path']}" + (f"  ({o['detail']})" if o.get("detail") else ""))
        for l in rep["log"]:
            if l.startswith("CLI ") or "not found" in l:
                print(f"  note: {l}")
        if rep.get("workdir"):
            print(f"  replay kept in {rep['workdir']}")
    return EXIT[rep["status"]]


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

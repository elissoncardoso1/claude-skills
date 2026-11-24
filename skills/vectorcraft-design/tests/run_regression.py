#!/usr/bin/env python3
"""Regression suite for the vectorcraft-design skill (stdlib only).

Usage: run_regression.py [--suite unit|cli|mcp|all] [--case ID]... [--report FILE.json] [--update-golden]
  unit  every script's --selftest + schema/validator agreement (no VectorCraft needed)
  cli   tests/scenarios/*.json with suite "cli": deliveries built and replayed with vectorcraft-cli
  mcp   suite "mcp": a private headless MCP server (`vectorcraft-cli mcp` confined to a temp folder)
Scenarios with suite "manual" are listed as NOT_AUTOMATED with the reason; they are never passed.
Golden hashes live in tests/golden/<cli version>/<ID>.json. A version without golden files gets
PASS_NO_BASELINE (expectations met, bytes not compared) and its kinds are compared with 0.15.0:
that is the version matrix. --update-golden writes the current hashes (review the diff first).
Exit 1 if any result is FAIL, else 0.
"""
import argparse, json, os, pathlib, shutil, subprocess, sys, tempfile, time
HERE = pathlib.Path(__file__).resolve().parent
SKILL = HERE.parent
sys.path.insert(0, str(SKILL / "scripts"))
import vc_common as C
import vc_manifest, vc_replay

SELFTESTS = ["vc_common", "vc_check", "vc_links", "vc_tree", "tokens_to_steps", "vc_replay", "vc_manifest", "vc_preflight"]
REFERENCE_GOLDEN = "0.15.0"


def py(script, *args, env=None):
    return subprocess.run([sys.executable, "-B", str(SKILL / "scripts" / script), *args], capture_output=True,
                          text=True, env=dict(os.environ, **(env or {})), timeout=600)


# ---------------------------------------------------------------- unit
def unit():
    res = []
    for s in SELFTESTS:
        t = time.time()
        r = py(f"{s}.py", "--selftest")
        ok = r.returncode == 0 and "selftest ok" in r.stdout
        res.append({"id": f"unit:{s}", "suite": "unit", "status": "PASS" if ok else "FAIL",
                    "detail": "" if ok else (r.stdout + r.stderr)[-800:], "seconds": round(time.time() - t, 2)})
    schema = json.loads((SKILL / "schemas/manifest.schema.json").read_text())
    probe = C.validate_manifest({})
    code_req = sorted(e.split(" ", 1)[1] for e in probe if e.startswith("missing "))
    same = code_req == sorted(schema["required"])
    res.append({"id": "unit:schema-agreement", "suite": "unit", "status": "PASS" if same else "FAIL",
                "detail": "" if same else f"schema {sorted(schema['required'])} vs code {code_req}"})
    return res


# ---------------------------------------------------------------- cli helpers
def recipe_file(sc, tmp):
    r = sc["recipe"]
    if "tokens" in r:
        out = tmp / "steps.json"
        p = py("tokens_to_steps.py", str(SKILL / r["tokens"]))
        if p.returncode:
            raise AssertionError(p.stderr)
        out.write_text(p.stdout)
        return out
    return SKILL / r["steps"]


def delivery(sc, cli, tmp):
    steps = recipe_file(sc, tmp)
    d = tmp / "delivery"
    m = vc_manifest.build(steps, d, sc["exports"], sc.get("scale"), SKILL / sc["in"] if sc.get("in") else None,
                          outline=sc.get("outline", []), cli=cli)
    e, fails = sc.get("expect", {}), []
    if e.get("reproduction") and m["reproduction"]["status"] != e["reproduction"]:
        fails.append(f"reproduction {m['reproduction']['status']} != {e['reproduction']}")
    first = next(o["path"] for o in m["outputs"] if o["format"] in ("vectorcraft", "pdf", "svg"))
    kinds = C.info(cli, C.inside(d, first)).get("kinds", {})
    if "kinds" in e and kinds != e["kinds"]:
        fails.append(f"kinds {kinds} != {e['kinds']}")
    for k, n in e.get("kinds_min", {}).items():
        if kinds.get(k, 0) < n:
            fails.append(f"kinds {k}={kinds.get(k, 0)} < {n}")
    for k in e.get("kinds_absent", []):
        if k in kinds:
            fails.append(f"unexpected kind {k}")
    for f in e.get("fonts", []):
        if not any(x["family"] == f["family"] and x["status"] == f["status"] for x in m["fonts"]):
            fails.append(f"font {f} not in manifest {m['fonts']}")
    if "font_strategy" in e and m["font_strategy"] != e["font_strategy"]:
        fails.append(f"font_strategy {m['font_strategy']} != {e['font_strategy']}")
    if "vc_check" in e:
        args, code = e["vc_check"]
        r = py("vc_check.py", str(C.inside(d, args[0])), *args[1:])
        if r.returncode != code:
            fails.append(f"vc_check exit {r.returncode} != {code}: {r.stdout[-300:]}")
    for rel, text in e.get("contains", []):
        if text not in C.inside(d, rel).read_text("utf-8", "replace"):
            fails.append(f"{rel} lacks {text!r}")
    for rel, text in e.get("absent", []):
        if text in C.inside(d, rel).read_text("utf-8", "replace"):
            fails.append(f"{rel} contains {text!r}")
    again = vc_replay.verify(d, cli=cli)          # second clean replay (test A: twice, clean folders)
    if again["status"] != m["reproduction"]["status"]:
        fails.append(f"second replay {again['status']} != first {m['reproduction']['status']}")
    return fails, {"outputs": {o["path"]: o["sha256"] for o in m["outputs"]}, "kinds": kinds}


# ---------------------------------------------------------------- custom checks
def s04_diagnose(cli, tmp):
    r = py("vc_check.py", str(SKILL / "tests/fixtures/badge-messy.svg"), "--json")
    out = json.loads(r.stdout)
    need = ["outside artboards", "font Comic Neue Fantasy"]
    return [f"vc_check missed {n!r}: {out['problems']}" for n in need if not any(n in p for p in out["problems"])] + \
           ([] if r.returncode == 1 else [f"exit {r.returncode} != 1"]), None


def s08_ids(cli, tmp):
    steps = tmp / "s.json"
    steps.write_text(json.dumps([{"id": "file.new", "params": {"width": 100, "height": 100}}, {"id": "select.none"},
                                 {"id": "paint.default"}, {"id": "path.create", "params": {"d": "M10 10 L90 90"}}]))
    def run(*a):
        r = subprocess.run([cli, "run", *a], cwd=tmp, capture_output=True, text=True, timeout=120)
        if r.returncode:
            raise AssertionError(r.stderr)
        return [json.loads(l) for l in r.stdout.splitlines() if l.startswith("{")]
    run("--commands", "s.json", "--export", "a.vectorcraft")
    found = run("--in", "a.vectorcraft", "--cmd", "document.find", "--params", '{"kind":"Path"}')[-1]["result"]
    pid = found[0]["id"] if isinstance(found, list) else found["matches"][0]["id"] if "matches" in found else found["ids"][0]
    run("--in", "a.vectorcraft", "--cmd", "object.setProps", "--params", json.dumps({"id": pid, "name": "renamed"}),
        "--export", "b.vectorcraft")
    again = run("--in", "b.vectorcraft", "--cmd", "document.find", "--params", '{"name":"renamed"}')[-1]["result"]
    ids = [x["id"] for x in again] if isinstance(again, list) else [x["id"] for x in again.get("matches", again.get("nodes", []))]
    return ([] if ids == [pid] else [f"find by name gave {again}, expected id {pid}"]), None


def s09_unknown(cli, tmp):
    r = subprocess.run([cli, "run", "--cmd", "effect.neonGlow"], cwd=tmp, capture_output=True, text=True, timeout=60)
    fails = [] if r.returncode == 1 and "step 0" in r.stderr else [f"exit {r.returncode}, stderr {r.stderr[-200:]}"]
    ids = [c["id"] for c in json.loads(C.cli_json(cli, ["commands"]))]
    effects = C.cli_json(cli, ["run", "--cmd", "effect.list"])
    if "artistic.neonGlow" not in effects:
        fails.append("artistic.neonGlow not in effect.list (discovery path of S9)")
    if "effect.apply" not in ids:
        fails.append("effect.apply missing from the catalogue")
    return fails, None


def s10_unsupported(cli, tmp):
    shutil.copy(SKILL / "tests/fixtures/fake.sketch", tmp / "fake.sketch")
    r = subprocess.run([cli, "convert", "fake.sketch", "out.svg"], cwd=tmp, capture_output=True, text=True, timeout=60)
    fails = [] if r.returncode != 0 and "not a format VectorCraft reads" in r.stderr else [f"exit {r.returncode}: {r.stderr[-200:]}"]
    if (tmp / "out.svg").exists():
        fails.append("out.svg was written")
    return fails, None


def r01_negative(cli, tmp):
    fails = []
    src = SKILL.parent.parent / "examples/reproducible-delivery"
    if not src.is_dir():
        return ["examples/reproducible-delivery missing"], None
    base = tmp / "base"; shutil.copytree(src, base)
    rep0 = vc_replay.verify(base, cli=cli)
    # byte equality is only promised for the CLI version that made the example; another version may
    # stamp its own version into .vectorcraft/PDF and must then still reproduce the artwork
    same = rep0["cli_version"] == rep0["manifest_cli"]
    ok = rep0["status"] == "REPRODUCED_BINARY" if same else rep0["status"].startswith("REPRODUCED_")
    if not ok:
        fails.append(f"pristine example: {rep0['status']} (CLI {rep0['cli_version']}, made with {rep0['manifest_cli']})")
    t1 = tmp / "t1"; shutil.copytree(src, t1)
    with open(t1 / "outputs/icons.svg", "ab") as f:
        f.write(b" ")
    if vc_replay.verify(t1, cli=cli)["status"] != "FAILED":
        fails.append("tampered output not detected")
    t2 = tmp / "t2"; shutil.copytree(src, t2)
    (t2 / "steps.json").write_text((t2 / "steps.json").read_text().replace("#111827", "#ff0000", 1))
    if vc_replay.verify(t2, cli=cli)["status"] != "FAILED":
        fails.append("edited recipe not detected")
    # a recipe changed consistently (manifest updated) + a new epoch, so integrity passes and bytes differ:
    # the structural comparison must catch the colour change in the .vectorcraft/.pdf and the PNG must differ
    t3 = tmp / "t3"; shutil.copytree(src, t3)
    (t3 / "steps.json").write_text((t3 / "steps.json").read_text().replace("#111827", "#ff0000"))
    m = json.loads((t3 / "manifest.json").read_text())
    m["recipe"]["sha256"] = C.sha256(t3 / "steps.json"); m["source_date_epoch"] += 1
    (t3 / "manifest.json").write_text(json.dumps(m))
    rep = vc_replay.verify(t3, cli=cli)
    by = {o["path"]: o["status"] for o in rep["outputs"]}
    if rep["status"] != "FAILED" or "REPRODUCED_STRUCTURAL" in by.values() or by.get("outputs/icons.png") != "FAILED":
        fails.append(f"real change not detected: {by}")
    # same bounding box, different geometry + dash + opacity, PNG dropped (audit finding): must still FAIL
    t4 = tmp / "t4"; shutil.copytree(src, t4)
    steps = json.loads((t4 / "steps.json").read_text())
    k = next(i for i, s in enumerate(steps) if s["id"] == "path.create" and s["params"]["d"].startswith("M 5 9"))
    steps[k]["params"]["d"] = "M 5 9 L 12 20 L 19 9 L 12 9 L 5 20 L 19 20"     # zigzag inside the same 5..19 x 9..20 box
    steps[k + 3]["params"]["dash"] = [1, 3]
    steps.insert(k + 4, {"id": "object.setProps", "params": {"id": f"${k}.id", "opacity": 20}})
    steps = [{**s, "params": {kk: ([f"${int(v[1:].split('.')[0]) + 1}.id" if isinstance(v, str) and v.startswith("$") and v[1].isdigit() and int(v[1:].split('.')[0]) > k + 3 else v for v in vv]
              if isinstance(vv, list) else vv) for kk, vv in s.get("params", {}).items()}} for s in steps]
    (t4 / "steps.json").write_text(json.dumps(steps))
    m = json.loads((t4 / "manifest.json").read_text())
    m["recipe"]["sha256"] = C.sha256(t4 / "steps.json"); m["source_date_epoch"] += 1
    m["run"]["exports"] = [e for e in m["run"]["exports"] if not e.endswith(".png")]
    m["outputs"] = [o for o in m["outputs"] if not o["path"].endswith(".png")]
    (t4 / "outputs/icons.png").unlink()
    (t4 / "manifest.json").write_text(json.dumps(m))
    rep = vc_replay.verify(t4, cli=cli)
    by4 = {o["path"]: o["status"] for o in rep["outputs"]}
    if rep["status"] != "FAILED" or set(by4.values()) != {"FAILED"}:
        fails.append(f"geometry/dash/opacity change with the same bounds not detected: {by4}")
    return fails, {"colour_change": by, "geometry_change": by4}


def e01_cli(cli, tmp):
    fails = []
    env = {"VECTORCRAFT_CLI": str(tmp / "absent")}
    r = py("vc_preflight.py", "--json", "--no-mcp", env=env)
    j = json.loads(r.stdout)
    if r.returncode != 1 or "UNAVAILABLE" not in json.dumps(j["errors"]):
        fails.append(f"preflight without CLI: exit {r.returncode}")
    src = SKILL.parent.parent / "examples/reproducible-delivery"
    r = py("vc_replay.py", str(src), env=env)
    if r.returncode != 3 or "UNVERIFIED" not in r.stdout:
        fails.append(f"replay without CLI: exit {r.returncode} {r.stdout[:80]}")
    wrap = tmp / "vectorcraft-cli"            # real CLI, but reporting another version
    wrap.write_text(f"#!/bin/sh\nif [ \"$1\" = --version ]; then echo 'vectorcraft-cli 9.9.9'; exit 0; fi\nexec '{cli}' \"$@\"\n")
    wrap.chmod(0o755)
    r = py("vc_preflight.py", "--json", "--no-mcp", env={"VECTORCRAFT_CLI": str(wrap)})
    j = json.loads(r.stdout)
    if r.returncode != 10 or "UNTESTED" not in json.dumps(j["warnings"]):
        fails.append(f"preflight with 9.9.9: exit {r.returncode} {j['status']}")
    r = py("vc_replay.py", str(src), env={"VECTORCRAFT_CLI": str(wrap)})
    if "9.9.9" not in r.stdout or "UNTESTED" not in r.stdout:
        fails.append(f"replay did not flag the version: {r.stdout[:200]}")
    return fails, None


# ---------------------------------------------------------------- MCP
class MCP:
    """Minimal stdio client for a private `vectorcraft-cli mcp` confined to one temp folder."""
    def __init__(self, cli, root):
        self.p = subprocess.Popen([cli, "mcp", "--automation-read-root", str(root), "--automation-write-root", str(root)],
                                  stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        self.n = 0
        self.call("initialize", {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "regression", "version": "1"}})
        self.p.stdin.write(json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"}) + "\n"); self.p.stdin.flush()

    def call(self, method, params):
        self.n += 1
        self.p.stdin.write(json.dumps({"jsonrpc": "2.0", "id": self.n, "method": method, "params": params}) + "\n")
        self.p.stdin.flush()
        while True:
            line = self.p.stdout.readline()
            if not line:
                raise AssertionError("MCP server closed the stream")
            r = json.loads(line)
            if r.get("id") == self.n:
                return r

    def tool(self, name, args):
        r = self.call("tools/call", {"name": name, "arguments": args})["result"]
        text = "".join(c.get("text", "") for c in r.get("content", []))
        return r.get("isError", False), text

    def close(self):
        self.p.stdin.close(); self.p.wait(timeout=20)


def m31_leak(cli, tmp):
    s = MCP(cli, tmp)
    try:
        dirty = [{"id": "file.new", "params": {"width": 100, "height": 100}}, {"id": "select.none"},
                 {"id": "paint.setFill", "params": {"color": "#ff0000"}}, {"id": "paint.setStroke", "params": {"color": "#00ff00"}},
                 {"id": "stroke.set", "params": {"weight": 7, "cap": "round", "dash": [3, 1]}},
                 {"id": "file.new", "params": {"width": 100, "height": 100}},
                 {"id": "path.create", "params": {"d": "M10 10 L90 10 L90 90 Z"}},
                 {"id": "document.inspect", "params": {"ids": ["$6.id"]}}]
        err, text = s.tool("command_batch", {"steps": dirty})
        node = json.loads(text)["results"][-1]["result"]["nodes"][0]
        leaked = node["fill"] == "#ff0000" and node["strokeWidth"] == 7
        clean = [{"id": "file.new", "params": {"width": 100, "height": 100}}, {"id": "select.none"}, {"id": "paint.default"},
                 {"id": "path.create", "params": {"d": "M10 10 L90 10 L90 90 Z"}}, {"id": "document.inspect", "params": {"ids": ["$3.id"]}}]
        err2, text2 = s.tool("command_batch", {"steps": clean})
        n2 = json.loads(text2)["results"][-1]["result"]["nodes"][0]
        reset = (n2["fill"], n2["stroke"], n2["strokeWidth"], n2["strokeOptions"]["cap"], n2["strokeOptions"]["dash"]) == \
                ("#ffffff", "#000000", 1.0, "butt", None)
    finally:
        s.close()
    fails = []
    if not leaked:
        fails.append(f"M31 no longer reproduces (good news: update docs): {node['fill']} {node['strokeWidth']}")
    if not reset:
        fails.append(f"preamble did not reset paint: {n2}")
    return fails, {"leak_reproduced": leaked, "preamble_resets": reset}


def s12_headless(cli, tmp):
    s = MCP(cli, tmp)
    try:
        err, text = s.tool("inspect_ui", {})
    finally:
        s.close()
    ok = err and "desktop app" in text and "--control" in text      # names the cause and the way out
    return ([] if ok else [f"inspect_ui in headless: isError={err}, expected a message naming the desktop app and --control: {text[:160]}"]), {"message": text[:200]}


CUSTOM = {f.__name__: f for f in (s04_diagnose, s08_ids, s09_unknown, s10_unsupported, r01_negative, e01_cli, m31_leak, s12_headless)}


def golden_compare(sc_id, version, got, update):
    gdir = HERE / "golden" / (version or "none")
    path = gdir / f"{sc_id}.json"
    if update and version:
        gdir.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(got, indent=1, sort_keys=True) + "\n")
        return [], "golden written"
    if path.exists():
        g = json.loads(path.read_text())
        diff = [p for p in g["outputs"] if g["outputs"][p] != got["outputs"].get(p)]
        diff += ["kinds"] if g["kinds"] != got["kinds"] else []
        return [f"differs from golden {version}: {diff}"] if diff else [], None
    ref = HERE / "golden" / REFERENCE_GOLDEN / f"{sc_id}.json"
    if ref.exists() and json.loads(ref.read_text())["kinds"] != got["kinds"]:
        return [f"kinds differ from {REFERENCE_GOLDEN}: {json.loads(ref.read_text())['kinds']} vs {got['kinds']}"], None
    return [], "NO_BASELINE"


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--suite", default="all", choices=["unit", "cli", "mcp", "all"])
    ap.add_argument("--case", action="append", default=[]); ap.add_argument("--report")
    ap.add_argument("--update-golden", action="store_true")
    a = ap.parse_args(argv)
    cli = C.cli_path()
    version = C.cli_version(cli) if cli else None
    results = []
    if a.suite in ("unit", "all") and not a.case:
        results += unit()
    for f in sorted((HERE / "scenarios").glob("[A-Z]*.json")):
        sc = json.loads(f.read_text())
        if a.case and sc["id"] not in a.case:
            continue
        if a.suite != "all" and sc["suite"] not in (a.suite, "manual"):
            continue
        r = {"id": sc["id"], "suite": sc["suite"], "title": sc["title"], "origin": sc.get("origin")}
        if sc.get("human_review"):
            r["human_review"] = sc["human_review"]
        if sc["kind"] == "manual":
            results.append({**r, "status": "NOT_AUTOMATED", "detail": sc["reason"]}); continue
        if not cli:
            results.append({**r, "status": "SKIPPED", "detail": "vectorcraft-cli not found"}); continue
        t = time.time()
        tmp = pathlib.Path(tempfile.mkdtemp(prefix=f"vc-{sc['id']}-"))
        try:
            if sc["kind"] == "delivery":
                fails, got = delivery(sc, cli, tmp)
                gf, note = golden_compare(sc["id"], version, got, a.update_golden)
                fails += gf
            else:
                fails, got = CUSTOM[sc["check"]](cli, tmp)
                note = None
            status = "FAIL" if fails else "PASS_NO_BASELINE" if note == "NO_BASELINE" else "PASS"
            results.append({**r, "status": status, "detail": "; ".join(fails) or (note or ""), "data": got,
                            "seconds": round(time.time() - t, 2)})
        except Exception as e:                       # a crashing scenario is a failure, reported, not hidden
            results.append({**r, "status": "FAIL", "detail": f"{type(e).__name__}: {C.redact(e)}"})
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    known = {json.loads(f.read_text())["id"] for f in (HERE / "scenarios").glob("[A-Z]*.json")}
    unknown = [c for c in a.case if c not in known]
    if unknown:
        print(f"unknown case(s) {unknown}; known: {sorted(known)}", file=sys.stderr)
        return 2
    counts = {}
    for r in results:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    report = {"plugin": C.PLUGIN_VERSION, "environment": C.environment(cli), "compatibility": C.compat(version),
              "suite": a.suite, "summary": counts, "results": results}
    for r in results:
        print(f"{r['status']:<17} {r['id']:<26} {r.get('title', '')[:70]}" + (f"\n                  -> {r['detail'][:300]}" if r.get("detail") and r["status"] != "PASS" else ""))
    print(f"\nCLI {version} [{C.compat(version)}] · " + " · ".join(f"{k} {v}" for k, v in sorted(counts.items())))
    if a.report:
        pathlib.Path(a.report).write_text(json.dumps(report, indent=1, ensure_ascii=False) + "\n")
    return 1 if counts.get("FAIL") else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

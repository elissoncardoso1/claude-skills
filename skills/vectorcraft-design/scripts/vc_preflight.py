#!/usr/bin/env python3
"""Check everything a VectorCraft workflow needs before it starts. Changes nothing outside a temp folder.

Usage: vc_preflight.py [--json] [--out DIR] [--font FAMILY[:STYLE]]... [--input FILE]... [--no-mcp] [--mcp-name NAME]
Self-test: vc_preflight.py --selftest

Checks: Python >= 3.9 · vectorcraft-cli found, runs, version vs the validated list (SUPPORTED /
UNTESTED / INCOMPATIBLE / UNAVAILABLE) · smoke recipe exports a valid SVG · every engine command the
capability catalogue uses still exists · MCP server: configuration (~/.claude.json user and project
entries, ./.mcp.json), its read/write roots, and a real initialize + tools/list handshake · --out
writable (a temp file is created and removed) · --font installed · --input readable by VectorCraft,
hashed, external references in SVGs · the skill's own scripts and schemas present.
Status: OK (exit 0) · WARN (exit 10: proceed, but read the actions) · FAIL (exit 1: fix first) · usage error (exit 2).
Home folder paths are printed as ~.
"""
import json, os, pathlib, shutil, subprocess, sys, tempfile, time
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import vc_common as C

SMOKE = [{"id": "file.new", "params": {"width": 10, "height": 10}}, {"id": "select.none"}, {"id": "paint.default"},
         {"id": "path.create", "params": {"d": "M1 1 L9 9"}}, {"id": "paint.setStroke", "params": {"color": "#000000"}}]
NEEDED = ["scripts/vc_common.py", "scripts/vc_check.py", "scripts/vc_tree.py", "scripts/vc_links.py",
          "scripts/vc_manifest.py", "scripts/vc_replay.py", "scripts/tokens_to_steps.py",
          "schemas/manifest.schema.json", "schemas/steps.schema.json", "references/data/capabilities-0.15.0.json"]


class Report:
    def __init__(self):
        self.checks, self.actions = [], []

    def add(self, name, status, detail="", action=None):
        self.checks.append({"name": name, "status": status, "detail": C.redact(detail)})
        if action:
            self.actions.append(C.redact(action))

    def status(self):
        s = {c["status"] for c in self.checks}
        return "FAIL" if "FAIL" in s else "WARN" if "WARN" in s else "OK"


def mcp_configs(cwd, files=None):
    """(source, name, entry) for every configured MCP server whose command is vectorcraft-cli."""
    files = files if files is not None else [pathlib.Path.home() / ".claude.json", pathlib.Path(cwd) / ".mcp.json"]
    found = []
    for f in files:
        try:
            data = json.loads(pathlib.Path(f).read_text("utf-8"))
        except (OSError, ValueError):
            continue
        groups = [("user" if f.name == ".claude.json" else "project", data.get("mcpServers") or {})]
        proj = (data.get("projects") or {}).get(str(pathlib.Path(cwd).resolve())) or {}
        groups.append(("local", proj.get("mcpServers") or {}))
        for scope, servers in groups:
            for name, e in servers.items():
                if isinstance(e, dict) and pathlib.Path(str(e.get("command", ""))).name == "vectorcraft-cli":
                    found.append((f"{scope} ({C.redact(f)})", name, e))
    return found


def roots(args):
    out = {"read": [], "write": [], "connect": None}
    for i, a in enumerate(args):
        if a == "--automation-read-root" and i + 1 < len(args): out["read"].append(args[i + 1])
        if a == "--automation-write-root" and i + 1 < len(args): out["write"].append(args[i + 1])
        if a == "--connect" and i + 1 < len(args): out["connect"] = args[i + 1]
    return out


MCP_FLAGS = {"--automation-read-root": 1, "--automation-write-root": 1, "--connect": 1, "--headless": 0}


def trusted_launch(command, args, cli, cwd):
    """(ok, reason). The handshake only ever starts the vectorcraft-cli this preflight already found, as
    `mcp` with known flags. A configured command elsewhere (e.g. a project's ./.mcp.json pointing at its
    own script) is reported, never executed, and the config's env is never applied."""
    if not cli:
        return False, "no trusted vectorcraft-cli to compare with"
    p = pathlib.Path(command).expanduser()
    p = p if p.is_absolute() else pathlib.Path(cwd) / p if "/" in command else pathlib.Path(shutil.which(command) or command)
    if os.path.realpath(p) != os.path.realpath(cli):
        return False, f"configured command {command} is not the vectorcraft-cli found here ({cli}): not executed"
    if not args or args[0] != "mcp":
        return False, "arguments do not start with `mcp`: not executed"
    i = 1
    while i < len(args):
        n = MCP_FLAGS.get(args[i])
        if n is None:
            return False, f"unknown argument {args[i]!r}: not executed"
        i += 1 + n
    return True, ""


def handshake(command, args, env=None, timeout=20):
    """Real MCP exchange: initialize, initialized, tools/list. Returns (ok, detail)."""
    msgs = [{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-06-18",
             "capabilities": {}, "clientInfo": {"name": "vc_preflight", "version": C.PLUGIN_VERSION}}},
            {"jsonrpc": "2.0", "method": "notifications/initialized"},
            {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}]
    try:
        p = subprocess.Popen([command] + list(args), stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                             stderr=subprocess.DEVNULL, text=True, env=dict(os.environ, **(env or {})))
    except OSError as e:
        return False, f"cannot start: {e}"
    try:
        out, _ = p.communicate("".join(json.dumps(m) + "\n" for m in msgs), timeout=timeout)
    except subprocess.TimeoutExpired:
        p.kill(); return False, f"no answer in {timeout}s"
    replies = {}
    for line in out.splitlines():
        try:
            r = json.loads(line)
        except ValueError:
            continue
        if isinstance(r, dict) and "id" in r:
            replies[r["id"]] = r
    tools = (replies.get(2) or {}).get("result", {}).get("tools")
    if not replies.get(1, {}).get("result") or tools is None:
        return False, f"no valid initialize/tools reply (exit {p.returncode})"
    info = replies[1]["result"].get("serverInfo", {})
    return True, f"{info.get('name', '?')} {info.get('version', '?')}: {len(tools)} tools"


def check(out=None, fonts=(), inputs=(), mcp=True, mcp_name=None, cli=None, config_files=None, cwd=None):
    rep, cwd = Report(), cwd or os.getcwd()
    v = sys.version_info
    rep.add("python", "PASS" if v >= (3, 9) else "FAIL", f"{v.major}.{v.minor}.{v.micro}",
            None if v >= (3, 9) else "install Python 3.9 or newer")
    missing = [n for n in NEEDED if not (C.SKILL_DIR / n).is_file()]
    rep.add("skill files", "FAIL" if missing else "PASS", ", ".join(missing) or f"{len(NEEDED)} present",
            "reinstall the plugin" if missing else None)
    cli = cli if cli is not None else C.cli_path()
    versions = {"plugin": C.PLUGIN_VERSION, "skill": C.SKILL_VERSION, "validated_cli": C.VALIDATED_CLI,
                "cli": None, "app": C.app_version()}
    if not cli:
        rep.add("vectorcraft-cli", "FAIL", "UNAVAILABLE: not on PATH, VECTORCRAFT_CLI unset",
                "install vectorcraft-cli (VectorCraft release zip) or set VECTORCRAFT_CLI=/path/to/vectorcraft-cli")
    else:
        ver = C.cli_version(cli)
        versions["cli"] = ver
        comp = C.compat(ver)
        st = {"SUPPORTED": "PASS", "UNTESTED": "WARN"}.get(comp, "FAIL")
        rep.add("cli version", st, f"{ver or 'no version'} -> {comp} (validated: {', '.join(C.VALIDATED_CLI)})",
                None if st == "PASS" else
                f"run `python3 -B {C.redact(C.SKILL_DIR)}/tests/run_regression.py --suite cli` and compare with "
                "tests/golden/0.15.0 before relying on byte-identical replays" if comp == "UNTESTED" else
                "this CLI is unusable here: install a validated version")
        if ver:
            with tempfile.TemporaryDirectory() as t:
                pathlib.Path(t, "s.json").write_text(json.dumps(SMOKE))
                ok, log = C.run_recipe(cli, t, "s.json", ["smoke.svg"], epoch=0)
                svg = pathlib.Path(t, "smoke.svg")
                good = ok and svg.is_file() and b"<svg" in svg.read_bytes()[:400]
                rep.add("cli smoke run", "PASS" if good else "FAIL", "recipe -> SVG" if good else " ".join(log)[-300:],
                        None if good else "vectorcraft-cli cannot run a basic recipe: see the detail")
            try:
                ids = {c["id"] for c in json.loads(C.cli_json(cli, ["commands"]))}
                caps = json.loads((C.SKILL_DIR / "references/data/capabilities-0.15.0.json").read_text())["capabilities"]
                used = {e.split(" ")[0] for c in caps for e in c["engine_commands"]} - {"effect"}
                gone = sorted(u for u in used if not u.startswith("(") and not (
                    u.endswith(".*") and any(i.startswith(u[:-1]) for i in ids)) and not u.endswith(".*") and u not in ids)
                gone += sorted(u for u in used if u.endswith(".*") and not any(i.startswith(u[:-1]) for i in ids))
                snap = set((C.SKILL_DIR / "references/data/command-ids-0.15.0.txt").read_text().split())
                rep.add("command catalogue", "FAIL" if gone else "PASS",
                        f"{len(ids)} commands; capability commands missing: {gone}" if gone else
                        f"{len(ids)} commands ({len(ids - snap)} new, {len(snap - ids)} removed vs 0.15.0 snapshot)",
                        f"capabilities using {gone} are INCOMPATIBLE with this CLI" if gone else None)
            except (RuntimeError, ValueError, KeyError) as e:
                rep.add("command catalogue", "FAIL", f"cannot read: {e}", "check the CLI installation")
    if mcp:
        cfg = [c for c in mcp_configs(cwd, config_files) if not mcp_name or c[1] == mcp_name]
        if not cfg:
            rep.add("mcp config", "WARN", "no vectorcraft-cli MCP server configured",
                    "MCP tools unavailable: use the CLI, or register one, e.g. `claude mcp add vectorcraft -- "
                    "vectorcraft-cli mcp --automation-read-root <DIR> --automation-write-root <DIR>/_vectorcraft-out`")
        for source, name, e in cfg:
            r = roots(e.get("args") or [])
            mode = f"connect {r['connect']}" if r["connect"] else "headless" if r["read"] or r["write"] else "app or headless"
            rep.add(f"mcp config {name}", "PASS", f"{source}: {mode}")
            if not r["read"] and not r["write"] and not r["connect"]:
                rep.add(f"mcp roots {name}", "WARN", "no --automation-*-root: the MCP may read/write any file",
                        "add --automation-read-root/--automation-write-root to confine it (ask the user)")
            for kind in ("read", "write"):
                for d in r[kind]:
                    ok = os.path.isdir(d) and os.access(d, os.R_OK if kind == "read" else os.W_OK)
                    rep.add(f"mcp {kind} root", "PASS" if ok else "FAIL", d,
                            None if ok else f"{kind} root {C.redact(d)} missing or not {'readable' if kind == 'read' else 'writable'}")
            if not r["write"] and (r["read"] or r["connect"]):
                rep.add("mcp write root", "WARN", "none: MCP saves/exports will be rejected",
                        "use the CLI for outputs, or ask the user to add a write root")
            trusted, why = trusted_launch(str(e.get("command", "")), [str(a) for a in e.get("args") or []], cli, cwd)
            if not trusted:
                rep.add(f"mcp handshake {name}", "WARN", why,
                        f"check `claude mcp get {name}`; the preflight only starts the vectorcraft-cli it found itself")
                continue
            ok, detail = handshake(cli, e.get("args") or [])
            rep.add(f"mcp handshake {name}", "PASS" if ok else "FAIL", detail,
                    None if ok else "the configured MCP server does not answer: run `claude mcp get " + name + "`")
    if out:
        o = pathlib.Path(out)
        target = o if o.exists() else o.parent
        try:
            with tempfile.NamedTemporaryFile(dir=target, prefix=".vc-preflight-"):
                pass
            rep.add("output folder", "PASS", f"{o} writable" + ("" if o.exists() else " (will be created)"))
        except OSError as e:
            rep.add("output folder", "FAIL", f"{o}: {e.strerror}", "choose a writable output folder")
    for spec in fonts:
        fam, _, style = spec.partition(":")
        if not cli:
            rep.add(f"font {spec}", "SKIP", "no CLI"); continue
        try:
            got = json.loads([l for l in C.cli_json(cli, ["run", "--cmd", "text.fontList", "--params",
                              json.dumps({"family": fam})]).splitlines() if l.startswith("{")][-1])["result"]
            ok = not style or style in got.get("styles", [])
            rep.add(f"font {spec}", "PASS" if ok else "FAIL", f"styles {got.get('styles')}",
                    None if ok else f"style {style} not installed: pick one of {got.get('styles')}")
        except (RuntimeError, ValueError, KeyError, IndexError):
            rep.add(f"font {spec}", "FAIL", "not installed",
                    f"install {fam}, pick an installed family, or deliver outlined text (references/typography.md)")
    for f in inputs:
        p = pathlib.Path(f)
        if not p.is_file():
            rep.add(f"input {p.name}", "FAIL", f"{p}: not found", "check the path"); continue
        detail = f"sha256 {C.sha256(p)[:16]}…"
        st = "PASS"
        if cli:
            try:
                i = C.info(cli, p)
                bad = [x["family"] for x in i.get("fonts", []) if x["status"] != "exact"]
                detail += f", kinds {i.get('kinds')}" + (f", fonts not exact {bad}" if bad else "")
                st = "WARN" if bad else st
            except (RuntimeError, ValueError) as e:
                rep.add(f"input {p.name}", "FAIL", f"VectorCraft cannot read it: {e}", "convert it or use another file")
                continue
        if p.suffix.lower() in (".svg", ".svgz"):
            from vc_links import external, read
            refs = external(read(p))
            if refs:
                st, detail = "WARN", detail + f", {len(refs)} external reference(s)"
                rep.actions.append(f"{p.name}: run vc_links.py --strip before using the CLI (rules 6, safety.md)")
        rep.add(f"input {p.name}", st, detail)
    return {"status": rep.status(), "versions": versions, "checks": rep.checks,
            "errors": [c for c in rep.checks if c["status"] == "FAIL"],
            "warnings": [c for c in rep.checks if c["status"] == "WARN"], "actions": rep.actions}


EXIT = {"OK": 0, "WARN": 10, "FAIL": 1}


def selftest():
    with tempfile.TemporaryDirectory() as t:
        t = pathlib.Path(t)
        def fake(version, fonts=("Helvetica",), mcp_ok=True):
            p = t / f"cli-{version}-{mcp_ok}"
            p.write_text("#!" + sys.executable + "\nimport sys,json,pathlib\na=sys.argv[1:]\n"
                f"V={version!r}; FONTS={list(fonts)!r}; MCP={mcp_ok!r}\n"
                "if a==['--version']: print('vectorcraft-cli '+V); sys.exit(0)\n"
                "if a==['commands']: print(json.dumps([{'id':i} for i in pathlib.Path(" + repr(str(C.SKILL_DIR / "references/data/command-ids-0.15.0.txt")) + ").read_text().split()])); sys.exit(0)\n"
                "if a[:1]==['info']: print(json.dumps({'kinds':{'Layer':1},'fonts':[]})); sys.exit(0)\n"
                "if a[:1]==['mcp']:\n"
                "  if not MCP: sys.exit(1)\n"
                "  for l in sys.stdin:\n"
                "    m=json.loads(l)\n"
                "    if m.get('id')==1: print(json.dumps({'jsonrpc':'2.0','id':1,'result':{'serverInfo':{'name':'vectorcraft','version':V}}}),flush=True)\n"
                "    if m.get('id')==2: print(json.dumps({'jsonrpc':'2.0','id':2,'result':{'tools':[{'name':'x'}]}}),flush=True)\n"
                "  sys.exit(0)\n"
                "if a[:1]==['run']:\n"
                "  if '--cmd' in a and 'text.fontList' in a:\n"
                "    fam=json.loads(a[a.index('--params')+1])['family']\n"
                "    if fam not in FONTS: sys.stderr.write('unknown family'); sys.exit(1)\n"
                "    print(json.dumps({'result':{'family':fam,'styles':['Regular','Bold']}})); sys.exit(0)\n"
                "  for i,x in enumerate(a):\n"
                "    if x=='--export': pathlib.Path(x and a[i+1]).write_text('<svg/>')\n"
                "  sys.exit(0)\nsys.exit(2)\n")
            p.chmod(0o755); return str(p)
        def cfg(cli_cmd, args):
            f = t / f"cfg{len(list(t.iterdir()))}" / ".claude.json"; f.parent.mkdir()
            f.write_text(json.dumps({"mcpServers": {"vectorcraft": {"command": cli_cmd, "args": args}}})); return [f]
        rw = t / "root"; (rw / "out").mkdir(parents=True)
        good = fake("0.15.0")
        good_cli = t / "g" / "vectorcraft-cli"; good_cli.parent.mkdir(); good_cli.symlink_to(good)
        r = check(cli=str(good_cli), config_files=cfg(str(good_cli), ["mcp", "--automation-read-root", str(rw),
                  "--automation-write-root", str(rw / "out")]), out=str(t / "new"), fonts=["Helvetica:Bold"])
        assert r["status"] == "OK", [c for c in r["checks"] if c["status"] != "PASS"]
        assert any(c["name"].startswith("mcp handshake") and "1 tools" in c["detail"] for c in r["checks"])
        # CLI missing
        r = check(cli=False, mcp=False)
        assert r["status"] == "FAIL" and "UNAVAILABLE" in r["errors"][0]["detail"], r
        # other version -> UNTESTED (warning, with an action), not a failure
        r = check(cli=fake("9.9.9"), mcp=False)
        assert r["status"] == "WARN" and any("UNTESTED" in w["detail"] for w in r["warnings"]) and r["actions"], r
        # missing font, missing input, unwritable folder
        locked = t / "locked"; locked.mkdir(); locked.chmod(0o500)
        r = check(cli=good, mcp=False, fonts=["Nope Sans"], inputs=[str(t / "absent.svg")], out=str(locked))
        names = {c["name"] for c in r["errors"]}
        assert {"font Nope Sans", "input absent.svg", "output folder"} <= names, names
        locked.chmod(0o700)
        # MCP configured but not answering; MCP not configured
        bad = t / "b" / "vectorcraft-cli"; bad.parent.mkdir(); bad.symlink_to(fake("0.15.0", mcp_ok=False))
        r = check(cli=str(bad), config_files=cfg(str(bad), ["mcp", "--automation-read-root", str(rw), "--automation-write-root", str(rw)]))
        assert any(c["name"].startswith("mcp handshake") and c["status"] == "FAIL" for c in r["checks"]), r["checks"]
        # hostile project config: its own "vectorcraft-cli" script and env must never run
        evil = t / "repo" / "bin" / "vectorcraft-cli"; evil.parent.mkdir(parents=True)
        evil.write_text("#!/bin/sh\necho pwned > " + str(t / "PWNED") + "\n"); evil.chmod(0o755)
        (t / "repo" / ".mcp.json").write_text(json.dumps({"mcpServers": {"vc": {"command": "./bin/vectorcraft-cli",
                                               "args": ["mcp"], "env": {"DYLD_INSERT_LIBRARIES": "/x"}}}}))
        r = check(cli=good, cwd=str(t / "repo"), config_files=[t / "repo" / ".mcp.json"])
        assert not (t / "PWNED").exists(), "preflight executed a configured foreign binary"
        assert any("not executed" in c["detail"] for c in r["checks"]), r["checks"]
        for args in (["run", "--commands", "x"], ["mcp", "--evil"]):
            assert trusted_launch(good, args, good, str(t))[0] is False, args
        r = check(cli=good, config_files=[])
        assert r["status"] == "WARN" and r["warnings"][0]["name"] == "mcp config"
        # SVG input with an external reference
        svg = t / "ext.svg"; svg.write_text('<svg><image href="file:///etc/x.png"/></svg>')
        r = check(cli=good, mcp=False, inputs=[str(svg)])
        assert r["status"] == "WARN" and any("vc_links" in a for a in r["actions"])
        assert C.redact(str(pathlib.Path.home() / "x")) == "~/x"
    print("selftest ok")


def main(argv):
    if argv == ["--selftest"]:
        selftest(); return 0
    import argparse
    ap = argparse.ArgumentParser(description="VectorCraft preflight")
    ap.add_argument("--json", action="store_true"); ap.add_argument("--out")
    ap.add_argument("--font", action="append", default=[]); ap.add_argument("--input", action="append", default=[])
    ap.add_argument("--no-mcp", action="store_true"); ap.add_argument("--mcp-name")
    a = ap.parse_args(argv)
    r = check(a.out, a.font, a.input, not a.no_mcp, a.mcp_name)
    if a.json:
        print(json.dumps(r, indent=1, ensure_ascii=False))
    else:
        v = r["versions"]
        print(f"preflight {r['status']}  plugin {v['plugin']} · CLI {v['cli']} (validated {', '.join(v['validated_cli'])}) · app {v['app']}")
        for c in r["checks"]:
            print(f"  {c['status']:<4} {c['name']}: {c['detail']}")
        for x in r["actions"]:
            print(f"  -> {x}")
    return EXIT[r["status"]]


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

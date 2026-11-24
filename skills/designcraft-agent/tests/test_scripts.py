#!/usr/bin/env python3
"""Self-checks for the skill's scripts. Run: python3 tests/test_scripts.py
The live part needs designcraft-cli on PATH; it is skipped (and said so) without it."""
import json, os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.join(HERE, "..", "scripts")
sys.path.insert(0, SCRIPTS)
import dc_check  # noqa: E402


def unit():
    page = {"bounds": [0, 0, 600, 800], "name": "1", "side": "right",
            "margins": {"top": 50, "bottom": 50, "inside": 40, "outside": 30}}
    doc = {"stories": [{"id": 9, "frames": [8], "overset": True, "length": 10},
                       {"id": 11, "frames": [10], "overset": False, "length": 0}],
           "spreads": [{"index": 0, "pages": [page], "items": [
               {"id": 8, "kind": "<text frame>", "bounds": [-10, 0, 100, 100]},
               {"id": 10, "kind": "<text frame>", "bounds": [20, 60, 100, 100]},
               {"id": 12, "kind": "<rectangle>", "bounds": [40, 50, 570, 750]}]}]}
    fonts = [{"family": "Inter", "style": "Bold", "matchStatus": "styleSubstitute", "missing": False,
              "resolvedFamily": "Inter", "resolvedStyle": "SemiBold", "characters": 3}]
    kinds = sorted(i["kind"] for i in dc_check.check(doc, fonts, {"issues": []}, margins=True))
    assert kinds == ["crossesMargin", "emptyText", "fontSubstitute", "overset", "pastPageEdge"], kinds
    # a left page swaps inside/outside: its left margin becomes the 30pt outside one
    page["side"] = "left"
    kinds = [i["kind"] for i in dc_check.check(doc, [], {"issues": []}, margins=True)]
    assert "crossesMargin" in kinds  # item 10 at x=20 < 30
    print("unit: ok")


def live():
    cli = shutil.which("designcraft-cli")
    if not cli:
        print("live: SKIPPED (designcraft-cli not on PATH)")
        return
    d = tempfile.mkdtemp()
    f = os.path.join(d, "o.designcraft")
    step = 'frame.create {"rect":[36,36,80,50],"content":"text","text":"far too much text for this frame"}'
    subprocess.run([cli, "script", "-", "--save", f], input=step, text=True, check=True, capture_output=True)
    r = subprocess.run([sys.executable, os.path.join(SCRIPTS, "dc_check.py"), f], capture_output=True, text=True)
    assert r.returncode == 1 and any(i["kind"] == "overset" for i in json.loads(r.stdout)["issues"]), r.stdout
    calls = os.path.join(d, "calls.json")
    json.dump([{"tool": "new_document", "args": {"preset": "A4"}},
               {"tool": "render_page", "args": {"page": 0, "scale": 0.25}},
               {"tool": "execute", "args": {"command": "no.such", "params": {}}}], open(calls, "w"))
    r = subprocess.run([sys.executable, os.path.join(SCRIPTS, "dc_mcp.py"), calls, "--out", d],
                       capture_output=True, text=True)
    lines = [json.loads(l) for l in r.stdout.splitlines()]
    assert r.returncode == 1 and len(lines) == 3 and lines[2]["isError"], r.stdout + r.stderr
    assert os.path.getsize(lines[1]["images"][0]) > 0
    print("live: ok")


if __name__ == "__main__":
    unit()
    live()

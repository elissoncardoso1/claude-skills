#!/usr/bin/env python3
"""Structural checks of a .designcraft (or .idml) file before you call it done.

usage: dc_check.py FILE [--margins] [--min-ppi N] [--cli PATH]

Runs document.inspect, font.list and preflight.run headlessly (nothing is saved) and reports:
  ERROR  overset story (text that does not fit its frames)
  ERROR  font missing, or style substituted (e.g. Inter Bold drawn as SemiBold)
  WARN   item that extends past the page edges of its spread (fine for bleed art, check it)
  WARN   item that crosses the page margins (only with --margins)
  WARN   empty text frame
  WARN/ERROR  every preflight.run issue, at the severity preflight gives it
Prints a JSON report; exit 0 when there are no ERRORs, 1 otherwise, 2 if the CLI failed.
It does not judge visual quality: render the pages and look at them as well.
"""
import argparse, json, shutil, subprocess, sys


def run_script(cli, path, steps):
    text = "\n".join(f"{c} {json.dumps(p)}" for c, p in steps)
    r = subprocess.run([cli, "script", "-", "--in", path], input=text, capture_output=True, text=True)
    try:
        out = json.loads(r.stdout)
    except ValueError:
        sys.stderr.write(r.stderr or r.stdout)
        sys.exit(2)
    if r.returncode or "error" in out:
        sys.stderr.write(r.stderr or json.dumps(out))
        sys.exit(2)
    return out["results"]


def walk(items):
    for it in items:
        yield it
        yield from walk(it.get("children") or [])


def check(doc, fonts, pre, margins=False):
    issues = []
    add = lambda sev, kind, msg, **k: issues.append({"severity": sev, "kind": kind, "message": msg, **k})
    eps = 0.5
    for st in doc.get("stories", []):
        if st.get("overset"):
            add("error", "overset", f"story {st['id']} overflows its frames {st['frames']}: "
                f"thread another frame, enlarge, or cut text", story=st["id"])
        if st.get("length") == 0:
            add("warn", "emptyText", f"story {st['id']} is empty (frames {st['frames']})", story=st["id"])
    for f in fonts:
        if f.get("missing"):
            add("error", "missingFont", f"font {f['family']} {f['style']} is missing ({f['characters']} chars)")
        elif f.get("matchStatus") != "exact":
            add("error", "fontSubstitute", f"{f['family']} {f['style']} is drawn as "
                f"{f.get('resolvedFamily')} {f.get('resolvedStyle')}: pick an available style")
    for sp in doc.get("spreads", []):
        pages = sp.get("pages", [])
        if not pages:
            continue
        x0 = min(p["bounds"][0] for p in pages); y0 = min(p["bounds"][1] for p in pages)
        x1 = max(p["bounds"][2] for p in pages); y1 = max(p["bounds"][3] for p in pages)
        for it in sp.get("items", []):  # top-level only: a group's bounds cover its children
            b = it.get("bounds")
            if not b or it.get("hidden"):
                continue
            if b[0] < x0 - eps or b[1] < y0 - eps or b[2] > x1 + eps or b[3] > y1 + eps:
                add("warn", "pastPageEdge", f"item {it['id']} {it['kind']} {b} extends past the page "
                    f"edges of spread {sp['index']}", item=it["id"], spread=sp["index"])
            elif margins:
                for p in pages:
                    pb, m = p["bounds"], p.get("margins", {})
                    if b[2] <= pb[0] or b[0] >= pb[2]:
                        continue  # not on this page
                    # inside is the spine side: right of a left page, left of any other page
                    left, right = m.get("inside", 0), m.get("outside", 0)
                    if p.get("side") == "left":
                        left, right = right, left
                    if (b[0] < pb[0] + left - eps or b[2] > pb[2] - right + eps or
                            b[1] < pb[1] + m.get("top", 0) - eps or b[3] > pb[3] - m.get("bottom", 0) + eps):
                        add("warn", "crossesMargin", f"item {it['id']} {it['kind']} {b} crosses the margins "
                            f"of page {p['name']}", item=it["id"], page=p["name"])
    for i in pre.get("issues", []):
        add("error" if i.get("severity") == "error" else "warn", "preflight:" + i.get("kind", "?"),
            i.get("message", ""), **{k: i[k] for k in ("item", "page") if k in i})
    return issues


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--margins", action="store_true", help="also warn about items crossing page margins")
    ap.add_argument("--min-ppi", type=float, default=150)
    ap.add_argument("--cli", default=shutil.which("designcraft-cli") or "designcraft-cli")
    a = ap.parse_args()
    doc, fonts, pre = run_script(a.cli, a.file, [("document.inspect", {}), ("font.list", {}),
                                                 ("preflight.run", {"minPpi": a.min_ppi})])
    issues = check(doc, fonts, pre, a.margins)
    errors = sum(i["severity"] == "error" for i in issues)
    print(json.dumps({"file": a.file, "pages": doc.get("pageCount"), "errors": errors,
                      "warnings": len(issues) - errors, "issues": issues}, indent=1, ensure_ascii=False))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Run FilmCraft MCP tool calls in ONE session (ids stay valid between calls).

Usage:
  fc_mcp.py [--cli PATH] [--project P.fcproj | --demo | --bridge 127.0.0.1:PORT] [--list] CALLS.json|-
(--bridge drives the running app; FILMCRAFT_CONTROL_TOKEN must be in the environment.)
CALLS is a JSON array of {"tool": name, "args": {...}}. Each result is printed as one
JSON line {"i", "tool", "isError", "result"}; image results are saved next to the
calls file as mcp_<i>.png and reported by path. Exit 1 if any call errored.
A string arg value "$<i>.<key>[.<key|index>...]" is replaced by that part of call i's
JSON result (e.g. "$0.sequence", "$1.items", "$1.items.0", "$3.placed.0.0"), so later
calls can use ids returned earlier. A reference that cannot be resolved (for example
because call i failed) stops the run there, before sending anything else.
"""
import base64, json, os, shutil, subprocess, sys

def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        print(__doc__); return 0 if a else 2
    cli =shutil.which("filmcraft-cli") or os.path.expanduser("~/.local/bin/filmcraft-cli")
    server_args, listing, src = [], False, None
    while a:
        x = a.pop(0)
        if x == "--cli": cli = a.pop(0)
        elif x == "--project": server_args += ["--project", a.pop(0)]
        elif x == "--demo": server_args.append("--demo")
        elif x == "--bridge": server_args += ["--bridge", a.pop(0)]
        elif x == "--list": listing = True
        else: src = x
    calls = [] if listing else json.load(sys.stdin if src in (None, "-") else open(src))
    outdir = os.path.dirname(os.path.abspath(src)) if src not in (None, "-") else os.getcwd()
    p = subprocess.Popen([cli, "mcp", *server_args], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    n = 0
    def rpc(method, params=None, notify=False):
        nonlocal n
        msg = {"jsonrpc": "2.0", "method": method, "params": params or {}}
        if not notify:
            n += 1; msg["id"] = n
        p.stdin.write(json.dumps(msg) + "\n"); p.stdin.flush()
        if notify: return None
        while True:
            line = p.stdout.readline()
            if not line: raise SystemExit("server closed the connection")
            r = json.loads(line)
            if r.get("id") == n: return r
    rpc("initialize", {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "fc_mcp", "version": "1"}})
    rpc("notifications/initialized", notify=True)
    if listing:
        for t in rpc("tools/list")["result"]["tools"]:
            print(json.dumps({"name": t["name"], "args": sorted(t.get("inputSchema", {}).get("properties", {}))}))
        p.stdin.close(); p.wait(); return 0
    results, failed = [], False
    def subst(v):
        if isinstance(v, str) and v.startswith("$") and "." in v:
            i, *path = v[1:].split(".")
            try:
                cur = results[int(i)]
                for k in path:
                    cur = cur[int(k)] if isinstance(cur, list) else cur[k]
                return cur
            except (IndexError, KeyError, ValueError, TypeError):
                raise LookupError(f"{v}: not found in the result of call {i}: {json.dumps(results[int(i)]) if i.isdigit() and int(i) < len(results) else 'no such call'}")
        if isinstance(v, dict): return {k: subst(x) for k, x in v.items()}
        if isinstance(v, list): return [subst(x) for x in v]
        return v
    for i, c in enumerate(calls):
        try:
            args = subst(c.get("args", {}))
        except LookupError as e:
            print(json.dumps({"i": i, "tool": c["tool"], "isError": True, "result": f"not run: {e}"}))
            failed = True
            break
        r = rpc("tools/call", {"name": c["tool"], "arguments": args})
        if "error" in r:
            out, err = r["error"], True
        else:
            res = r["result"]; err = bool(res.get("isError")); out = []
            for part in res.get("content", []):
                if part.get("type") == "image":
                    path = os.path.join(outdir, f"mcp_{i}.png")
                    open(path, "wb").write(base64.b64decode(part["data"])); out.append({"image": path})
                elif part.get("type") == "text":
                    try: out.append(json.loads(part["text"]))
                    except ValueError: out.append(part["text"])
            out = out[0] if len(out) == 1 else out
        results.append(out if isinstance(out, dict) else {"value": out})
        failed |= err
        print(json.dumps({"i": i, "tool": c["tool"], "isError": err, "result": out}))
    p.stdin.close(); p.wait()
    return 1 if failed else 0

if __name__ == "__main__":
    sys.exit(main())

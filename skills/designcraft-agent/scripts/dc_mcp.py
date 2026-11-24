#!/usr/bin/env python3
"""Drive `designcraft-cli mcp` over stdio without registering it in an MCP client.

usage: dc_mcp.py CALLS.json [--out DIR] [--cli PATH] [-- EXTRA MCP ARGS...]
       dc_mcp.py --tools            # print tool names + input keys and exit

CALLS.json is a JSON array of calls, each {"tool": NAME, "args": {...}}.
Image results (render_page, screenshot) are written to DIR/call-<n>.png.
Prints one JSON line per call: {"n", "tool", "isError", "text", "images"}.
Stops at the first tool error unless --keep-going. Exit status 1 if any call failed.
Extra args after `--` go to `designcraft-cli mcp` (e.g. `--connect 7979`,
`--sample`, `--automation-write-root DIR`).
"""
import argparse, base64, json, os, shutil, subprocess, sys


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("calls", nargs="?")
    ap.add_argument("--out", default=".")
    ap.add_argument("--cli", default=shutil.which("designcraft-cli") or "designcraft-cli")
    ap.add_argument("--tools", action="store_true")
    ap.add_argument("--keep-going", action="store_true")
    argv = sys.argv[1:]
    extra = argv[argv.index("--") + 1:] if "--" in argv else []
    a = ap.parse_args(argv[:argv.index("--")] if "--" in argv else argv)
    if not a.tools and not a.calls:
        ap.error("CALLS.json required (or --tools)")
    calls = [] if a.tools else json.load(open(a.calls))
    if not isinstance(calls, list):
        ap.error("CALLS.json must be a JSON array of {tool, args}")
    os.makedirs(a.out, exist_ok=True)

    p = subprocess.Popen([a.cli, "mcp", *extra], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, text=True, bufsize=1)

    def rpc(i, method, params=None):
        p.stdin.write(json.dumps({"jsonrpc": "2.0", "id": i, "method": method, "params": params or {}}) + "\n")
        p.stdin.flush()
        line = p.stdout.readline()
        if not line:
            sys.exit("designcraft-cli mcp exited: " + p.stderr.read().strip())
        return json.loads(line)

    init = rpc(0, "initialize", {"protocolVersion": "2025-06-18", "capabilities": {},
                                 "clientInfo": {"name": "dc_mcp.py", "version": "1"}})
    if "error" in init:
        sys.exit("initialize failed: " + json.dumps(init["error"]))
    p.stdin.write(json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"}) + "\n")

    if a.tools:
        for t in rpc(1, "tools/list")["result"]["tools"]:
            print(t["name"], sorted(t["inputSchema"].get("properties", {})))
        p.stdin.close(); p.wait(); return 0

    failed = False
    for n, c in enumerate(calls):
        m = rpc(n + 1, "tools/call", {"name": c["tool"], "arguments": c.get("args", {})})
        rec = {"n": n, "tool": c["tool"]}
        if "error" in m:  # protocol error, e.g. -32602 unknown argument
            rec.update(isError=True, text=f"JSON-RPC {m['error'].get('code')}: {m['error'].get('message')}")
        else:
            r = m["result"]
            rec["isError"] = bool(r.get("isError"))
            texts, imgs = [], []
            for k, part in enumerate(r.get("content", [])):
                if part.get("type") == "text":
                    texts.append(part["text"])
                elif part.get("type") == "image":
                    path = os.path.join(a.out, f"call-{n}" + (f"-{k}" if k else "") + ".png")
                    open(path, "wb").write(base64.b64decode(part["data"]))
                    imgs.append(path)
            rec.update(text="\n".join(texts), images=imgs)
        print(json.dumps(rec, ensure_ascii=False), flush=True)
        if rec["isError"]:
            failed = True
            if not a.keep_going:
                break
    p.stdin.close()
    p.wait(timeout=30)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

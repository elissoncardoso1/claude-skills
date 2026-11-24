#!/bin/bash
# FilmCraft environment check. Run it; don't read it. Exit 0 = ready (warnings allowed), 1 = blocking problem.
# Usage: bash doctor.sh [--bridge 127.0.0.1:PORT]
CLI="${FILMCRAFT_CLI:-$(command -v filmcraft-cli || echo "$HOME/.local/bin/filmcraft-cli")}"
fail=0; ok(){ echo "OK    $*"; }; warn(){ echo "WARN  $*"; }; bad(){ echo "FAIL  $*"; fail=1; }

[ -x "$CLI" ] && ok "cli: $CLI" || { bad "filmcraft-cli not found or not executable ($CLI). Set FILMCRAFT_CLI or install to ~/.local/bin"; exit 1; }
v=$("$CLI" --version 2>&1); rc=$?
[ $rc -eq 0 ] && ok "version: $v" || { bad "'$CLI --version' failed (exit $rc: $v). On macOS a binary copied over an old one in place can be killed (137): rm it, copy again"; exit 1; }
case "$v" in *" 0.19."*) ;; *) warn "this skill was verified on 0.19.0; got '$v' — re-check behaviour with 'commands'/'describe'";; esac
command -v filmcraft-cli >/dev/null || warn "filmcraft-cli is not on PATH (use the full path above)"

n=$("$CLI" commands --json --compact 2>/dev/null | python3 -c 'import json,sys;print(len(json.load(sys.stdin)))' 2>/dev/null)
[ -n "$n" ] && ok "engine catalog: $n commands" || bad "'commands --json' failed"

mcp_check(){ python3 - "$CLI" "$@" <<'PY'
import json,subprocess,sys
p=subprocess.Popen([sys.argv[1],"mcp",*sys.argv[2:]],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
def rpc(i,m,pa={}):
    p.stdin.write(json.dumps({"jsonrpc":"2.0","id":i,"method":m,"params":pa})+"\n"); p.stdin.flush()
    while True:
        l=p.stdout.readline()
        if not l: raise SystemExit("server closed: "+p.stderr.read().strip()[:200])
        r=json.loads(l)
        if r.get("id")==i: return r
init=rpc(0,"initialize",{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"doctor","version":"1"}})
p.stdin.write('{"jsonrpc":"2.0","method":"notifications/initialized"}\n'); p.stdin.flush()
tools=[t["name"] for t in rpc(1,"tools/list")["result"]["tools"]]
extra=""
if "--bridge" in sys.argv:
    r=rpc(2,"tools/call",{"name":"ui_inspect","arguments":{}})["result"]
    extra=" | ui_inspect: "+("ERROR "+r["content"][0]["text"][:120] if r.get("isError") else "ok")
print(f'{init["result"]["serverInfo"]["name"]} {init["result"]["serverInfo"]["version"]}, {len(tools)} tools{extra}')
p.stdin.close(); p.wait()
PY
}
out=$(mcp_check 2>&1) && ok "mcp (headless) starts: $out" || bad "mcp did not start: $out"

d="${FILMCRAFT_DATA_DIR:-$HOME/Library/Application Support/FilmCraft}"
[ -d "$d" ] && { [ -w "$d" ] && ok "data dir writable: $d" || warn "data dir not writable: $d"; } || warn "data dir absent (created on first use): $d"
t=$(mktemp -d 2>/dev/null) && [ -w "$t" ] && { ok "temp dir writable: $t"; rmdir "$t"; } || bad "cannot create a temp dir"
APP=/Applications/FilmCraft.app/Contents/MacOS/FilmCraft
if [ -x "$APP" ]; then av=$("$APP" --version 2>/dev/null | awk '{print $2}'); ok "app: FilmCraft $av"
  [ "$av" = "${v##* }" ] || warn "app $av != cli ${v##* }: bridge was verified CLI 0.19.0 -> app 0.20.1; other pairs untested"
else warn "FilmCraft.app not found (bridge mode unavailable; headless works)"; fi
command -v ffprobe >/dev/null && ok "ffprobe available for output checks" || warn "ffprobe missing: verify exports with 'filmcraft-cli probe <file>' instead"

if [ "$1" = "--bridge" ]; then
  addr="$2"
  [ ${#FILMCRAFT_CONTROL_TOKEN} -eq 64 ] && ok "FILMCRAFT_CONTROL_TOKEN set (64 chars)" || bad "FILMCRAFT_CONTROL_TOKEN must be 64 hex chars, same value given to the app"
  nc -z "${addr%:*}" "${addr#*:}" 2>/dev/null && ok "control port $addr listening" || bad "nothing listening on $addr (start: FILMCRAFT_CONTROL_TOKEN=… /Applications/FilmCraft.app/Contents/MacOS/FilmCraft --control ${addr#*:})"
  [ $fail -eq 0 ] && { out=$(mcp_check --bridge "$addr" 2>&1) && ok "mcp (bridge): $out" || bad "mcp bridge: $out"; }
fi
exit $fail

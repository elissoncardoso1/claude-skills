#!/usr/bin/env bash
# Start the FilmCraft desktop app with its control channel, wait until it answers,
# run ONE command with FILMCRAFT_CONTROL_TOKEN in its environment, then quit the app.
#
#   fc_bridge_session.sh [--port 9876] [--data-dir DIR] [--keep] [--app PATH] -- COMMAND...
#
# The token is generated here and only passed through the environment (never argv,
# never written to disk). --keep leaves the app running (you then lose the token, so
# only use it when a person will take over the window). Exit status = COMMAND's.
set -euo pipefail
PORT=9876; DATA=""; KEEP=0
APP="${FILMCRAFT_APP:-/Applications/FilmCraft.app/Contents/MacOS/FilmCraft}"
while [ $# -gt 0 ]; do
  case "$1" in
    --port) PORT="$2"; shift 2 ;;
    --data-dir) DATA="$2"; shift 2 ;;
    --keep) KEEP=1; shift ;;
    --app) APP="$2"; shift 2 ;;
    --) shift; break ;;
    *) echo "unknown option $1" >&2; exit 2 ;;
  esac
done
[ $# -gt 0 ] || { echo "usage: $0 [options] -- COMMAND..." >&2; exit 2; }
export FILMCRAFT_CONTROL_TOKEN="$(python3 -c 'import secrets; print(secrets.token_hex(32))')"
args=(--control "$PORT" --empty --no-recover)
[ -n "$DATA" ] && { mkdir -p "$DATA"; args+=(--data-dir "$DATA"); }
"$APP" "${args[@]}" >/dev/null 2>&1 &
# Ready = a request succeeds (the port opens before the app accepts requests:
# early replies are "FilmCraft is still starting; send the request again").
python3 - "$PORT" <<'PY'
import json, os, socket, sys, time
port = int(sys.argv[1]); deadline = time.time() + 60
while time.time() < deadline:
    try:
        s = socket.create_connection(("127.0.0.1", port), timeout=5); f = s.makefile("rw")
        f.write(json.dumps({"id": 1, "token": os.environ["FILMCRAFT_CONTROL_TOKEN"], "method": "ui.inspect"}) + "\n"); f.flush()
        if json.loads(f.readline() or "{}").get("ok"): sys.exit(0)
    except OSError:
        pass
    time.sleep(0.5)
sys.exit("FilmCraft did not become ready on port %d within 60 s" % port)
PY
set +e; "$@"; rc=$?; set -e
if [ "$KEEP" = 0 ]; then
  python3 - "$PORT" <<'PY'
import json, os, socket, sys
try:
    s = socket.create_connection(("127.0.0.1", int(sys.argv[1])), timeout=5); f = s.makefile("rw")
    f.write(json.dumps({"id": 1, "token": os.environ["FILMCRAFT_CONTROL_TOKEN"], "method": "app.quit", "params": {}}) + "\n"); f.flush(); f.readline()
except OSError:
    pass
PY
fi
exit $rc

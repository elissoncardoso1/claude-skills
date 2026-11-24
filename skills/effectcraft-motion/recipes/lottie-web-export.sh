#!/usr/bin/env bash
# Lottie for the web: export a comp to .json and .lottie, list what Lottie can't carry (warnings), and
# render frames in a real player (lottie-web, headless Chrome) to see what a browser will show.
# usage: lottie-web-export.sh PROJECT.ecproj COMP OUT_BASENAME [TEXT_AS_SHAPES=1]
#   TEXT_AS_SHAPES=1 (default): text becomes glyph shapes → no font needed in the browser, but Source
#   Text keys and text animators are baked at time 0. Use 0 for live text (the browser then needs the font).
set -euo pipefail
E=${EFFECTCRAFT_CLI:-effectcraft-cli}
HERE=$(cd "$(dirname "$0")" && pwd)
proj=${1:?project}; comp=${2:?comp}; base=${3:?out basename, e.g. web/lower-third}; tas=${4:-1}
mkdir -p "$(dirname "$base")"
abs=$(cd "$(dirname "$base")" && pwd)/$(basename "$base")
opt=$([[ "$tas" == 1 ]] && echo ',"textAsShapes":true' || echo '')

for ext in json lottie; do
  $E exec file.exportLottie "{\"comp\":\"$comp\",\"path\":\"$abs.$ext\"$opt}" "$proj" --json \
    | python3 -c 'import json,sys;d=json.load(sys.stdin);r=d.get("result",d);print(r["path"],r["bytes"],"bytes");[print("  WARNING:",w) for w in r["warnings"]]'
done
# Frames to check in the browser player: 1/4, 1/2 and 3/4 of the animation.
read -r q1 q2 q3 < <(python3 -c 'import json,sys;d=json.load(open(sys.argv[1]));o=d["op"]-d["ip"];print(int(d["ip"]+o/4),int(d["ip"]+o/2),int(d["ip"]+3*o/4))' "$abs.json")
"$HERE/../scripts/lottie_preview.sh" "$abs.json" "$(dirname "$abs")/lottie-check" "$q1" "$q2" "$q3" | tail -1

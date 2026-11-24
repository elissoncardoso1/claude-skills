#!/usr/bin/env bash
# Render N evenly spaced frames of a comp and (if ImageMagick is present) a contact sheet.
# usage: preview.sh PROJECT.ecproj COMP [N=6] [MAX_SIDE=480] [OUT_DIR=preview]
#   extra times: TIMES="0.25 1.2" preview.sh …   (added to the evenly spaced ones)
# Prints the paths of the frames and of sheet.png. Exit 1 if any frame fails or comes out empty.
set -euo pipefail
proj=${1:?project .ecproj}; comp=${2:?comp name or id}; n=${3:-6}; side=${4:-480}; out=${5:-preview}
cli=${EFFECTCRAFT_CLI:-effectcraft-cli}
mkdir -p "$out"

info=$("$cli" exec comp.info "{\"comp\":\"$comp\"}" "$proj" --json)
# Last renderable frame is duration - 1/fps (a frame at t = duration is outside the comp).
times=$(python3 -c '
import json,sys
d=json.loads(sys.argv[1]); n=int(sys.argv[2]); extra=sys.argv[3].split()
last=d["duration"]-1.0/d["frameRate"]
ts=[round(last*i/(n-1),4) for i in range(n)] if n>1 else [0.0]
ts+= [float(x) for x in extra]
print(" ".join(f"{t:g}" for t in sorted(set(ts))))' "$info" "$n" "${TIMES:-}")

frames=()
for t in $times; do
  f="$out/t_${t}.png"
  msg=$("$cli" render-frame "$proj" --comp "$comp" --time "$t" --max-side "$side" --out "$f" 2>&1) || { echo "$msg" >&2; exit 1; }
  [[ -s "$f" ]] || { echo "empty frame at t=$t" >&2; exit 1; }
  frames+=("$f"); echo "$f"
done

if command -v magick >/dev/null; then
  magick montage "${frames[@]}" -tile "${#frames[@]}x1" -geometry +4+4 -background '#333' -label '%t' "$out/sheet.png" 2>/dev/null \
    || magick montage "${frames[@]}" -tile "${#frames[@]}x1" -geometry +4+4 "$out/sheet.png"
  echo "$out/sheet.png"
fi

#!/usr/bin/env bash
# Render frames of a Lottie .json in a real player (lottie-web 5.12.2 from cdnjs) with headless Chrome,
# to check what a web player shows (fonts, unsupported features) before delivering.
# usage: lottie_preview.sh ANIM.json OUT_DIR FRAME [FRAME…]     (frames are Lottie frame numbers)
# Needs Google Chrome (CHROME=/path to override) and network access to cdnjs.cloudflare.com.
set -euo pipefail
json=${1:?lottie .json}; out=${2:?out dir}; shift 2
[[ $# -gt 0 ]] || { echo "give at least one frame number" >&2; exit 1; }
chrome=${CHROME:-"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"}
command -v "$chrome" >/dev/null || [[ -x "$chrome" ]] || { echo "Chrome not found (set CHROME=…)" >&2; exit 1; }
mkdir -p "$out"
read -r w h < <(python3 -c 'import json,sys;d=json.load(open(sys.argv[1]));print(d["w"],d["h"])' "$json")
vw=960; vh=$(( h * vw / w ))
shots=()
for fr in "$@"; do
  page="$out/page_$fr.html"
  python3 - "$json" "$fr" "$vw" "$vh" > "$page" <<'PY'
import sys
data, fr, vw, vh = open(sys.argv[1]).read(), sys.argv[2], sys.argv[3], sys.argv[4]
print(f"""<!doctype html><html><body style="margin:0;background:#808080">
<div id="a" style="width:{vw}px;height:{vh}px"></div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/bodymovin/5.12.2/lottie.min.js"></script>
<script>var a=lottie.loadAnimation({{container:document.getElementById('a'),renderer:'svg',loop:false,autoplay:false,animationData:{data}}});
a.addEventListener('DOMLoaded',function(){{a.goToAndStop({fr},true);}});</script></body></html>""")
PY
  shot="$(cd "$out" && pwd)/web_$fr.png"
  "$chrome" --headless=new --disable-gpu --hide-scrollbars --window-size="$vw,$vh" --virtual-time-budget=6000 \
    --screenshot="$shot" "file://$(cd "$out" && pwd)/page_$fr.html" >/dev/null 2>&1
  [[ -s "$shot" ]] || { echo "no screenshot for frame $fr" >&2; exit 1; }
  shots+=("$shot"); echo "$shot"
done
if command -v magick >/dev/null; then magick montage "${shots[@]}" -tile "${#shots[@]}x1" -geometry +4+4 "$out/web_sheet.png"; echo "$out/web_sheet.png"; fi

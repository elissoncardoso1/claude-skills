#!/usr/bin/env bash
# Per-character reveal, vertical 1080x1920, 4 s: a Text Animator (opacity 0, position +80 px, blur)
# with a Range Selector whose Start goes 0→100 reveals the title letter by letter; a subtitle fades up.
# Kept inside the 9:16 safe zone (top 14 %, bottom 20 % clear of platform UI).
# usage: TITLE="LANÇAMENTO" SUB="sexta, 20h" text-reveal-per-character.sh [OUT.ecproj]
set -euo pipefail
E=${EFFECTCRAFT_CLI:-effectcraft-cli}
P=${1:-text-reveal.ecproj}
TITLE=${TITLE:-LANÇAMENTO}; SUB=${SUB:-sexta, 20h}
A=text/animators/animator
S=$A/selectors/rangeSelector

$E exec comp.new --params '{"name":"Reveal","width":1080,"height":1920,"frameRate":30,"duration":4,"background":"#111827"}' --empty --save-as "$P" >/dev/null

args=$(mktemp)
cat > "$args" <<EOF
layer.newText
{"text":"$TITLE","name":"Title","font":"Inter","style":"Bold","size":116,"fill":"#ffffff","position":[540,960]}
layer.addTextAnimator
{"layer":"Title","properties":["opacity","position","blur"]}
prop.set
{"layer":"Title","path":"$A/properties/opacity","value":0}
prop.set
{"layer":"Title","path":"$A/properties/position","value":[0,80,0]}
prop.set
{"layer":"Title","path":"$A/properties/blur","value":[12,12]}
prop.addKey
{"layer":"Title","path":"$S/start","time":0.2,"value":0}
prop.addKey
{"layer":"Title","path":"$S/start","time":1.6,"value":100}
layer.newText
{"text":"$SUB","name":"Sub","font":"Inter","style":"Medium","size":56,"fill":"#ffd23f","position":[540,1060]}
prop.addKey
{"layer":"Sub","path":"transform/opacity","time":1.4,"value":0}
prop.addKey
{"layer":"Sub","path":"transform/opacity","time":1.9,"value":100}
prop.addKey
{"layer":"Sub","path":"transform/position","time":1.4,"value":[540,1100,0]}
prop.addKey
{"layer":"Sub","path":"transform/position","time":1.9,"value":[540,1060,0]}
keys.selectAll
{"layers":["Title","Sub"]}
keys.easyEase
{}
EOF
$E run --args-file "$args" "$P" --save >/dev/null
rm -f "$args"
echo "$P"

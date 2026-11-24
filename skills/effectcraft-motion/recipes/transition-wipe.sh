#!/usr/bin/env bash
# Wipe transition 1920x1080, 4 s: scene A (solid + title) is precomposed and wiped away left→right with a
# feathered Linear Wipe (1.5 s → 2.3 s, eased), revealing scene B underneath; a thin accent bar rides
# the wipe edge. Linear Wipe angle: 90 = wipe travels from the left (0 top, 180 bottom, 270 right).
# usage: A_TEXT="CAPÍTULO 1" B_TEXT="CAPÍTULO 2" transition-wipe.sh [OUT.ecproj]
set -euo pipefail
E=${EFFECTCRAFT_CLI:-effectcraft-cli}
P=${1:-transition-wipe.ecproj}
A_TEXT=${A_TEXT:-CAPÍTULO 1}; B_TEXT=${B_TEXT:-CAPÍTULO 2}

$E exec comp.new --params '{"name":"Wipe","width":1920,"height":1080,"frameRate":30,"duration":4,"background":"#000000"}' --empty --save-as "$P" >/dev/null

args=$(mktemp)
cat > "$args" <<EOF
layer.newSolid
{"name":"B BG","color":"#f5efe6"}
layer.newText
{"text":"$B_TEXT","name":"B Title","font":"Inter","style":"Bold","size":150,"fill":"#111827","position":[960,590]}
layer.newSolid
{"name":"A BG","color":"#1d3557"}
layer.newText
{"text":"$A_TEXT","name":"A Title","font":"Inter","style":"Bold","size":150,"fill":"#f1faee","position":[960,590]}
layer.precompose
{"layers":["A BG","A Title"],"name":"Scene A","mode":"move"}
effect.apply
{"effect":"Linear Wipe","layers":["Scene A"]}
prop.set
{"layer":"Scene A","path":"effects/#1/angle","value":90}
prop.set
{"layer":"Scene A","path":"effects/#1/feather","value":60}
prop.addKey
{"layer":"Scene A","path":"effects/#1/completion","time":1.5,"value":0}
prop.addKey
{"layer":"Scene A","path":"effects/#1/completion","time":2.3,"value":100}
layer.newShape
{"kind":"rect","name":"Edge","size":[14,1080],"fill":"#e63946","position":[-20,540]}
prop.addKey
{"layer":"Edge","path":"transform/position","time":1.5,"value":[-20,540,0]}
prop.addKey
{"layer":"Edge","path":"transform/position","time":2.3,"value":[1940,540,0]}
keys.selectAll
{"layers":["Scene A","Edge"]}
keys.easyEase
{}
EOF
$E run --args-file "$args" "$P" --save >/dev/null
rm -f "$args"
echo "$P"

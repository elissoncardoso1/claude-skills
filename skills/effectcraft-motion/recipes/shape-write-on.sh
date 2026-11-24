#!/usr/bin/env bash
# Shape write-on 1920x1080, 3 s: a hand-drawn bezier stroke (pen path with tangents) draws on with
# Trim Paths End, then draws off with Start (classic "write-on / write-off"); round caps and joins.
# usage: COLOR="#ff5a36" shape-write-on.sh [OUT.ecproj]
set -euo pipefail
E=${EFFECTCRAFT_CLI:-effectcraft-cli}
P=${1:-shape-write-on.ecproj}
COLOR=${COLOR:-#ff5a36}

$E exec comp.new --params '{"name":"Write On","width":1920,"height":1080,"frameRate":30,"duration":3,"background":"#0b1020"}' --empty --save-as "$P" >/dev/null

# A wave across the frame: comp-space vertices with symmetric bezier tangents (relative to each vertex).
args=$(mktemp)
cat > "$args" <<EOF
shape.newPath
{"name":"Stroke","space":"comp","vertices":[[260,620],[760,420],[1160,660],[1660,460]],"inTangents":[[0,0],[-180,0],[-180,0],[-180,0]],"outTangents":[[180,0],[180,0],[180,0],[0,0]],"closed":false,"fill":false,"stroke":"$COLOR","strokeWidth":22}
EOF
$E run --args-file "$args" "$P" --save --json >/dev/null
rm -f "$args"
# shape.newPath stores the path in layer space (centred) under contents/group/contents/{path,stroke}.
STROKE=contents/group/contents/stroke
$E run "$P" \
  layer.addShapeItem '{"layer":"Stroke","kind":"trim"}' \
  prop.set "{\"layer\":\"Stroke\",\"path\":\"$STROKE/cap\",\"value\":1}" \
  prop.set "{\"layer\":\"Stroke\",\"path\":\"$STROKE/join\",\"value\":1}" \
  prop.addKey '{"layer":"Stroke","path":"contents/trim/end","time":0,"value":0}' \
  prop.addKey '{"layer":"Stroke","path":"contents/trim/end","time":1.2,"value":100}' \
  prop.addKey '{"layer":"Stroke","path":"contents/trim/start","time":1.6,"value":0}' \
  prop.addKey '{"layer":"Stroke","path":"contents/trim/start","time":2.7,"value":100}' \
  keys.selectAll '{"layers":["Stroke"]}' keys.easyEase '{}' --save >/dev/null
echo "$P"

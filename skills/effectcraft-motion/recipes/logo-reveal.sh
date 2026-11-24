#!/usr/bin/env bash
# Logo reveal 1920x1080, 4 s: a glowing ring draws on (Trim Paths + offset spin), a star mark pops in
# (scale overshoot + rotation), the wordmark rises and fades in under it. Glow on ring and mark.
# usage: BRAND="NOVA" ACCENT="#36c5ff" logo-reveal.sh [OUT.ecproj]
set -euo pipefail
E=${EFFECTCRAFT_CLI:-effectcraft-cli}
P=${1:-logo-reveal.ecproj}
BRAND=${BRAND:-NOVA}; ACCENT=${ACCENT:-#36c5ff}

$E exec comp.new --params '{"name":"Logo Reveal","width":1920,"height":1080,"frameRate":30,"duration":4,"background":"#05070d"}' --empty --save-as "$P" >/dev/null

args=$(mktemp)
cat > "$args" <<EOF
layer.newShape
{"kind":"ellipse","name":"Ring","size":[320,320],"fillType":"none","stroke":"$ACCENT","strokeWidth":12,"position":[960,450]}
prop.set
{"layer":"Ring","path":"contents/group/contents/stroke/cap","value":1}
layer.addShapeItem
{"layer":"Ring","kind":"trim"}
prop.addKey
{"layer":"Ring","path":"contents/trim/end","time":0,"value":0}
prop.addKey
{"layer":"Ring","path":"contents/trim/end","time":1.2,"value":100}
prop.addKey
{"layer":"Ring","path":"contents/trim/offset","time":0,"value":-90}
prop.addKey
{"layer":"Ring","path":"contents/trim/offset","time":1.2,"value":0}
layer.newShape
{"kind":"star","name":"Mark","size":[170,170],"fill":"#ffffff","position":[960,450]}
prop.addKey
{"layer":"Mark","path":"transform/scale","time":0.8,"value":[0,0,100]}
prop.addKey
{"layer":"Mark","path":"transform/scale","time":1.15,"value":[115,115,100]}
prop.addKey
{"layer":"Mark","path":"transform/scale","time":1.4,"value":[100,100,100]}
prop.addKey
{"layer":"Mark","path":"transform/rotation","time":0.8,"value":-72}
prop.addKey
{"layer":"Mark","path":"transform/rotation","time":1.4,"value":0}
layer.newText
{"text":"$BRAND","name":"Wordmark","font":"Inter","style":"SemiBold","size":110,"fill":"#ffffff","tracking":300,"position":[960,790]}
prop.addKey
{"layer":"Wordmark","path":"transform/position","time":1.3,"value":[960,830,0]}
prop.addKey
{"layer":"Wordmark","path":"transform/position","time":1.9,"value":[960,790,0]}
prop.addKey
{"layer":"Wordmark","path":"transform/opacity","time":1.3,"value":0}
prop.addKey
{"layer":"Wordmark","path":"transform/opacity","time":1.8,"value":100}
keys.selectAll
{"layers":["Ring","Mark","Wordmark"]}
keys.easyEase
{}
EOF
$E run --args-file "$args" "$P" --save >/dev/null
rm -f "$args"
# Glow (one undo step each through add_effect in MCP; here effect.apply + prop.set).
$E run "$P" \
  effect.apply '{"effect":"Glow","layers":["Ring"]}' \
  prop.set '{"layer":"Ring","path":"effects/#1/threshold","value":20}' \
  prop.set '{"layer":"Ring","path":"effects/#1/radius","value":45}' \
  prop.set '{"layer":"Ring","path":"effects/#1/intensity","value":1.6}' \
  effect.apply '{"effect":"Glow","layers":["Mark"]}' \
  prop.set '{"layer":"Mark","path":"effects/#1/threshold","value":30}' \
  prop.set '{"layer":"Mark","path":"effects/#1/radius","value":30}' --save >/dev/null
echo "$P"

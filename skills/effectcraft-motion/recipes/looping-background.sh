#!/usr/bin/env bash
# Seamless looping background, 10 s: Fractal Noise whose Evolution is driven by an expression that turns
# exactly `cycle` revolutions per loop (Cycle Evolution on), colourised with Tint. With Cycle Evolution,
# evolution 720 (2 revolutions) renders exactly like 0, so frame at t = duration equals frame 0: it loops.
# Anything else animated (offset, scale…) must also return to its start value at t = duration.
# usage: W=1920 H=1080 DUR=10 DARK="#120a2a" LIGHT="#ff7a59" looping-background.sh [OUT.ecproj]
set -euo pipefail
E=${EFFECTCRAFT_CLI:-effectcraft-cli}
P=${1:-looping-background.ecproj}
W=${W:-1920}; H=${H:-1080}; DUR=${DUR:-10}; DARK=${DARK:-#120a2a}; LIGHT=${LIGHT:-#ff7a59}
FX=effects/#1

$E exec comp.new --params "{\"name\":\"Loop BG\",\"width\":$W,\"height\":$H,\"frameRate\":30,\"duration\":$DUR,\"background\":\"#000000\"}" --empty --save-as "$P" >/dev/null

args=$(mktemp)
cat > "$args" <<EOF
layer.newSolid
{"name":"Noise","color":"#000000"}
effect.apply
{"effect":"Fractal Noise","layers":["Noise"]}
prop.set
{"layer":"Noise","path":"$FX/fractalType","value":1}
prop.set
{"layer":"Noise","path":"$FX/contrast","value":220}
prop.set
{"layer":"Noise","path":"$FX/brightness","value":-90}
prop.set
{"layer":"Noise","path":"$FX/transform/scale","value":260}
prop.set
{"layer":"Noise","path":"$FX/complexity","value":4}
prop.set
{"layer":"Noise","path":"$FX/evolutionOptions/cycleEvolution","value":true}
prop.set
{"layer":"Noise","path":"$FX/evolutionOptions/cycle","value":2}
prop.setExpression
{"layer":"Noise","path":"$FX/evolution","expression":"time / thisComp.duration * 360 * effect(\"Fractal Noise\")(\"Evolution Options\")(\"Cycle (in Revolutions)\")"}
effect.apply
{"effect":"Tint","layers":["Noise"]}
prop.set
{"layer":"Noise","path":"effects/#2/black","value":"$DARK"}
prop.set
{"layer":"Noise","path":"effects/#2/white","value":"$LIGHT"}
EOF
$E run --args-file "$args" "$P" --save >/dev/null
rm -f "$args"
echo "$P"

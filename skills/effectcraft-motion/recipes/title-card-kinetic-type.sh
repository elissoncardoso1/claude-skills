#!/usr/bin/env bash
# Kinetic title card 1920x1080, 4 s: three words pop in one after another (scale overshoot 0→112→100,
# 0.2 s stagger), an underline draws on with Trim Paths, everything drifts up and fades out at the end.
# usage: W1=MAKE W2=IT W3=MOVE ACCENT="#ffd23f" title-card-kinetic-type.sh [OUT.ecproj]
set -euo pipefail
E=${EFFECTCRAFT_CLI:-effectcraft-cli}
P=${1:-title-card.ecproj}
W1=${W1:-MAKE}; W2=${W2:-IT}; W3=${W3:-MOVE}; ACCENT=${ACCENT:-#ffd23f}

$E exec comp.new --params '{"name":"Title Card","width":1920,"height":1080,"frameRate":30,"duration":4,"background":"#0b1020"}' --empty --save-as "$P" >/dev/null

args=$(mktemp)
{
  # Text baseline sits on position.y; 3 lines of 200 px Inter Bold baselines at 430, 620, 810; block centred near y=540.
  i=0
  for w in "$W1" "$W2" "$W3"; do
    i=$((i+1)); y=$((240 + i*190)); t0=$(python3 -c "print(round(0.2*($i-1),2))")
    cat <<EOF
layer.newText
{"text":"$w","name":"Word$i","font":"Inter","style":"Bold","size":200,"fill":"#ffffff","tracking":-20,"position":[960,$y]}
prop.set
{"layer":"Word$i","path":"transform/anchor","value":[0,-70,0]}
prop.set
{"layer":"Word$i","path":"transform/position","value":[960,$((y-70)),0]}
prop.addKey
{"layer":"Word$i","path":"transform/scale","time":$t0,"value":[0,0,100]}
prop.addKey
{"layer":"Word$i","path":"transform/scale","time":$(python3 -c "print($t0+0.28)"),"value":[112,112,100]}
prop.addKey
{"layer":"Word$i","path":"transform/scale","time":$(python3 -c "print($t0+0.5)"),"value":[100,100,100]}
prop.addKey
{"layer":"Word$i","path":"transform/opacity","time":$t0,"value":0}
prop.addKey
{"layer":"Word$i","path":"transform/opacity","time":$(python3 -c "print($t0+0.15)"),"value":100}
prop.addKey
{"layer":"Word$i","path":"transform/opacity","time":3.3,"value":100}
prop.addKey
{"layer":"Word$i","path":"transform/opacity","time":3.8,"value":0}
EOF
  done
  cat <<EOF
layer.newShape
{"kind":"rect","name":"Underline","size":[520,14],"fill":"$ACCENT","position":[960,860]}
layer.addShapeItem
{"layer":"Underline","kind":"trim"}
prop.addKey
{"layer":"Underline","path":"contents/trim/end","time":0.7,"value":0}
prop.addKey
{"layer":"Underline","path":"contents/trim/end","time":1.3,"value":100}
prop.addKey
{"layer":"Underline","path":"transform/opacity","time":3.3,"value":100}
prop.addKey
{"layer":"Underline","path":"transform/opacity","time":3.8,"value":0}
layer.newNull
{"name":"Drift"}
prop.set
{"layer":"Drift","path":"transform/position","value":[960,540,0]}
layer.setParent
{"layers":["Word1","Word2","Word3","Underline"],"parent":"Drift"}
prop.addKey
{"layer":"Drift","path":"transform/position","time":3.2,"value":[960,540,0]}
prop.addKey
{"layer":"Drift","path":"transform/position","time":3.8,"value":[960,470,0]}
keys.selectAll
{"layers":["Word1","Word2","Word3","Underline","Drift"]}
keys.easyEase
{}
EOF
} > "$args"
$E run --args-file "$args" "$P" --save >/dev/null
rm -f "$args"
echo "$P"

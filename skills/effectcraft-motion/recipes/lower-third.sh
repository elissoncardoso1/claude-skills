#!/usr/bin/env bash
# Lower third 1920x1080, 6 s: panel grows from the left, accent bar, name + role slide in; mirrored exit.
# usage: NAME="Ana Souza" ROLE="Diretora de Arte" ACCENT="#ff5a36" lower-third.sh [OUT.ecproj]
set -euo pipefail
E=${EFFECTCRAFT_CLI:-effectcraft-cli}
P=${1:-lower-third.ecproj}
NAME=${NAME:-Ana Souza}; ROLE=${ROLE:-Diretora de Arte}; ACCENT=${ACCENT:-#ff5a36}
# Layout: left title-safe margin 10% (x=192); panel 760x150 with its centre line at y=880.
X=192; Y=880; W=760; H=150

$E exec comp.new --params '{"name":"Lower Third","width":1920,"height":1080,"frameRate":30,"duration":6,"background":"#1f2937"}' --empty --save-as "$P" >/dev/null

args=$(mktemp)
cat > "$args" <<EOF
layer.newShape
{"kind":"rect","name":"Panel","size":[$W,$H],"fill":"#0f172a","fillOpacity":88,"position":[$((X+W/2)),$Y]}
prop.set
{"layer":"Panel","path":"transform/anchor","value":[-$((W/2)),0,0]}
prop.set
{"layer":"Panel","path":"transform/position","value":[$X,$Y,0]}
layer.newShape
{"kind":"rect","name":"Accent","size":[10,$H],"fill":"$ACCENT","position":[$((X+5)),$Y]}
layer.newText
{"text":"$NAME","name":"Name","font":"Inter","style":"Bold","size":58,"fill":"#ffffff","justify":"left","position":[$((X+44)),$((Y-6))]}
layer.newText
{"text":"$ROLE","name":"Role","font":"Inter","style":"Regular","size":34,"fill":"#cbd5e1","justify":"left","position":[$((X+44)),$((Y+44))]}
prop.addKey
{"layer":"Panel","path":"transform/scale","time":0,"value":[0,100,100]}
prop.addKey
{"layer":"Panel","path":"transform/scale","time":0.6,"value":[100,100,100]}
prop.addKey
{"layer":"Panel","path":"transform/scale","time":5.3,"value":[100,100,100]}
prop.addKey
{"layer":"Panel","path":"transform/scale","time":5.85,"value":[0,100,100]}
prop.addKey
{"layer":"Accent","path":"transform/scale","time":0.1,"value":[100,0,100]}
prop.addKey
{"layer":"Accent","path":"transform/scale","time":0.45,"value":[100,100,100]}
prop.addKey
{"layer":"Accent","path":"transform/scale","time":5.5,"value":[100,100,100]}
prop.addKey
{"layer":"Accent","path":"transform/scale","time":5.85,"value":[100,0,100]}
prop.addKey
{"layer":"Name","path":"transform/position","time":0.3,"value":[$((X+4)),$((Y-6)),0]}
prop.addKey
{"layer":"Name","path":"transform/position","time":0.85,"value":[$((X+44)),$((Y-6)),0]}
prop.addKey
{"layer":"Name","path":"transform/opacity","time":0.3,"value":0}
prop.addKey
{"layer":"Name","path":"transform/opacity","time":0.75,"value":100}
prop.addKey
{"layer":"Name","path":"transform/opacity","time":5.1,"value":100}
prop.addKey
{"layer":"Name","path":"transform/opacity","time":5.4,"value":0}
prop.addKey
{"layer":"Role","path":"transform/position","time":0.45,"value":[$((X+4)),$((Y+44)),0]}
prop.addKey
{"layer":"Role","path":"transform/position","time":1.0,"value":[$((X+44)),$((Y+44)),0]}
prop.addKey
{"layer":"Role","path":"transform/opacity","time":0.45,"value":0}
prop.addKey
{"layer":"Role","path":"transform/opacity","time":0.9,"value":100}
prop.addKey
{"layer":"Role","path":"transform/opacity","time":5.0,"value":100}
prop.addKey
{"layer":"Role","path":"transform/opacity","time":5.3,"value":0}
keys.selectAll
{"layers":["Panel","Accent","Name","Role"]}
keys.easyEase
{}
EOF
$E run --args-file "$args" "$P" --save >/dev/null
rm -f "$args"
echo "$P"

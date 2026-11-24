# Example: recolor a folder of SVGs with the CLI (verified 2026-10-23: C18, C22, C23, C29; audits S7, R4)

```bash
IN=in; OUT=out-recolored; SAMPLE=out-sample; MAP='{"map":{"#e53935":"#0055ff"}}'
mkdir -p "$OUT" "$SAMPLE"
# 0. untrusted inputs: see references/safety.md (linked local files)
# 1. one sample, in its own folder
f=$(ls "$IN"/*.svg | head -1)
vectorcraft-cli info "$f"
vectorcraft-cli run --in "$f" --cmd select.all --cmd recolor.colors          # colour keys present
vectorcraft-cli run --in "$f" --cmd select.all --cmd recolor.apply --params "$MAP" \
  --export "$SAMPLE/sample.svg" --export "$SAMPLE/sample.png" --scale 4
# Read $SAMPLE/sample.png
# 2. all files: never overwrite; a file whose colour isn't there is NOT delivered
for f in "$IN"/*.svg; do
  o="$OUT/$(basename "${f%.svg}")"
  [ -e "$o.svg" ] && { echo "SKIP $o.svg exists"; continue; }
  log=$(vectorcraft-cli run --in "$f" --cmd select.all --cmd recolor.apply --params "$MAP" \
        --export "$o.svg" --export "$o.png" --scale 2) || { echo "FAIL $f"; continue; }
  if grep -q '"changed":0' <<<"$log"; then rm -f "$o.svg" "$o.png"; echo "UNCHANGED $f (colour not found, no output)"
  else echo "ok $f"; fi
done
# 3. audit (case-insensitive; fill="#000000" on an unfilled <path> is the SVG default, not a recolour)
ls "$IN"/*.svg | wc -l; ls "$OUT"/*.svg | wc -l                  # out = in − UNCHANGED
grep -hoi '\(fill\|stroke\)="#[0-9a-f]*"' "$OUT"/*.svg | sort | uniq -c
grep -li 'e53935' "$OUT"/*.svg && echo "old colour still present"
```

Notes
- `recolor.apply` without a selection fails: "select artwork to recolour, or give a colour `group`" (C23).
- It recolours fills and strokes of the mapped colour, upper- or lower-case hex in the source (R4: `#E53935` matched).
- With no matching colour it returns `{"changed":0}` and exit 0, and the exports are still written — hence the `rm` + UNCHANGED.
- `select.all` + `paint.setFill {color}` (C18) repaints every fill regardless of its colour; [inferred, not tested] it would also fill stroke-only paths.

#!/usr/bin/env bash
# Render a comp and verify the output exists and matches the comp (duration, size, alpha).
# usage: render.sh PROJECT.ecproj COMP OUT FORMAT [extra effectcraft-cli render args…]
#   FORMAT: h264 | hevc | av1 | prores | webm | png | jpeg | tiff | exr | gif
#   alpha: add `--channels rgba` (prores → 4444, webm needs `--webm-codec vp9`, png/gif ok; h264 refuses)
#   sequences: OUT must contain [#####], e.g. 'frames/f_[#####].png'
# Refuses to overwrite an existing OUT (the CLI overwrites silently) unless FORCE=1.
set -euo pipefail
proj=${1:?project}; comp=${2:?comp}; out=${3:?output}; fmt=${4:?format}; shift 4
cli=${EFFECTCRAFT_CLI:-effectcraft-cli}

if [[ "$out" != *"[#"* && -e "$out" && "${FORCE:-0}" != 1 ]]; then
  echo "refusing to overwrite $out (set FORCE=1)" >&2; exit 1
fi
info=$("$cli" exec comp.info "{\"comp\":\"$comp\"}" "$proj" --json)
"$cli" render "$proj" --comp "$comp" --out "$out" --format "$fmt" "$@"

alpha=0; [[ " $* " == *" --channels rgba "* ]] && alpha=1
python3 - "$info" "$out" "$fmt" "$alpha" "$@" <<'PY'
import json, sys, glob, os, shutil, subprocess
info, out, fmt, alpha, extra = json.loads(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4] == "1", sys.argv[5:]
dur, fps, w, h = info["duration"], info["frameRate"], info["width"], info["height"]
if "--resolution" in extra:  # full | half | third | quarter | K (downsample factor)
    k = {"full": 1, "half": 2, "third": 3, "quarter": 4}.get(extra[extra.index("--resolution") + 1])
    w, h = (int(w / k), int(h / k)) if k else (None, None)  # numeric K: semantics unverified, skip size check
if "--fps" in extra:
    fps = float(extra[extra.index("--fps") + 1])
problems = []
if "[#" in out:
    pat = out[:out.index("[#")] + "*" + out[out.index("]") + 1:]
    files = sorted(glob.glob(pat))
    want = round(dur * fps)
    print(f"sequence: {len(files)} files (expected ~{want})")
    if abs(len(files) - want) > 1: problems.append(f"frame count {len(files)} != {want}")
    probe_target = files[len(files) // 2] if files else None
else:
    if not os.path.exists(out) or os.path.getsize(out) == 0: sys.exit(f"FAIL: {out} missing or empty")
    print(f"file: {out} {os.path.getsize(out)} bytes")
    probe_target = out
if probe_target and shutil.which("ffprobe"):
    q = ["ffprobe", "-v", "error", "-show_entries", "stream=codec_name,width,height,pix_fmt:stream_tags=alpha_mode:format=duration", "-of", "json"]
    p = json.loads(subprocess.run(q + [probe_target], capture_output=True, text=True).stdout or "{}")
    s = (p.get("streams") or [{}])[0]; d = float((p.get("format") or {}).get("duration") or 0)
    print("ffprobe:", s, "duration", d)
    if w and (s.get("width"), s.get("height")) not in ((w, h), (w & ~1, h & ~1)): problems.append(f"size {s.get('width')}x{s.get('height')} != {w}x{h}")
    if "[#" not in out and fmt not in ("png", "jpeg", "tiff", "exr") and abs(d - dur) > 1.5 / fps: problems.append(f"duration {d} != {dur}")
    if alpha:
        has = "a" in (s.get("pix_fmt") or "") or (s.get("tags") or {}).get("alpha_mode") == "1" or s.get("pix_fmt") in ("bgra", "rgba", "pal8")
        if not has: problems.append(f"no alpha in output (pix_fmt {s.get('pix_fmt')})")
elif probe_target:
    print("ffprobe not found: only existence checked")
if problems: sys.exit("FAIL: " + "; ".join(problems))
print("OK")
PY

#!/usr/bin/env python3
"""Summarize and sanity-check a FilmCraft project before export (read-only).

Usage: fc_check.py PROJECT.fcproj [--cli PATH] [--json]
Prints the active sequence (size, fps, length), each track's clips in seconds,
keyframes (in sequence seconds), transitions, markers and media status. Reads the saved
file, so save the project first. Exit 1 when media is offline/missing,
when a video clip is not the sequence's frame size and is left at 100 % scale
(it will appear cropped or letterboxed), or when the file is not a FilmCraft project.
"""
import json, os, shutil, subprocess, sys

TPS = 254016000000  # ticks per second

def cli_json(cli, *args):
    r = subprocess.run([cli, *args, "--compact"], capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"filmcraft-cli {' '.join(args)} failed: {r.stderr.strip()}")
    return json.loads(r.stdout)

def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        print(__doc__); return 2
    proj, cli, as_json = a[0], shutil.which("filmcraft-cli") or os.path.expanduser("~/.local/bin/filmcraft-cli"), "--json" in a
    if "--cli" in a: cli = a[a.index("--cli") + 1]
    with open(proj, encoding="utf-8") as f:
        doc = json.load(f)
    if doc.get("format") != "filmcraft.project":
        sys.exit(f"{proj}: not a FilmCraft project (format={doc.get('format')!r})")
    seq = cli_json(cli, "--project", proj, "inspect", "sequence")
    media = cli_json(cli, "--project", proj, "exec", "media.status")
    s = seq["settings"]; fr = s["frame_rate"]; fps = fr["num"] / fr["den"]
    problems = []
    report = {"schema_version": doc.get("schema_version"), "generator": doc.get("generator"),
              "sequence": seq.get("name"), "size": [s["width"], s["height"]], "fps": round(fps, 3),
              "seconds": round(seq["duration"] / TPS, 3), "frames": seq["durationFrames"],
              "tracks": [], "markers": [(m["name"], round(m["start"] / TPS, 3)) for m in seq["markers"]],
              "media": [(m["item"], m["name"], m["status"]) for m in media]}
    sizes, kfs = {}, {}
    for item in doc["project"]["items"].values():
        for t in item.get("kind", {}).get("Sequence", {}).get("video_tracks", []) + item.get("kind", {}).get("Sequence", {}).get("audio_tracks", []):
            for c in t.get("items", []):
                for e in c.get("effects", []):
                    for pname, pv in e.get("params", {}).items():
                        if pv.get("keyframes"):
                            # stored relative to the clip; shown as sequence seconds
                            kfs.setdefault(c["id"], []).append(f"{e['effect']}.{pname}@" + ",".join(
                                f"{round((c['start'] + k['time']) / TPS, 3)}s={list(k['value'].values())[0] if isinstance(k['value'], dict) else k['value']}"
                                for k in pv["keyframes"]))
        info = item.get("kind", {}).get("Media", {}).get("info", {})
        if info.get("video"):
            sizes[item["id"]] = (info["video"]["width"], info["video"]["height"])
    for kind in ("video", "audio"):
        for t in seq[kind]:
            clips = []
            for c in t["items"]:
                clips.append({"clip": c["clip"], "name": c["name"], "start": round(c["start"] / TPS, 3),
                              "end": round(c["end"] / TPS, 3), "speed": c["speed"], "keyframes": kfs.get(c["clip"], [])})
                if kind == "video" and c.get("item") in sizes and sizes[c["item"]] != (s["width"], s["height"]):
                    motion = next((e for e in c["effects"] if e["effect"] == "motion"), None)
                    if motion and motion["params"]["scale"]["value"] == "Float(100.0)":
                        problems.append(f"clip {c['clip']} ({c['name']}) is {sizes[c['item']][0]}x{sizes[c['item']][1]} "
                                        f"in a {s['width']}x{s['height']} sequence at 100 % scale: run clip.fitToFrame")
            if clips or t.get("transitions"):
                report["tracks"].append({"track": t["name"], "clips": clips,
                                         "transitions": [(x["effect"], round(x["start"] / TPS, 3), round(x["duration"] / TPS, 3))
                                                         for x in t.get("transitions", [])]})
    problems += [f"media item {i} {n} is {st}" for i, n, st in report["media"] if st != "online"]
    report["problems"] = problems
    if as_json:
        print(json.dumps(report, ensure_ascii=False, indent=1))
    else:
        print(f"{report['sequence']}: {s['width']}x{s['height']} @ {report['fps']} fps, "
              f"{report['seconds']} s ({report['frames']} frames) · schema v{report['schema_version']}")
        for t in report["tracks"]:
            print(f"  {t['track']}: " + ", ".join(f"[{c['clip']}] {c['name']} {c['start']}-{c['end']}s"
                                                + ("" if c["speed"] == 1 else f" x{c['speed']}") for c in t["clips"]))
            for x in t["transitions"]:
                print(f"    transition {x[0]} at {x[1]}s for {x[2]}s")
            for c in t["clips"]:
                for k in c["keyframes"]:
                    print(f"    keyframes [{c['clip']}] {k}")
        if report["markers"]:
            print("  markers: " + ", ".join(f"{n}@{t}s" for n, t in report["markers"]))
        print("  media: " + ", ".join(f"{n} ({st})" for _, n, st in report["media"]))
        print("OK" if not problems else "PROBLEMS:\n  - " + "\n  - ".join(problems))
    return 1 if problems else 0

if __name__ == "__main__":
    sys.exit(main())

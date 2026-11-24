# Workflow recipe: single-page event flyer, A5 with 3 mm bleed, CMYK swatches, image, grid of info blocks.
import json, os, sys
W, H, BL = 419.528, 595.276, 8.504
img = os.path.abspath(sys.argv[2] if len(sys.argv) > 2 else "hero.jpg")
steps = []
def s(cmd, **p): steps.append(f"{cmd} {json.dumps(p, ensure_ascii=False)}"); return len(steps) - 1
def r(i, k): return f"${i}.{k}"
M = 28
s("file.new", preset="A5", facingPages=False, margins=M, bleed=BL, title="Jazz Night flyer")
s("swatch.create", name="Night", color={"c": 85, "m": 75, "y": 30, "k": 45})
s("swatch.create", name="Gold", color={"c": 0, "m": 25, "y": 95, "k": 0})
s("style.paragraph.create", name="Display", chars={"fontFamily": "Source Sans 3", "fontStyle": "Bold", "size": 54, "leading": {"kind": "points", "value": 50}, "fill": "[Paper]"})
s("style.paragraph.create", name="Info Head", chars={"fontFamily": "Source Sans 3", "fontStyle": "Bold", "size": 9, "tracking": 100, "fill": "Gold"}, para={"spaceAfter": 2})
s("style.paragraph.create", name="Info", chars={"fontFamily": "Source Sans 3", "size": 12, "leading": {"kind": "points", "value": 15}, "fill": "[Paper]"})
bg = s("frame.create", rect=[-BL, -BL, W + BL, H + BL], content="graphic"); s("object.fill", swatch="Night", ids=[r(bg, "id")])
ph = s("frame.create", rect=[-BL, -BL, W + BL, 300], content="graphic")
s("file.place", path=img, frame=r(ph, "id")); s("object.fit", mode="fillProportionally", ids=[r(ph, "id")])
t = s("frame.create", rect=[M, 312, W - M, 430], content="text", text="Jazz\u2028Night")
s("selection.set", ids=[r(t, "id")]); s("style.paragraph.apply", name="Display")
col = (W - 2 * M - 2 * 12) / 3
ids = []
for i, (h, v) in enumerate([("WHEN", "Fri 14 Nov\n8 pm"), ("WHERE", "Blue Hall\nRiver St 12"), ("TICKETS", "€15 / €10\njazz.example")]):
    x = M + i * (col + 12)
    f = s("frame.create", rect=[x, 460, x + col, 530], content="text", text=f"{h}\n{v}")
    s("selection.set", ids=[r(f, "id")]); s("style.paragraph.apply", name="Info")
    s("text.select", story=r(f, "story"), anchor=0, focus=0); s("style.paragraph.apply", name="Info Head")
    ids.append(r(f, "id"))
s("object.align", edge="top", to="selection", ids=ids)
bar = s("frame.create", rect=[M, 548, W - M, 552], content="graphic"); s("object.fill", swatch="Gold", ids=[r(bar, "id")])
s("document.inspect")
open(sys.argv[1] if len(sys.argv) > 1 else "flyer.dcs", "w").write("\n".join(steps) + "\n")

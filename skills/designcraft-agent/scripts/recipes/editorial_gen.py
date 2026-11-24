# Workflow recipe: magazine feature spread (pages 2-3 of a facing A4 doc): full-bleed photo left,
# headline + deck + 3-column body with drop cap + pull quote right.
import json, os, sys
W, H, BLEED = 595.276, 841.89, 9
img = os.path.abspath(sys.argv[2] if len(sys.argv) > 2 else "hero.jpg")
steps = []
def s(cmd, **p): steps.append(f"{cmd} {json.dumps(p, ensure_ascii=False)}"); return len(steps) - 1
def r(i, k): return f"${i}.{k}"
s("file.new", preset="A4", facingPages=True, pages=3, margins={"top": 54, "bottom": 60, "inside": 54, "outside": 42}, bleed=BLEED)
s("swatch.create", name="Ink", color={"c": 0, "m": 0, "y": 0, "k": 90})
s("swatch.create", name="Red", color={"c": 0, "m": 90, "y": 85, "k": 0})
s("style.paragraph.create", name="Kicker", chars={"fontFamily": "Source Sans 3", "fontStyle": "Bold", "size": 9, "tracking": 120, "fill": "Red"}, para={"spaceAfter": 6})
s("style.paragraph.create", name="Headline", chars={"fontFamily": "Source Serif 4", "fontStyle": "Bold", "size": 40, "leading": {"kind": "points", "value": 42}, "fill": "Ink"}, para={"spaceAfter": 10})
s("style.paragraph.create", name="Deck", chars={"fontFamily": "Source Serif 4", "fontStyle": "Italic", "size": 14, "leading": {"kind": "points", "value": 19}, "fill": "Ink"}, para={"spaceAfter": 0})
s("style.paragraph.create", name="Body", chars={"fontFamily": "Source Serif 4", "size": 9.5, "leading": {"kind": "points", "value": 13}, "fill": "Ink"}, para={"align": "leftJustified", "firstLineIndent": 10})
s("style.paragraph.create", name="Body First", basedOn="Body", para={"firstLineIndent": 0, "dropCapLines": 3, "dropCapChars": 1})
s("style.paragraph.create", name="Pull", chars={"fontFamily": "Source Sans 3", "fontStyle": "Semibold", "size": 15, "leading": {"kind": "points", "value": 19}, "fill": "Red"}, para={"align": "left"})
s("style.paragraph.create", name="Caption", chars={"fontFamily": "Source Sans 3", "size": 7.5, "fill": "[Paper]"})
# spread 1 = pages 2 (left, x 0..W) and 3 (right, x W..2W). Photo bleeds off the left page.
ph = s("frame.create", spread=1, rect=[-BLEED, -BLEED, W, H + BLEED], content="graphic")
s("file.place", path=img, frame=r(ph, "id")); s("object.fit", mode="fillProportionally", ids=[r(ph, "id")])
cap = s("frame.create", spread=1, rect=[42, H - 60, 300, H - 42], content="text", text="Photo: the observatory at dusk.")
s("selection.set", ids=[r(cap, "id")]); s("style.paragraph.apply", name="Caption")
X0, X1 = W + 54, 2 * W - 42
hd = s("frame.create", spread=1, rect=[X0, 54, X1, 250], content="text",
       text="SCIENCE\nWhat the night sky still hides\nAstronomers are mapping the faint light between galaxies, and it is changing how we count the universe.")
s("selection.set", ids=[r(hd, "id")]); s("style.paragraph.apply", name="Deck")
s("text.select", story=r(hd, "story"), anchor=0, focus=0); s("style.paragraph.apply", name="Kicker")
s("text.select", story=r(hd, "story"), anchor=8, focus=8); s("style.paragraph.apply", name="Headline")
s("line.create", spread=1, a=[X0, 262], b=[X1, 262]); s("object.stroke", swatch="Ink", weight=0.75)
p = "Light from the earliest galaxies arrives stretched and dim, and for decades it was treated as noise. New surveys now count it photon by photon. "
body = "\n".join([p * 4] * 6)
bd = s("frame.create", spread=1, rect=[X0, 276, X1, H - 60], content="text", text=body)
s("object.textFrameOptions", columns=3, gutter=12, ids=[r(bd, "id")])
s("selection.set", ids=[r(bd, "id")]); s("style.paragraph.apply", name="Body")
s("text.select", story=r(bd, "story"), anchor=0, focus=0); s("style.paragraph.apply", name="Body First")
pq = s("frame.create", spread=1, rect=[X0 + 167, 470, X1, 506], content="text", text="“It is changing how we count the universe.”")
s("selection.set", ids=[r(pq, "id")]); s("style.paragraph.apply", name="Pull")
s("object.textWrap", mode="boundingBox", offset=[8, 8, 8, 8], ids=[r(pq, "id")])
s("story.get", story=r(bd, "story"))
open(sys.argv[1] if len(sys.argv) > 1 else "editorial.dcs", "w").write("\n".join(steps) + "\n")

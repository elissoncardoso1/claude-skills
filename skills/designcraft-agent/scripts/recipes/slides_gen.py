# Workflow recipe: paginated 16:9 presentation (Web 1920x1080 preset, in points), parent-page footer,
# title slide + bullet slides + image slide; export PDF and PPTX.
import json, os, sys
W, H, M = 1920.0, 1080.0, 96
img = os.path.abspath(sys.argv[2] if len(sys.argv) > 2 else "hero.jpg")
slides = [("Quarterly review", "Q3 2026 · Product team"),
          ("What shipped", ["Faster export pipeline", "New template gallery", "Offline mode beta"]),
          ("What we learned", ["Users want fewer clicks", "Templates drive retention", "Support load fell 18%"]),
          ("Next quarter", None)]
steps = []
def s(cmd, **p): steps.append(f"{cmd} {json.dumps(p, ensure_ascii=False)}"); return len(steps) - 1
def r(i, k): return f"${i}.{k}"
s("file.new", preset="Web 1920 × 1080", facingPages=False, pages=len(slides), margins=M)
s("swatch.create", name="Ink", color="#16213E"); s("swatch.create", name="Brand", color="#E94560")
s("style.paragraph.create", name="Slide Title", chars={"fontFamily": "Source Sans 3", "fontStyle": "Bold", "size": 88, "leading": {"kind": "points", "value": 92}, "fill": "Ink"})
s("style.paragraph.create", name="Subtitle", chars={"fontFamily": "Source Sans 3", "size": 40, "fill": "Brand"})
s("style.paragraph.create", name="Bullet", chars={"fontFamily": "Source Sans 3", "size": 48, "leading": {"kind": "points", "value": 60}, "fill": "Ink"}, para={"spaceAfter": 24})
s("style.paragraph.create", name="Footer", chars={"fontFamily": "Source Sans 3", "size": 20, "fill": "Ink"})
for rect, text, al in (([M, H - 70, W / 2, H - 40], "Product team · Q3 2026", "left"),
                       ([W / 2, H - 70, W - M, H - 40], "\ue000", "right")):   # \ue000 = page number
    f = s("frame.create", spread={"kind": "parent", "index": 0}, rect=rect, content="text", text=text)
    s("selection.set", ids=[r(f, "id")]); s("style.paragraph.apply", name="Footer"); s("type.para", attrs={"align": al})
bar = s("frame.create", spread={"kind": "parent", "index": 0}, rect=[0, 0, 24, H], content="graphic"); s("object.fill", swatch="Brand", ids=[r(bar, "id")])
for i, (title, body) in enumerate(slides):
    t = s("frame.create", spread=i, rect=[M, M, W - M, 300], content="text", text=title)
    s("selection.set", ids=[r(t, "id")]); s("style.paragraph.apply", name="Slide Title")
    if isinstance(body, str):
        b = s("frame.create", spread=i, rect=[M, 320, W - M, 420], content="text", text=body)
        s("selection.set", ids=[r(b, "id")]); s("style.paragraph.apply", name="Subtitle")
    elif body:
        b = s("frame.create", spread=i, rect=[M, 340, W / 2, H - 160], content="text", text="\n".join("• " + x for x in body))
        s("selection.set", ids=[r(b, "id")]); s("style.paragraph.apply", name="Bullet")
    else:
        ph = s("frame.create", spread=i, rect=[M, 340, W - M, H - 120], content="graphic")
        s("file.place", path=img, frame=r(ph, "id")); s("object.fit", mode="fillProportionally", ids=[r(ph, "id")])
s("document.inspect")
open(sys.argv[1] if len(sys.argv) > 1 else "slides.dcs", "w").write("\n".join(steps) + "\n")

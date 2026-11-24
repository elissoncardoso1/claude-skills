# Workflow recipe: multi-page report (cover, contents, autoflowed body, folios), A4 facing pages.
import json, sys
W, H, M = 595.276, 841.89, {"top": 64, "bottom": 72, "inside": 60, "outside": 48}
steps = []
def s(cmd, **p):            # append a step, return its index for "$N" references
    steps.append(f"{cmd} {json.dumps(p, ensure_ascii=False)}"); return len(steps) - 1
def ref(i, path): return f"${i}.{path}"

s("file.new", preset="A4", facingPages=True, pages=3, margins=M, columns=1, title="Annual Report 2026")
# 1 styles and colours first
s("swatch.create", name="Navy", color={"c": 100, "m": 70, "y": 0, "k": 40})
s("swatch.create", name="Accent", color={"c": 0, "m": 45, "y": 100, "k": 0})
s("style.paragraph.create", name="Cover Title", chars={"fontFamily": "Source Sans 3", "fontStyle": "Bold", "size": 44, "leading": {"kind": "points", "value": 48}, "fill": "[Paper]"})
s("style.paragraph.create", name="Cover Sub", chars={"fontFamily": "Source Sans 3", "size": 16, "fill": "[Paper]"})
s("style.paragraph.create", name="H1", chars={"fontFamily": "Source Sans 3", "fontStyle": "Bold", "size": 22, "leading": {"kind": "points", "value": 26}, "fill": "Navy"}, para={"spaceBefore": 14, "spaceAfter": 8})
s("style.paragraph.create", name="Body", chars={"fontFamily": "Source Serif 4", "size": 10.5, "leading": {"kind": "points", "value": 15}}, para={"spaceAfter": 6, "align": "leftJustified"})
s("style.paragraph.create", name="Folio", chars={"fontFamily": "Source Sans 3", "size": 8, "fill": "Navy"})
# 2 parent page: folios (left page x 0..W, right page x W..2W on the parent spread)
for x0, x1, al in ((48, 200, "left"), (W + W - 200, W + W - 48, "right")):
    f = s("frame.create", spread={"kind": "parent", "index": 0}, rect=[x0, H - 50, x1, H - 36], content="text", text="\ue000")
    s("selection.set", ids=[ref(f, "id")]); s("style.paragraph.apply", name="Folio"); s("type.para", attrs={"align": al})
# 3 cover (page 1 = spread 0, right page alone at x 0..W) with full-bleed panel
s("layout.pages.applyParent", pages=[0], parent=None)
bg = s("frame.create", rect=[0, 0, W, H], content="graphic"); s("object.fill", swatch="Navy", ids=[ref(bg, "id")])
bar = s("frame.create", rect=[60, 520, 180, 528], content="graphic"); s("object.fill", swatch="Accent", ids=[ref(bar, "id")])
t = s("frame.create", rect=[60, 540, W - 48, 700], content="text", text="Annual Report 2026\nResults, people and the year ahead")
s("selection.set", ids=[ref(t, "id")]); s("style.paragraph.apply", name="Cover Sub")
s("text.select", story=ref(t, "story"), anchor=0, focus=0); s("style.paragraph.apply", name="Cover Title")
# 4 body: page 3 (spread 1, right page x W..2W); autoflow adds pages until the story fits
sections = ["Overview", "Operations", "Finance", "Outlook"]
para = "The year combined steady growth with careful investment in people and tools. " * 6
body = "\n".join(f"{h}\n" + "\n".join([para] * 4) for h in sections)
b = s("frame.create", spread=1, rect=[W + 60, 64, 2 * W - 48, H - 72], content="text", text=body)
s("selection.set", ids=[ref(b, "id")]); s("style.paragraph.apply", name="Body")
off = 0
for h in sections:   # headings are paragraph starts; offsets are UTF-8 bytes
    s("text.select", story=ref(b, "story"), anchor=off, focus=off); s("style.paragraph.apply", name="H1")
    off += len((f"{h}\n" + "\n".join([para] * 4) + "\n").encode("utf-8"))
s("layout.pages.insert", count=1)
s("text.thread", **{"from": ref(b, "id")}, spread=2, rect=[48, 64, W - 60, H - 72], autoflow=True)
# 5 contents on page 2 (spread 1, left page)
s("toc.generate", styles=["H1"], title="Contents", page=2, createBookmarks=True)
s("story.get", story=ref(b, "story"))
open(sys.argv[1] if len(sys.argv) > 1 else "report.dcs", "w").write("\n".join(steps) + "\n")

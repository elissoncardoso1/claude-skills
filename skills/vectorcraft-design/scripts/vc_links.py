#!/usr/bin/env python3
"""List external references in an SVG/SVGZ before VectorCraft opens it.

vectorcraft-cli has no read roots: an <image> pointing at a local file is read and EMBEDDED into
every export, silently (test C28). Run this on untrusted SVGs first.

Usage: vc_links.py FILE [FILE...]     exit 1 if any reference is not data: or #fragment.
       vc_links.py --strip IN OUT        write a sanitized plain-SVG copy: external hrefs -> "#",
                                         <image> elements with an external href are removed (else
                                         VectorCraft draws a 64x64 missing-link placeholder), other
                                         external hrefs -> "#", external url(...) -> none; refuses an
                                         existing OUT.
`vectorcraft-cli info` kinds is NOT a substitute: an image inside a <pattern> shows no Image kind.
An external CSS url() fill is drawn BLACK by VectorCraft (not an error).
Catches href / xlink:href with double or single quotes, and CSS url(...). Text scan, no XML parsing.
Self-test: vc_links.py --selftest
"""
import gzip, re, sys

REF = re.compile(r"""(?:xlink:)?href\s*=\s*(["'])(.*?)\1|url\(\s*(["']?)(.*?)\3\s*\)""", re.I | re.S)

def external(text):
    out = []
    for m in REF.finditer(text):
        ref = (m.group(2) if m.group(2) is not None else m.group(4) or "").strip()
        if ref and not ref.startswith("#") and not ref.lower().startswith("data:"):
            out.append(ref)
    return out

IMAGE = re.compile(r"<image\b[^>]*?(?:/>|>.*?</image\s*>)", re.I | re.S)

def strip(text):
    text = IMAGE.sub(lambda m: "" if external(m.group(0)) else m.group(0), text)
    def sub(m):
        if m.group(2) is not None:
            ref = m.group(2).strip()
            keep = not ref or ref.startswith("#") or ref.lower().startswith("data:")
            return m.group(0) if keep else m.group(0).replace(m.group(2), "#", 1)
        ref = (m.group(4) or "").strip()
        return m.group(0) if ref.startswith("#") or ref.lower().startswith("data:") else "none"
    return REF.sub(sub, text)

def read(path):
    raw = open(path, "rb").read()
    if raw[:2] == b"\x1f\x8b":
        raw = gzip.decompress(raw)
    return raw.decode("utf-8", "replace")

def selftest():
    t = """<image xlink:href="file:///etc/a.png"/><image href='../b.png'/><use href="#s"/>
           <image href="data:image/png;base64,AAA"/><rect style="fill:url(#g)"/><rect style="fill:url('/abs/c.png')"/>
           <image HREF = 'http://x/y.png'/>"""
    assert external(t) == ["file:///etc/a.png", "../b.png", "/abs/c.png", "http://x/y.png"], external(t)
    clean = strip(t)
    assert external(clean) == [], external(clean)
    assert "<image" in clean and clean.count("<image") == 1, clean   # only the data: image is kept
    assert 'href="#s"' in clean and "url(#g)" in clean and "data:image/png" in clean, clean
    print("selftest ok")

if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        selftest(); sys.exit(0)
    if sys.argv[1:2] == ["--strip"] and len(sys.argv) == 4:
        src, dst = sys.argv[2:]
        import os
        if os.path.exists(dst):
            sys.exit(f"refusing to overwrite {dst}")
        clean = strip(read(src))
        open(dst, "w").write(clean)
        left = external(clean)
        print(f"{dst}: removed {len(external(read(src)))} external reference(s); left {len(left)}")
        sys.exit(1 if left else 0)
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    bad = False
    for f in sys.argv[1:]:
        refs = external(read(f))
        bad |= bool(refs)
        print(f"{f}: " + ("no external references" if not refs else f"{len(refs)} EXTERNAL: " + ", ".join(refs)))
    sys.exit(1 if bad else 0)

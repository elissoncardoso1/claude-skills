#!/usr/bin/env python3
"""Formatos de peça estática: dimensões, zona segura e overlay-guia.

Uso:
  python formatos.py --listar
  python formatos.py reels                  # dimensões + zona segura em px
  python formatos.py feed45 --overlay guia.png   # PNG transparente com guias
  python formatos.py a3 --overlay guia.png --dpi 150

Especificações de redes: consulta às páginas oficiais em nov/2026 — reconfirme
antes de veiculação paga. Formatos impressos incluem sangria de 3 mm no overlay.
"""
import argparse

# nome: (largura, altura, unidade, descrição, zona segura: (topo, base, esq, dir) em fração ou mm)
F = {
    "feed45":   (1080, 1350, "px", "Meta Feed 4:5 (master 1440×1800 opcional)", None),
    "feed45hd": (1440, 1800, "px", "Meta Feed 4:5 master", None),
    "quadrado": (1080, 1080, "px", "Feed/carrossel 1:1", None),
    "reels":    (1080, 1920, "px", "Stories/Reels 9:16", (0.14, 0.35, 0.06, 0.06)),
    "reelshd":  (1440, 2560, "px", "Reels 9:16 master", (0.14, 0.35, 0.06, 0.06)),
    "linkedin": (1200, 627, "px", "LinkedIn imagem única 1.91:1", None),
    "thumb":    (1280, 720, "px", "YouTube thumbnail 16:9", None),
    "a6": (105, 148, "mm", "A6", 5), "a5": (148, 210, "mm", "A5", 5),
    "a4": (210, 297, "mm", "A4", 5), "a3": (297, 420, "mm", "A3", 8),
    "a2": (420, 594, "mm", "A2", 10), "a1": (594, 841, "mm", "A1", 12),
    "cartao": (90, 50, "mm", "Cartão de visita BR", 4),
    "flyer10x15": (100, 150, "mm", "Flyer 10×15", 4),
}
BLEED = 3
ALIAS = {"stories": "reels", "story": "reels", "feed": "feed45", "post": "feed45", "1x1": "quadrado",
         "youtube": "thumb", "thumbnail": "thumb", "carrossel": "feed45"}


def info(k):
    w, h, u, d, z = F[k]
    print(f"{k}: {d} — {w}×{h} {u}")
    if u == "px" and z:
        t, b, l, r = z
        print(f"  zona livre: topo {round(h*t)} px, base {round(h*b)} px, laterais {round(w*l)} px")
        print(f"  área útil: x {round(w*l)}–{w-round(w*r)}, y {round(h*t)}–{h-round(h*b)} "
              f"({w-round(w*l)-round(w*r)}×{h-round(h*t)-round(h*b)} px)")
    elif u == "px" and w != h and h > w:
        s = (h - w) // 2
        print(f"  quadrado central 1:1 (recorte de grid): y {s}–{s+w} — mantenha título e marca aqui")
    elif u == "mm":
        print(f"  com sangria: {w+2*BLEED}×{h+2*BLEED} mm; margem de segurança sugerida: {z} mm")


def overlay(k, path, dpi):
    from PIL import Image, ImageDraw
    w, h, u, d, z = F[k]
    if u == "mm":
        s = dpi / 25.4
        W, H = round((w + 2 * BLEED) * s), round((h + 2 * BLEED) * s)
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        dr = ImageDraw.Draw(im)
        b = round(BLEED * s)
        dr.rectangle([b, b, W - b, H - b], outline=(255, 0, 0, 255), width=2)  # corte
        m = round((BLEED + z) * s)
        dr.rectangle([m, m, W - m, H - m], outline=(0, 160, 255, 255), width=2)  # segurança
    else:
        im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        dr = ImageDraw.Draw(im)
        if z:
            t, bb, l, r = z
            dr.rectangle([0, 0, w, round(h * t)], fill=(255, 0, 0, 70))
            dr.rectangle([0, h - round(h * bb), w, h], fill=(255, 0, 0, 70))
            dr.rectangle([0, 0, round(w * l), h], fill=(255, 0, 0, 50))
            dr.rectangle([w - round(w * r), 0, w, h], fill=(255, 0, 0, 50))
        elif h > w:
            s = (h - w) // 2
            dr.rectangle([0, s, w - 1, s + w], outline=(0, 160, 255, 255), width=3)
        for i in (1, 2):  # terços apenas como referência
            dr.line([(w * i // 3, 0), (w * i // 3, h)], fill=(255, 255, 255, 60), width=1)
            dr.line([(0, h * i // 3), (w, h * i // 3)], fill=(255, 255, 255, 60), width=1)
    im.save(path)
    print(f"overlay salvo em {path}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("formato", nargs="?")
    ap.add_argument("--listar", action="store_true")
    ap.add_argument("--overlay")
    ap.add_argument("--dpi", type=int, default=150)
    a = ap.parse_args()
    if a.listar or not a.formato:
        for k in F:
            info(k)
        return
    k = ALIAS.get(a.formato.lower(), a.formato.lower())
    if k not in F:
        raise SystemExit(f"Formato desconhecido: {a.formato}. Use --listar.")
    info(k)
    if a.overlay:
        overlay(k, a.overlay, a.dpi)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Razão de contraste (fórmula WCAG 2.x) entre pares de cores + teste de valor.

WCAG 1.4.3 é norma de conteúdo web; aqui é usada como META transferível para
peças estáticas: 4,5:1 texto normal, 3:1 texto grande (≥ ~24 px ou ~19 px negrito
em tela; em impresso, use como referência mínima, não garantia).

Uso:
  python contraste.py "#1A1A1A" "#F2E8D5"
  python contraste.py "#FFFFFF" "#E63946" "#1D3557"   # todos os pares
  python contraste.py --paleta "#0B132B,#1C2541,#3A506B,#5BC0BE,#FFFFFF"
A saída inclui a luminância (L*) aproximada de cada cor para o teste em escala
de cinza: diferenças de L* < ~20 entre texto e fundo tendem a falhar na leitura.
"""
import itertools
import sys


def hex2rgb(h):
    h = h.strip().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def lin(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def rel_lum(rgb):
    r, g, b = (lin(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def lstar(Y):
    f = Y ** (1 / 3) if Y > 216 / 24389 else (24389 / 27 * Y + 16) / 116
    return 116 * f - 16


def ratio(a, b):
    la, lb = rel_lum(hex2rgb(a)), rel_lum(hex2rgb(b))
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def veredito(r):
    if r >= 7:
        return "AAA texto normal"
    if r >= 4.5:
        return "AA texto normal"
    if r >= 3:
        return "só texto grande / elementos gráficos"
    return "FALHA para texto"


def main(args):
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return
    if args[0] == "--paleta":
        cores = [c for c in args[1].split(",") if c]
    else:
        cores = args
    print("Cor       L*")
    for c in cores:
        print(f"{c:9} {lstar(rel_lum(hex2rgb(c))):5.1f}")
    print()
    for a, b in itertools.combinations(cores, 2):
        r = ratio(a, b)
        dl = abs(lstar(rel_lum(hex2rgb(a))) - lstar(rel_lum(hex2rgb(b))))
        print(f"{a} × {b}: {r:5.2f}:1  ΔL*={dl:4.1f}  → {veredito(r)}")


if __name__ == "__main__":
    main(sys.argv[1:])

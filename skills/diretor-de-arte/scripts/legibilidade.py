#!/usr/bin/env python3
"""Dimensiona letra pela distância de leitura (Legge & Bigelow, 2011).

Base: leitura fluente quando a altura-x subtende entre ~0,2° (tamanho crítico)
e ~2° de ângulo visual. Abaixo de 0,2° a velocidade cai bruscamente.

Uso:
  python legibilidade.py 3m                 # distância → altura-x e corpo mínimos
  python legibilidade.py 3m --xh 0.48       # razão altura-x/corpo da fonte escolhida
  python legibilidade.py 3m --margem 2      # fator de segurança (idosos, baixa luz)
  python legibilidade.py --tabela           # tabela de distâncias usuais
  python legibilidade.py --tela 1080 --largura-mm 68 --dist 35cm
        # post de 1080 px visto num celular com tela de 68 mm de largura a 35 cm

Saída em mm e pt (1 pt = 0,3528 mm). A conversão para corpo assume razão
altura-x/corpo (padrão 0,5; fontes reais vão de ~0,28 a ~0,58 — confira a sua).
"""
import argparse
import math
import re

PT_MM = 25.4 / 72


def parse_dist(s: str) -> float:
    """Retorna distância em mm."""
    m = re.fullmatch(r"\s*([\d.,]+)\s*(mm|cm|m)?\s*", s)
    if not m:
        raise SystemExit(f"Distância inválida: {s}")
    v = float(m.group(1).replace(",", "."))
    unit = m.group(2) or "m"
    return v * {"mm": 1, "cm": 10, "m": 1000}[unit]


def xh_for_angle(dist_mm: float, deg: float) -> float:
    return 2 * dist_mm * math.tan(math.radians(deg) / 2)


def linha(dist_mm, xh_ratio, margem):
    crit = xh_for_angle(dist_mm, 0.2)
    alvo = crit * margem
    teto = xh_for_angle(dist_mm, 2.0)
    corpo_pt = alvo / xh_ratio / PT_MM
    return crit, alvo, teto, corpo_pt


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dist", nargs="?")
    ap.add_argument("--xh", type=float, default=0.5, help="razão altura-x/corpo")
    ap.add_argument("--margem", type=float, default=1.0, help="fator sobre o tamanho crítico")
    ap.add_argument("--tabela", action="store_true")
    ap.add_argument("--tela", type=int, help="largura da arte em px")
    ap.add_argument("--largura-mm", type=float, help="largura física exibida em mm")
    a = ap.parse_args()

    if a.tela:
        if not (a.largura_mm and a.dist):
            raise SystemExit("--tela exige --largura-mm e distância (ex.: --dist 35cm via posicional)")
        d = parse_dist(a.dist)
        px_per_mm = a.tela / a.largura_mm
        crit, alvo, teto, _ = linha(d, a.xh, a.margem)
        print(f"Arte de {a.tela}px exibida com {a.largura_mm} mm a {d/10:.0f} cm:")
        print(f"  altura-x crítica ≈ {crit*px_per_mm:.0f} px  → corpo ≈ {crit*px_per_mm/a.xh:.0f} px")
        print(f"  altura-x alvo (×{a.margem}) ≈ {alvo*px_per_mm:.0f} px → corpo ≈ {alvo*px_per_mm/a.xh:.0f} px")
        print(f"  acima de ≈ {teto*px_per_mm/a.xh:.0f} px de corpo a leitura não acelera (impacto = peso/contraste)")
        return

    if a.tabela or not a.dist:
        print(f"razão altura-x/corpo = {a.xh}; margem ×{a.margem}")
        print(f"{'distância':>10} | {'x crít. mm':>10} | {'x alvo mm':>9} | {'corpo pt':>8} | {'corpo mm':>8} | {'x 2° mm':>8}")
        for s in ["40cm", "1m", "2m", "3m", "5m", "10m", "20m"]:
            d = parse_dist(s)
            crit, alvo, teto, pt = linha(d, a.xh, a.margem)
            print(f"{s:>10} | {crit:10.1f} | {alvo:9.1f} | {pt:8.0f} | {pt*PT_MM:8.1f} | {teto:8.0f}")
        print("Recomendação: texto essencial com margem ≥2 (público idoso, baixa luz, leitura em movimento).")
        return

    d = parse_dist(a.dist)
    crit, alvo, teto, pt = linha(d, a.xh, a.margem)
    print(f"Distância {d/1000:.2f} m")
    print(f"  altura-x crítica (0,2°): {crit:.1f} mm")
    print(f"  altura-x alvo (×{a.margem}): {alvo:.1f} mm → corpo ≈ {pt:.0f} pt ({pt*PT_MM:.1f} mm) com razão {a.xh}")
    print(f"  teto da faixa fluente (2°): altura-x {teto:.0f} mm — acima disso, ganhe impacto com peso/contraste")


if __name__ == "__main__":
    main()

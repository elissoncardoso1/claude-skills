#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
diagnostico.py — diagnóstico heurístico de roteiro em texto/Fountain/Markdown.

Uso:
    python3 scripts/diagnostico.py roteiro.fountain
    python3 scripts/diagnostico.py roteiro.txt --formato longa -o relatorio.md
    python3 scripts/diagnostico.py roteiro.md --formato serie

Não substitui leitura humana. Mede o que é mensurável (cenas, páginas, fala,
personagens, distribuição de atos) e sinaliza padrões suspeitos.
"""

import argparse
import os
import re
import sys
import unicodedata
from collections import Counter, defaultdict

PAGE_LINES = 55  # linhas por página em roteiro formatado

SCENE_RE = re.compile(
    r"^(?:\d+[\.\)]\s*)?(INT\.?|EXT\.?|INT\.?/EXT\.?|I/E\.?|INTERIOR|EXTERIOR)\b",
    re.IGNORECASE,
)
CENA_RE = re.compile(r"^CENA\s*\d+\s*[\.\-–—:]\s*", re.IGNORECASE)
MD_SCENE_RE = re.compile(r"^#{1,6}\s*(CENA\b.*|INT\b.*|EXT\b.*)$", re.IGNORECASE)
TRANSITIONS = (
    "corta para",
    "corte para",
    "corta rápido para",
    "funde com",
    "fade in",
    "fade out",
    "freeze",
    "congela",
    "cut to",
    "fade to",
    "match cut",
)
TIME_WORDS = (
    "dia",
    "noite",
    "manhã",
    "manha",
    "tarde",
    "amanhecer",
    "anoitecer",
    "entardecer",
    "day",
    "night",
    "morning",
    "evening",
    "continuous",
    "contínuo",
    "continuo",
)
CAMERA_WORDS = (
    "câmera",
    "camera",
    "close",
    "close-up",
    "close up",
    "travelling",
    "pan",
    "zoom",
    "plano ",
    "plano-",
    "enquadramento",
    "ângulo",
    "angulo",
    "contra-plano",
    "contraplano",
)


def strip_accents(s: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn"
    )


def is_upper_line(s: str) -> bool:
    letters = [c for c in s if c.isalpha()]
    if not letters:
        return False
    # compara apenas letras, ignorando acentos e pontuação
    return all(c.isupper() for c in letters)


def split_heading(heading: str):
    """Retorna (local, tempo) a partir de um cabeçalho."""
    h = heading.strip()
    h = re.sub(r"^#{1,6}\s*", "", h)
    is_cena_style = bool(re.match(r"^CENA\s*\d+", h, re.IGNORECASE))
    h = re.sub(r"^CENA\s*\d+\s*[\.\-–—:]\s*", "", h, flags=re.IGNORECASE)
    if is_cena_style:
        # padrão brasileiro: CENA 28. RUA DO CENTRO. EXTERIOR. DIA.
        parts = [p.strip() for p in re.split(r"[\.;]", h) if p.strip()]
    else:
        parts = re.split(r"\s+[-–—]\s+", h)
    loc = parts[0] if parts else h
    loc = re.sub(r"^(INT\.?/EXT\.?|I/E\.?|INT\.?|EXT\.?|INTERIOR|EXTERIOR)\s*[\.\-–—:]?\s*", "", loc, flags=re.IGNORECASE)
    time = ""
    for p in parts[1:] + [h]:
        low = strip_accents(p.lower())
        for w in TIME_WORDS:
            if re.search(r"\b" + re.escape(strip_accents(w)) + r"\b", low):
                time = w
                break
        if time:
            break
    return loc.strip(), time


class Script:
    def __init__(self, text: str):
        self.raw = text
        self.lines = text.splitlines()
        self.scenes = []          # dicts: index, heading, loc, time, start, end
        self.characters = Counter()
        self.character_words = Counter()
        self.dialogue_lines = 0
        self.action_lines = 0
        self.parentheticals = 0
        self.transitions = 0
        self.camera_flags = []
        self.we_see_flags = []
        self.page_breaks = text.count("\f")
        self._parse()

    def _is_scene(self, line: str):
        s = line.strip()
        if not s:
            return False
        if SCENE_RE.match(s) or CENA_RE.match(s) or MD_SCENE_RE.match(s):
            return True
        return False

    def _parse(self):
        current = None
        i = 0
        n = len(self.lines)
        first_content = None
        last_content = None
        while i < n:
            raw = self.lines[i]
            line = raw.strip()
            if line and first_content is None:
                first_content = i
            if line:
                last_content = i

            if self._is_scene(line):
                if current is not None:
                    current["end"] = i
                loc, tm = split_heading(line)
                current = {
                    "index": len(self.scenes) + 1,
                    "heading": line,
                    "loc": loc,
                    "time": tm,
                    "start": i,
                    "end": i,
                }
                self.scenes.append(current)
                i += 1
                continue

            low = strip_accents(line.lower())
            if any(low.startswith(t) for t in TRANSITIONS):
                self.transitions += 1
                i += 1
                continue

            # Cue de personagem: linha em maiúsculas, curta, seguida de fala
            if (
                line
                and len(line) <= 40
                and is_upper_line(line)
                and not line.startswith("(")
                and not line.endswith(":")
                and not self._is_scene(line)
                and i + 1 < n
                and self.lines[i + 1].strip()
                and not self._is_scene(self.lines[i + 1].strip())
            ):
                name = re.sub(r"\s*\(.*?\)\s*", "", line).strip()
                if name and len(name) >= 2 and not any(
                    strip_accents(name.lower()).startswith(t) for t in TRANSITIONS
                ):
                    self.characters[name] += 1
                    j = i + 1
                    while j < n and self.lines[j].strip():
                        d = self.lines[j].strip()
                        if d.startswith("(") and d.endswith(")"):
                            self.parentheticals += 1
                        else:
                            self.dialogue_lines += 1
                            self.character_words[name] += len(d.split())
                        j += 1
                    i = j
                    continue

            if line:
                self.action_lines += 1
                if any(w in low for w in CAMERA_WORDS):
                    self.camera_flags.append((i + 1, line))
                if re.search(r"\bnós vemos\b|\bvemos que\b|\bwe see\b", low):
                    self.we_see_flags.append((i + 1, line))
            i += 1

        if current is not None:
            current["end"] = n

        if first_content is not None and last_content is not None:
            self.physical_lines = max(1, last_content - first_content + 1)
        else:
            self.physical_lines = 0

    # ----- métricas -----
    @property
    def total_lines(self):
        return self.action_lines + self.dialogue_lines

    @property
    def pages(self):
        if self.page_breaks:
            return round(self.page_breaks + 1, 1)
        return round(self.physical_lines / PAGE_LINES, 1) if self.physical_lines else 0.0

    def scene_pages(self, sc):
        length = max(1, sc["end"] - sc["start"])
        return round(length / PAGE_LINES, 2)

    def act_of(self, page, formato):
        if formato == "serie":
            marks = (18, 30, 45, 60)
            for idx, m in enumerate(marks, start=1):
                if page <= m:
                    return idx
            return 5
        marks = (25, 55, 85)
        for idx, m in enumerate(marks, start=1):
            if page <= m:
                return idx
        return 4

    def distribution(self, formato):
        counts = Counter()
        pages = defaultdict(float)
        for sc in self.scenes:
            p = self.scene_pages(sc)
            # posição aproximada: páginas acumuladas antes da cena + metade
            before = sum(self.scene_pages(x) for x in self.scenes[: sc["index"] - 1])
            act = self.act_of(before + p / 2, formato)
            counts[act] += 1
            pages[act] += p
        return counts, pages


def diagnose(path, formato):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    sc = Script(text)
    out = []
    add = out.append

    nome = os.path.basename(path)
    add(f"# Diagnóstico de roteiro — `{nome}`\n")
    add(f"**Formato considerado:** {formato} · **Páginas estimadas:** {sc.pages} · "
        f"**Cenas:** {len(sc.scenes)} · **Linhas de texto:** {sc.total_lines}\n")

    if not sc.scenes:
        add("> **Alerta alto:** nenhum cabeçalho de cena reconhecido. "
            "Se o arquivo for um tratamento, uma escaleta ou um texto em prosa, "
            "este diagnóstico não se aplica. Se for roteiro, use `INT.`/`EXT.` "
            "ou `CENA n.` no início das cenas.\n")
        return "\n".join(out)

    # Tabela-resumo
    add("## Resumo\n")
    add("| Métrica | Valor |")
    add("|---|---|")
    add(f"| Cenas | {len(sc.scenes)} |")
    add(f"| Páginas estimadas | {sc.pages} |")
    add(f"| Diálogo | {sc.dialogue_lines} linhas ({pct(sc.dialogue_lines, sc.total_lines)}%) |")
    add(f"| Ação | {sc.action_lines} linhas ({pct(sc.action_lines, sc.total_lines)}%) |")
    add(f"| Parênteses | {sc.parentheticals} |")
    add(f"| Transições | {sc.transitions} |")
    add(f"| Personagens falantes | {len(sc.characters)} |")
    add(f"| Locais distintos | {len(set(s['loc'] for s in sc.scenes))} |")
    add("")

    # Distribuição por ato
    counts, pages = sc.distribution(formato)
    add("## Distribuição por ato (aproximada)\n")
    add("| Ato | Cenas | Páginas | % do roteiro |")
    add("|---|---|---|---|")
    total_pages = sum(pages.values()) or 1
    for a in sorted(counts):
        add(f"| {a} | {counts[a]} | {pages[a]:.1f} | {pages[a]/total_pages*100:.0f}% |")
    add("")

    # Personagens
    add("## Personagens por volume de fala\n")
    add("| Personagem | Falas | Palavras | % das falas |")
    add("|---|---|---|---|")
    total_dial = sum(sc.characters.values()) or 1
    for name, count in sc.characters.most_common(15):
        add(f"| {name} | {count} | {sc.character_words[name]} | {count/total_dial*100:.0f}% |")
    add("")

    # Cenas mais longas
    longs = sorted(sc.scenes, key=lambda s: sc.scene_pages(s), reverse=True)[:8]
    add("## Cenas mais longas\n")
    add("| # | Cena | Páginas |")
    add("|---|---|---|")
    for s in longs:
        add(f"| {s['index']} | {s['heading'][:70]} | {sc.scene_pages(s)} |")
    add("")

    # Alertas
    alerts = []
    if sc.pages > 0:
        if formato == "longa" and not (80 <= sc.pages <= 140):
            alerts.append(("médio", f"Páginas estimadas ({sc.pages}) fora da faixa usual de longa (80–140)."))
        if formato == "curta" and sc.pages > 30:
            alerts.append(("médio", f"Curta com {sc.pages} páginas: verifique se não é um longa comprimido."))
        if formato == "serie" and not (25 <= sc.pages <= 70):
            alerts.append(("médio", f"Episódio com {sc.pages} páginas: confira a grade de atos e a duração."))

    if sc.total_lines:
        dp = sc.dialogue_lines / sc.total_lines
        if dp > 0.65:
            alerts.append(("médio", f"Diálogo ocupa {dp*100:.0f}% do texto: risco de roteiro 'falado'. Verifique se a imagem conta a história."))
        if dp < 0.15:
            alerts.append(("baixo", f"Diálogo ocupa só {dp*100:.0f}%: verifique se há informação dramática suficiente em cena."))

    if sc.characters:
        top, topn = sc.characters.most_common(1)[0]
        if len(sc.characters) >= 3 and topn / total_dial > 0.55:
            alerts.append(("médio", f"{top} concentra {topn/total_dial*100:.0f}% das falas: risco de monólogo ou protagonismo sem contraponto."))
        one_liners = [n for n, c in sc.characters.items() if c == 1]
        if len(one_liners) >= 3:
            alerts.append(("baixo", f"{len(one_liners)} personagens falam uma única vez: verifique se são funcionais ou decorativos."))

    long_scenes = [s for s in sc.scenes if sc.scene_pages(s) > 4]
    if long_scenes:
        alerts.append(("médio", f"{len(long_scenes)} cena(s) com mais de 4 páginas. Considere dividir ou cortar."))

    missing_time = [s for s in sc.scenes if not s["time"]]
    if missing_time:
        alerts.append(("médio", f"{len(missing_time)} cena(s) sem indicação de tempo (DIA/NOITE)."))

    repeat_locs = Counter(s["loc"] for s in sc.scenes)
    top_loc, top_loc_n = repeat_locs.most_common(1)[0]
    if top_loc_n > max(6, len(sc.scenes) * 0.4):
        alerts.append(("baixo", f"O local '{top_loc}' aparece em {top_loc_n} cenas: risco de monotonia visual ou de economia de produção (pode ser intencional)."))

    if sc.parentheticals and sc.dialogue_lines:
        if sc.parentheticals / sc.dialogue_lines > 0.10:
            alerts.append(("baixo", f"{sc.parentheticals} parênteses para {sc.dialogue_lines} falas: use só quando a fala for ambígua."))

    if sc.camera_flags:
        alerts.append(("médio", f"{len(sc.camera_flags)} linha(s) com linguagem de câmera. O roteirista não dirige; escreva o que se vê, não o plano."))
    if sc.we_see_flags:
        alerts.append(("baixo", f"{len(sc.we_see_flags)} ocorrência(s) de 'nós vemos'/'vemos que'. Prefira a ação direta."))

    # Checagem de atos vazios
    if formato in ("longa", "serie"):
        expected = 4 if formato == "longa" else 5
        for a in range(1, expected + 1):
            if counts.get(a, 0) == 0:
                alerts.append(("alto", f"Nenhuma cena no ato {a}: a divisão de atos pode estar desbalanceada ou o midpoint ausente."))

    if not alerts:
        alerts.append(("baixo", "Nenhum padrão suspeito detectado pelas heurísticas. Isso não significa que o roteiro está bom — significa que os números não gritam."))

    add("## Alertas\n")
    ordem = {"alto": 0, "médio": 1, "baixo": 2}
    for level, msg in sorted(alerts, key=lambda x: ordem.get(x[0], 3)):
        icon = {"alto": "🔴", "médio": "🟠", "baixo": "🟡"}[level]
        add(f"- {icon} **{level.capitalize()}:** {msg}")
    add("")

    add("## Limites deste diagnóstico\n")
    add("- Heurístico: não entende ironia, subtexto, gênero nem intenção. "
        "Um número estranho pode ser uma escolha deliberada.")
    add("- A contagem de páginas é estimada por linhas (55/página) ou por quebras de página do arquivo.")
    add("- Cabeçalhos, cues e diálogos são reconhecidos por padrão; formatação fora do padrão pode gerar falsos positivos.")
    add("- Use o relatório como ponto de partida para a leitura, nunca como veredito.\n")

    return "\n".join(out)


def pct(a, b):
    return round(a / b * 100) if b else 0


def main():
    ap = argparse.ArgumentParser(description="Diagnóstico heurístico de roteiro.")
    ap.add_argument("arquivo", help="arquivo .fountain, .txt ou .md")
    ap.add_argument("--formato", choices=["longa", "curta", "serie", "auto"], default="auto")
    ap.add_argument("-o", "--output", help="salvar relatório em Markdown")
    args = ap.parse_args()

    if not os.path.exists(args.arquivo):
        sys.stderr.write(f"Arquivo não encontrado: {args.arquivo}\n")
        sys.exit(1)

    formato = args.formato
    if formato == "auto":
        with open(args.arquivo, "r", encoding="utf-8", errors="ignore") as f:
            head = f.read(4000).lower()
        if "série" in head or "serie" in head or "episódio" in head or "episodio" in head:
            formato = "serie"
        elif "curta" in head:
            formato = "curta"
        else:
            formato = "longa"

    report = diagnose(args.arquivo, formato)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"Relatório salvo em {args.output}")
    else:
        print(report)


if __name__ == "__main__":
    main()

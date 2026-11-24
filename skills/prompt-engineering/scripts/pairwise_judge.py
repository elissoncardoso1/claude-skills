#!/usr/bin/env python3
"""Juiz LLM pareado com controle de viés de posição (Zheng et al., MT-Bench).

Avalia A vs B nas duas ordens. Uma resposta só vence se vencer nas duas; caso contrário, EMPATE.

Uso (um par):
    python pairwise_judge.py --task tarefa.txt --a saida_a.txt --b saida_b.txt \
        --criteria "fidelidade à fonte; completude; clareza" --provider anthropic --model <modelo>

Uso (lote JSONL com campos task, a, b e opcionais reference, id):
    python pairwise_judge.py --batch pares.jsonl --criteria "..." --provider openai --model <modelo>

Sem chave de API, use --provider mock para testar o fluxo.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from llm_client import complete  # noqa: E402

JUDGE = """Compare duas respostas à mesma tarefa. A ordem de apresentação é aleatória e não indica qualidade. Não favoreça a resposta mais longa nem a mais confiante; avalie apenas os critérios.

<tarefa>
{task}
</tarefa>
{ref_block}
<resposta_1>
{first}
</resposta_1>

<resposta_2>
{second}
</resposta_2>

<criterios>
{criteria}
</criterios>

{ref_instr}Analise cada critério em <analise>, citando trechos das respostas. Depois escreva em <veredito> exatamente uma palavra: 1, 2 ou EMPATE.
"""


def verdict(text: str) -> str:
    m = re.search(r"<veredito>\s*(1|2|EMPATE)\s*</veredito>", text, re.I)
    if not m:
        m = re.search(r"\b(1|2|EMPATE)\b\s*$", text.strip(), re.I)
    return m.group(1).upper() if m else "INVALIDO"


def judge_pair(task, a, b, criteria, provider, model, reference=None, temperature=0.0):
    ref_block = f"\n<referencia>\n{reference}\n</referencia>\n" if reference else ""
    ref_instr = ("Use a referência como resposta correta para verificar fatos e resultados. " if reference
                 else "Se a tarefa tiver resposta verificável, resolva-a você mesmo antes de comparar. ")
    out = {}
    for order, (x, y) in {"AB": (a, b), "BA": (b, a)}.items():
        prompt = JUDGE.format(task=task, first=x, second=y, criteria=criteria, ref_block=ref_block, ref_instr=ref_instr)
        raw = complete(provider, model, prompt, temperature=temperature)
        v = verdict(raw)
        # traduz 1/2 de volta para A/B
        if v == "1":
            v = "A" if order == "AB" else "B"
        elif v == "2":
            v = "B" if order == "AB" else "A"
        out[order] = {"verdict": v, "raw": raw}
    v1, v2 = out["AB"]["verdict"], out["BA"]["verdict"]
    final = v1 if v1 == v2 and v1 in {"A", "B"} else ("EMPATE" if "INVALIDO" not in (v1, v2) else "INVALIDO")
    return {"final": final, "consistent": v1 == v2, "AB": v1, "BA": v2, "raw": out}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--task", type=Path)
    ap.add_argument("--a", type=Path)
    ap.add_argument("--b", type=Path)
    ap.add_argument("--reference", type=Path)
    ap.add_argument("--batch", type=Path)
    ap.add_argument("--criteria", required=True)
    ap.add_argument("--provider", default="mock")
    ap.add_argument("--model", default="mock")
    ap.add_argument("--out", type=Path)
    a = ap.parse_args()

    if a.batch:
        rows = [json.loads(l) for l in a.batch.read_text(encoding="utf-8").splitlines() if l.strip()]
    elif a.task and a.a and a.b:
        rows = [{"id": "par-1", "task": a.task.read_text(encoding="utf-8"), "a": a.a.read_text(encoding="utf-8"),
                 "b": a.b.read_text(encoding="utf-8"),
                 "reference": a.reference.read_text(encoding="utf-8") if a.reference else None}]
    else:
        ap.error("Informe --batch ou --task/--a/--b")

    results = []
    for i, r in enumerate(rows):
        res = judge_pair(r["task"], r["a"], r["b"], a.criteria, a.provider, a.model, r.get("reference"))
        res["id"] = r.get("id", i)
        results.append(res)
        print(f"{res['id']}: {res['final']}  (AB={res['AB']}, BA={res['BA']}, consistente={res['consistent']})")

    c = Counter(r["final"] for r in results)
    n = len(results)
    print(f"\nA: {c['A']}/{n} · B: {c['B']}/{n} · Empates: {c['EMPATE']}/{n} · Inválidos: {c['INVALIDO']}/{n}")
    print(f"Consistência entre ordens: {sum(r['consistent'] for r in results)}/{n}")
    if a.out:
        a.out.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

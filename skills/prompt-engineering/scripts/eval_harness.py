#!/usr/bin/env python3
"""Harness simples para comparar variantes de prompt num dataset com graders.

Entradas
--------
--variants   um ou mais arquivos de template. Cada arquivo pode ter um bloco de system opcional:
                 ---system---
                 texto do system prompt
                 ---user---
                 texto do prompt de usuário com {{variaveis}}
             Sem marcadores, o arquivo inteiro é o prompt de usuário.
--dataset    JSONL; cada linha é um objeto com as variáveis do template e campos de referência.
--graders    JSON com lista de graders, ex.:
             [
               {"name": "rotulo_correto", "type": "exact", "field": "esperado", "normalize": true},
               {"name": "contem_fonte", "type": "contains", "value": "[1]"},
               {"name": "formato_data", "type": "regex", "pattern": "\\d{4}-\\d{2}-\\d{2}"},
               {"name": "json_ok", "type": "json_keys", "keys": ["categoria", "valor"]},
               {"name": "curto", "type": "max_words", "value": 80},
               {"name": "custom", "type": "python", "path": "meus_graders.py:verifica"}
             ]
             Grader python: função f(output: str, row: dict) -> bool | float (0..1).
--provider   anthropic | openai | gemini | mock     --model  nome do modelo
--runs       repetições por caso (útil com temperatura > 0)

Saídas: <out>/results.json e <out>/report.md (média por variante e grader, falhas de exemplo).

Exemplo offline:
    python eval_harness.py --variants v1.txt v2.txt --dataset casos.jsonl --graders graders.json --provider mock
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import statistics
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from llm_client import complete  # noqa: E402

VAR = re.compile(r"\{\{\s*([a-zA-Z_][\w]*)\s*\}\}")


def load_variant(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8")
    system, user = None, raw
    if "---user---" in raw:
        head, user = raw.split("---user---", 1)
        if "---system---" in head:
            system = head.split("---system---", 1)[1].strip()
    return {"name": path.stem, "system": system, "user": user.strip()}


def render(tpl: str | None, row: dict) -> str | None:
    if tpl is None:
        return None

    def sub(m):
        k = m.group(1)
        if k not in row:
            raise KeyError(f"Variável '{k}' ausente na linha do dataset: {list(row)}")
        v = row[k]
        return v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)

    return VAR.sub(sub, tpl)


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip().lower().strip(".:;!\"'`"))


def _extract_json(s: str):
    s2 = s.strip()
    fence = re.search(r"```(?:json)?\s*(.*?)```", s2, re.S)
    if fence:
        s2 = fence.group(1)
    start = min([i for i in (s2.find("{"), s2.find("[")) if i >= 0], default=-1)
    if start < 0:
        raise ValueError("sem JSON")
    return json.loads(s2[start:])


def make_grader(cfg: dict):
    t = cfg["type"]
    if t == "exact":
        field, norm = cfg["field"], cfg.get("normalize", True)
        return lambda out, row: (_norm(out) == _norm(str(row[field]))) if norm else out.strip() == str(row[field]).strip()
    if t == "contains":
        return lambda out, row: (str(row[cfg["field"]]) if "field" in cfg else cfg["value"]).lower() in out.lower()
    if t == "not_contains":
        return lambda out, row: cfg["value"].lower() not in out.lower()
    if t == "regex":
        rx = re.compile(cfg["pattern"], re.S)
        return lambda out, row: bool(rx.search(out))
    if t == "max_words":
        return lambda out, row: len(out.split()) <= int(cfg["value"])
    if t == "json_keys":
        keys = cfg.get("keys", [])

        def g(out, row):
            try:
                obj = _extract_json(out)
            except Exception:
                return False
            return isinstance(obj, dict) and all(k in obj for k in keys)
        return g
    if t == "json_field_equals":
        def g(out, row):
            try:
                return _norm(str(_extract_json(out).get(cfg["key"]))) == _norm(str(row[cfg["field"]]))
            except Exception:
                return False
        return g
    if t == "python":
        file, func = cfg["path"].rsplit(":", 1)
        spec = importlib.util.spec_from_file_location("custom_graders", file)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)  # type: ignore
        return getattr(mod, func)
    raise ValueError(f"Tipo de grader desconhecido: {t}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--variants", nargs="+", required=True, type=Path)
    ap.add_argument("--dataset", required=True, type=Path)
    ap.add_argument("--graders", required=True, type=Path)
    ap.add_argument("--provider", default="mock")
    ap.add_argument("--model", default="mock")
    ap.add_argument("--temperature", type=float, default=None)
    ap.add_argument("--max-tokens", type=int, default=4096)
    ap.add_argument("--runs", type=int, default=1)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--out", type=Path, default=Path("eval_out"))
    a = ap.parse_args()

    variants = [load_variant(p) for p in a.variants]
    rows = [json.loads(l) for l in a.dataset.read_text(encoding="utf-8").splitlines() if l.strip()]
    gcfgs = json.loads(a.graders.read_text(encoding="utf-8"))
    graders = [(c["name"], make_grader(c)) for c in gcfgs]

    jobs = [(v, i, r, k) for v in variants for i, r in enumerate(rows) for k in range(a.runs)]

    def run(job):
        v, i, row, k = job
        t0 = time.time()
        try:
            out = complete(a.provider, a.model, render(v["user"], row), render(v["system"], row),
                           a.temperature, a.max_tokens)
            err = None
        except Exception as e:
            out, err = "", str(e)
        scores = {}
        for name, g in graders:
            try:
                s = g(out, row)
                scores[name] = float(s)
            except Exception as e:
                scores[name] = 0.0
                err = (err or "") + f" | grader {name}: {e}"
        return {"variant": v["name"], "case": row.get("id", i), "run": k, "output": out, "scores": scores,
                "seconds": round(time.time() - t0, 2), "error": err}

    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        results = list(ex.map(run, jobs))

    a.out.mkdir(parents=True, exist_ok=True)
    (a.out / "results.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")

    names = [n for n, _ in graders]
    md = [f"# Relatório de avaliação\n", f"Provedor: `{a.provider}` · Modelo: `{a.model}` · Casos: {len(rows)} · Runs: {a.runs}\n",
          "| Variante | " + " | ".join(names) + " | Média geral | Erros |", "|---" * (len(names) + 3) + "|"]
    summary = {}
    for v in variants:
        rs = [r for r in results if r["variant"] == v["name"]]
        per = {n: statistics.mean(r["scores"][n] for r in rs) for n in names}
        overall = statistics.mean(per.values()) if per else 0
        errs = sum(1 for r in rs if r["error"])
        summary[v["name"]] = {"per_grader": per, "overall": overall, "errors": errs}
        md.append(f"| {v['name']} | " + " | ".join(f"{per[n]:.2f}" for n in names) + f" | **{overall:.2f}** | {errs} |")

    md.append("\n## Falhas (até 3 por variante)\n")
    for v in variants:
        fails = [r for r in results if r["variant"] == v["name"] and min(r["scores"].values(), default=1) < 1][:3]
        if not fails:
            continue
        md.append(f"### {v['name']}")
        for r in fails:
            bad = [n for n, s in r["scores"].items() if s < 1]
            md.append(f"- caso `{r['case']}` (run {r['run']}) falhou em {', '.join(bad)}:\n  ```\n  {r['output'][:400]}\n  ```")
    (a.out / "report.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md[:len(variants) + 4]))
    print(f"\nRelatório: {a.out / 'report.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Checagem estática de prompts — encontra sinais comuns de problema antes de gastar tokens.

Não substitui avaliação: aponta suspeitas para revisão humana/LLM.

Uso:
    python prompt_lint.py prompt.md
    python prompt_lint.py prompt.md --json
    cat prompt.txt | python prompt_lint.py -
    python prompt_lint.py system.md --role system   # checagens extras para system prompt
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass

SHOUT_WORDS = {
    "MUST", "NEVER", "ALWAYS", "CRITICAL", "IMPORTANT", "DO NOT", "DON'T", "ABSOLUTELY",
    "NUNCA", "SEMPRE", "DEVE", "OBRIGATÓRIO", "OBRIGATORIO", "IMPORTANTE", "CRÍTICO", "CRITICO", "JAMAIS", "PROIBIDO",
}
NEGATIVE_START = re.compile(r"^\s*(?:[-*\d.)]+\s*)?(não|nao|nunca|jamais|evite|don't|do not|never|avoid)\b", re.I)
FORMAT_HINTS = re.compile(
    r"(formato|format|output|saída|saida|responda|responder|retorne|return|json|schema|tabela|table|lista|list|"
    r"parágrafo|paragrafo|paragraph|palavras|words|frases|sentences|markdown|<resposta>|<answer>)",
    re.I,
)
EMOTIONAL = re.compile(
    r"(minha carreira|my career|take a deep breath|respire fundo|i will tip|vou te dar uma gorjeta|gorjeta|"
    r"\$\d+ tip|you'?d better be sure|é muito importante para mim|this is very important to my|"
    r"pessoas vão morrer|people will die|or you will be (?:fired|punished))",
    re.I,
)
VAGUE = re.compile(r"\b(curto|curta|breve|alguns|algumas|poucos|poucas|short|brief|some|a few|concise|conciso|concisa)\b", re.I)
NUMBER_NEAR = re.compile(r"\d")
PLACEHOLDER = re.compile(r"\{\{\s*([^}]+?)\s*\}\}|\{([a-zA-Z_][a-zA-Z0-9_]*)\}|\[([A-Z_]{3,})\]")
XML_OPEN = re.compile(r"<([a-zA-Z_][\w\-]*)(?:\s[^<>]*)?>")
XML_CLOSE = re.compile(r"</([a-zA-Z_][\w\-]*)>")
MD_HEADER = re.compile(r"^#{1,6}\s+\S", re.M)
EXAMPLE_TAG = re.compile(r"<(example|exemplo)\b", re.I)
EXAMPLE_HDR = re.compile(r"^(#+\s*)?(exemplo|example)s?\b", re.I | re.M)
UNTRUSTED_VAR = re.compile(r"(user_input|entrada_usuario|user_message|mensagem|email|documento|document|html|page|pagina|web|retrieved|context|contexto|tool_output)", re.I)
REASON_PHRASE = re.compile(r"(porque|pois|para que|já que|since|because|so that|in order to)", re.I)


@dataclass
class Finding:
    severity: str  # alta | media | baixa | info
    code: str
    message: str
    suggestion: str


def lint(text: str, role: str = "any") -> tuple[list[Finding], dict]:
    f: list[Finding] = []
    lines = text.splitlines()
    n_chars = len(text)
    est_tokens = round(n_chars / 3.6)  # aproximação conservadora para PT/EN misto

    # 1. Linguagem agressiva
    shouts = []
    for w in SHOUT_WORDS:
        shouts += re.findall(rf"(?<![A-Za-zÀ-ÿ]){re.escape(w)}(?![A-Za-zÀ-ÿ])", text)
    caps_words = re.findall(r"\b[A-ZÀ-Ý]{5,}\b", text)
    if len(shouts) >= 3 or len(caps_words) >= 8:
        f.append(Finding("media", "AGRESSIVO",
                         f"{len(shouts)} termos de ênfase (MUST/NUNCA/CRITICAL...) e {len(caps_words)} palavras em CAIXA ALTA.",
                         "Modelos atuais seguem instruções literalmente e superdisparam com ênfase. Use tom normal e explique o porquê."))

    # 2. Instruções negativas em excesso
    instr_lines = [l for l in lines if l.strip()]
    neg = [l for l in instr_lines if NEGATIVE_START.search(l)]
    if len(neg) >= 4 and len(neg) / max(1, len(instr_lines)) > 0.25:
        f.append(Finding("media", "NEGATIVAS",
                         f"{len(neg)} linhas começam com proibição (não/nunca/evite).",
                         "Reescreva como o que fazer ('escreva em prosa' em vez de 'não use markdown')."))

    # 3. Formato de saída
    if not FORMAT_HINTS.search(text):
        f.append(Finding("alta", "SEM_FORMATO",
                         "Nenhuma especificação de formato/extensão de saída encontrada.",
                         "Defina estrutura, extensão e idioma da resposta; se for para parser, use structured output."))

    # 4. Placeholders
    ph = sorted({(m.group(1) or m.group(2) or m.group(3)) for m in PLACEHOLDER.finditer(text)})
    if ph:
        f.append(Finding("info", "PLACEHOLDERS", f"Variáveis encontradas: {', '.join(ph[:20])}",
                         "Confirme que todas serão preenchidas e que dados externos ficam delimitados."))

    # 5. Dados não confiáveis no system prompt
    if role == "system":
        risky = [p for p in ph if UNTRUSTED_VAR.search(p)]
        if risky:
            f.append(Finding("alta", "DADO_NO_SYSTEM",
                             f"Variáveis que parecem conteúdo externo/usuário no system prompt: {', '.join(risky)}",
                             "Mova dados não confiáveis para a mensagem de usuário, delimitados, com lembrete anti-injeção."))

    # 6. Pressão emocional
    emo = EMOTIONAL.findall(text)
    if emo:
        f.append(Finding("baixa", "EMOCIONAL", f"Apelos emocionais/pressão: {', '.join(sorted(set(e if isinstance(e, str) else e[0] for e in emo)))}",
                         "Evidência recente (2026) mostra efeito ~nulo em modelos atuais. Remova e use instruções claras."))

    # 7. Quantificadores vagos sem número por perto
    vague_hits = []
    for l in lines:
        if VAGUE.search(l) and not NUMBER_NEAR.search(l):
            vague_hits.append(l.strip()[:80])
    if vague_hits:
        f.append(Finding("baixa", "VAGO", f"{len(vague_hits)} linha(s) com termo vago sem número (ex.: '{vague_hits[0]}').",
                         "Quantifique: 'até 3 frases', 'no máximo 150 palavras', '3–5 itens'."))

    # 8. Delimitadores mistos
    opens = [t.lower() for t in XML_OPEN.findall(text)]
    closes = [t.lower() for t in XML_CLOSE.findall(text)]
    has_md = bool(MD_HEADER.search(text))
    if opens and has_md and len(opens) >= 3:
        f.append(Finding("baixa", "DELIM_MISTOS", "Usa tags XML e cabeçalhos Markdown como estrutura.",
                         "Tudo bem se o Markdown organiza seções e XML delimita conteúdo; evite alternar arbitrariamente."))

    # 9. Tags não fechadas
    from collections import Counter
    # Só considera tags de bloco (no início da linha); menções inline como "responda em <resposta>" são ignoradas.
    block_opens = [t.lower() for t in re.findall(r"^\s*<([a-zA-Z_][\w\-]*)(?:\s[^<>]*)?>", text, re.M)]
    co, cc = Counter(block_opens), Counter(closes)
    unclosed = [t for t in co if co[t] > cc.get(t, 0) and t not in {"br", "hr", "img"}]
    if unclosed:
        f.append(Finding("media", "TAG_ABERTA", f"Tags possivelmente não fechadas: {', '.join(unclosed[:10])}",
                         "Feche todas as tags para delimitar claramente o conteúdo."))

    # 10. Exemplos
    n_ex = len(EXAMPLE_TAG.findall(text)) or len(EXAMPLE_HDR.findall(text))
    if n_ex == 0 and est_tokens > 150:
        f.append(Finding("info", "SEM_EXEMPLOS", "Nenhum exemplo detectado.",
                         "Exemplos são o controle mais forte de formato e tom; considere 3–5 diversos."))
    elif 0 < n_ex < 3:
        f.append(Finding("info", "POUCOS_EXEMPLOS", f"{n_ex} exemplo(s).",
                         "3–5 exemplos diversos costumam ser o ponto de partida; cubra casos de borda."))

    # 11. Contexto longo com pergunta no início
    if est_tokens > 6000:
        tail = "\n".join(lines[int(len(lines) * 0.85):])
        if "?" not in tail and not re.search(r"(tarefa|task|pergunta|question|responda|answer)", tail, re.I):
            f.append(Finding("media", "PERGUNTA_NO_INICIO",
                             "Prompt longo sem pergunta/tarefa no trecho final.",
                             "Coloque documentos no topo e a pergunta/instrução no fim (até +30% em multi-documento)."))

    # 12. Motivação
    if est_tokens > 200 and not REASON_PHRASE.search(text):
        f.append(Finding("baixa", "SEM_PORQUE", "Nenhuma justificativa ('porque', 'para que'...) para as regras.",
                         "Explique o motivo das regras não óbvias; o modelo generaliza a partir da razão."))

    # 13a. Proibição da saída honesta (causa clássica de alucinação)
    if re.search(r"(nunca diga que n[aã]o sabe|n[aã]o diga que n[aã]o sabe|sempre (deve )?responder|deve sempre responder|"
                 r"never say (that )?you don'?t know|always (provide an )?answer|never refuse)", text, re.I):
        f.append(Finding("alta", "PROIBE_NAO_SEI",
                         "O prompt proíbe admitir falta de informação ou obriga a sempre responder.",
                         "Isso força o modelo a inventar. Dê uma saída segura: 'se não tiver a informação, diga e encaminhe para X'."))

    # 13. Sem saída para incerteza
    if not re.search(r"(não sei|nao sei|não encontr|nao encontr|não houver|se faltar|insuficiente|unknown|not found|don't know|if .* not|null|n/a|desconhecido)", text, re.I) and est_tokens > 150:
        f.append(Finding("baixa", "SEM_FALLBACK", "Não há instrução para quando faltar informação.",
                         "Defina o que responder quando a resposta não existir ou a entrada estiver fora do escopo."))

    # 14. Pedido de CoT visível (aviso para modelos com thinking)
    if re.search(r"(passo a passo|step by step|<thinking>|<pensamento>|pense em voz alta)", text, re.I):
        f.append(Finding("info", "COT_MANUAL", "Pede raciocínio explícito.",
                         "Útil sem thinking nativo. Em modelos de raciocínio, prefira effort/thinking e peça só o contrato de saída."))

    stats = {"chars": n_chars, "tokens_estimados": est_tokens, "linhas": len(lines), "exemplos": n_ex,
             "tags_xml": len(set(opens)), "placeholders": len(ph)}
    order = {"alta": 0, "media": 1, "baixa": 2, "info": 3}
    f.sort(key=lambda x: order[x.severity])
    return f, stats


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", help="arquivo do prompt ou '-' para stdin")
    ap.add_argument("--role", choices=["any", "system", "user"], default="any")
    ap.add_argument("--json", action="store_true", help="saída em JSON")
    a = ap.parse_args()
    text = sys.stdin.read() if a.path == "-" else open(a.path, encoding="utf-8").read()
    findings, stats = lint(text, a.role)
    if a.json:
        print(json.dumps({"stats": stats, "findings": [asdict(x) for x in findings]}, ensure_ascii=False, indent=2))
    else:
        print(f"Prompt: ~{stats['tokens_estimados']} tokens, {stats['linhas']} linhas, {stats['exemplos']} exemplo(s)\n")
        if not findings:
            print("Nenhum problema detectado pela checagem estática.")
        for x in findings:
            print(f"[{x.severity.upper():5}] {x.code}: {x.message}\n        → {x.suggestion}")
    return 1 if any(x.severity == "alta" for x in findings) else 0


if __name__ == "__main__":
    sys.exit(main())

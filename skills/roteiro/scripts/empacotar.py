#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
empacotar.py — valida e empacota a skill no formato Agent Skills.

Uso:
    python3 scripts/empacotar.py

Gera:
    dist/roteiro/          cópia limpa (sem PDFs, _extratos, dist, .DS_Store)
    dist/roteiro.skill     zip com roteiro/SKILL.md na raiz (formato oficial)
    dist/roteiro.zip       mesmo conteúdo, extensão .zip

Não usa dependências externas além da biblioteca padrão. Se PyYAML estiver
disponível, valida o frontmatter com ele; caso contrário, usa um parser mínimo.
"""

import fnmatch
import os
import re
import shutil
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
STAGE = DIST / "roteiro"

EXCLUDE_DIRS = {"__pycache__", "node_modules", "_extratos", "dist", ".git"}
EXCLUDE_FILES = {".DS_Store", "Biblio_roteiro.md"}
EXCLUDE_GLOBS = {"*.pdf", "*.pyc", "*.skill", "*.zip"}

ALLOWED = {"name", "description", "license", "allowed-tools", "metadata", "compatibility"}


def should_exclude(path: Path) -> bool:
    parts = path.parts
    if any(p in EXCLUDE_DIRS for p in parts):
        return True
    if path.name in EXCLUDE_FILES:
        return True
    return any(fnmatch.fnmatch(path.name, g) for g in EXCLUDE_GLOBS)


def parse_frontmatter(text: str):
    if not text.startswith("---"):
        return None, "SKILL.md não começa com frontmatter YAML (---)."
    m = re.match(r"^---\r?\n(.*?)\r?\n---", text, re.DOTALL)
    if not m:
        return None, "Frontmatter inválido: fechamento --- não encontrado."
    raw = m.group(1)

    try:
        import yaml  # type: ignore

        data = yaml.safe_load(raw)
        if not isinstance(data, dict):
            return None, "Frontmatter precisa ser um dicionário YAML."
        return data, None
    except ImportError:
        # parser mínimo: chave: valor (uma linha)
        data = {}
        for line in raw.splitlines():
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            if ":" in line and not line.startswith(" "):
                k, v = line.split(":", 1)
                data[k.strip()] = v.strip().strip('"').strip("'")
        return data, None
    except Exception as e:  # YAML inválido
        return None, f"YAML inválido no frontmatter: {e}"


def validate_skill(skill_dir: Path):
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return False, "SKILL.md não encontrado."

    text = skill_md.read_text(encoding="utf-8")
    fm, err = parse_frontmatter(text)
    if err:
        return False, err

    extra = set(fm.keys()) - ALLOWED
    if extra:
        return False, (
            "Campos não permitidos no frontmatter: "
            + ", ".join(sorted(extra))
            + ". Permitidos: "
            + ", ".join(sorted(ALLOWED))
            + "."
        )

    name = str(fm.get("name", "")).strip()
    if not name:
        return False, "Campo 'name' ausente."
    if not re.match(r"^[a-z0-9-]+$", name):
        return False, "O nome deve ser kebab-case (a-z, 0-9, hífen)."
    if name.startswith("-") or name.endswith("-") or "--" in name:
        return False, "O nome não pode começar/terminar com hífen nem ter hífen duplo."
    if len(name) > 64:
        return False, f"Nome com {len(name)} caracteres (máximo 64)."
    if name != skill_dir.name:
        return False, f"O nome '{name}' deve ser igual ao nome da pasta '{skill_dir.name}'."

    desc = str(fm.get("description", "")).strip()
    if not desc:
        return False, "Campo 'description' ausente."
    if len(desc) > 1024:
        return False, f"Descrição com {len(desc)} caracteres (máximo 1024)."
    if "<" in desc or ">" in desc:
        return False, "A descrição não pode conter '<' ou '>'."

    comp = str(fm.get("compatibility", "") or "").strip()
    if len(comp) > 500:
        return False, f"Compatibility com {len(comp)} caracteres (máximo 500)."

    body_lines = text.count("\n") + 1
    if body_lines > 500:
        return False, f"SKILL.md com {body_lines} linhas (recomendado: até 500)."

    # Referências relativas precisam existir
    missing = []
    for m in re.finditer(r"`((?:references|assets|scripts)/[^`]+)`", text):
        if not (skill_dir / m.group(1)).exists():
            missing.append(m.group(1))
    if missing:
        return False, "Referências quebradas no SKILL.md: " + ", ".join(sorted(set(missing)))

    return True, f"Skill válida: '{name}', {len(desc)} caracteres de descrição, {body_lines} linhas."


def copy_clean(src: Path, dst: Path):
    if dst.exists():
        shutil.rmtree(dst)
    dst.mkdir(parents=True)

    for item in sorted(src.iterdir()):
        rel = item.relative_to(src)
        if should_exclude(rel):
            continue
        target = dst / rel.name
        if item.is_dir():
            shutil.copytree(item, target)
        else:
            shutil.copy2(item, target)


def make_zip(stage: Path, out: Path):
    if out.exists():
        out.unlink()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for path in sorted(stage.rglob("*")):
            if path.is_file():
                arc = path.relative_to(stage.parent)  # roteiro/...
                z.write(path, str(arc))


def main():
    print(f"Skill: {ROOT}")

    ok, msg = validate_skill(ROOT)
    print(("✅ " if ok else "❌ ") + msg)
    if not ok:
        sys.exit(1)

    copy_clean(ROOT, STAGE)
    print(f"📁 Cópia limpa: {STAGE}")

    skill_file = DIST / "roteiro.skill"
    zip_file = DIST / "roteiro.zip"
    make_zip(STAGE, skill_file)
    make_zip(STAGE, zip_file)

    for f in (skill_file, zip_file):
        size = f.stat().st_size / 1024
        print(f"📦 {f} ({size:.1f} KB)")

    # Confere conteúdo essencial
    with zipfile.ZipFile(skill_file) as z:
        names = z.namelist()
        required = ["roteiro/SKILL.md", "roteiro/references/revisao.md",
                    "roteiro/assets/relatorio-revisao.md", "roteiro/scripts/diagnostico.py"]
        missing = [r for r in required if r not in names]
        if missing:
            print("❌ Faltando no pacote: " + ", ".join(missing))
            sys.exit(1)
        print(f"✅ Pacote com {len(names)} arquivos, estrutura verificada.")


if __name__ == "__main__":
    main()

# claude-skills

Skills para Claude Code (padrão aberto [Agent Skills](https://agentskills.io): `SKILL.md` + `references/` + `scripts/`), criadas e testadas por Elisson Coimbra.

| Skill | Para quê | Idioma |
|---|---|---|
| [after-effects-applescript](skills/after-effects-applescript) | Controlar o Adobe After Effects no macOS via servidor MCP `ae-applescript-mcp` (AppleScript/ExtendScript) | PT |
| [designcraft-agent](skills/designcraft-agent) | Diagramar e exportar documentos no DesignCraft (classe InDesign) por CLI/MCP | EN |
| [diretor-de-arte](skills/diretor-de-arte) | Direção de arte baseada em evidências para peças estáticas (cartaz, post, carrossel, impresso) | PT |
| [effectcraft-motion](skills/effectcraft-motion) | Motion graphics no EffectCraft (classe After Effects) e exportação MP4/ProRes/WebM/Lottie | PT/EN |
| [esp32-cyd](skills/esp32-cyd) | Firmware para a placa ESP32-2432S032C ("Cheap Yellow Display" 3,2") no macOS | PT |
| [filmcraft-agent](skills/filmcraft-agent) | Editar e exportar vídeo no FilmCraft (NLE open source) por CLI/MCP | PT |
| [photocraft-design](skills/photocraft-design) | Edição de imagem e design gráfico no PhotoCraft (classe Photoshop) | EN |
| [prompt-engineering](skills/prompt-engineering) | Engenharia de prompt e contexto baseada em papers e docs oficiais | PT |
| [roteiro](skills/roteiro) | Criar e revisar roteiros (longa, série, documentário, institucional, YouTube) | PT |
| [vectorcraft-design](skills/vectorcraft-design) | Arte vetorial no VectorCraft (classe Illustrator) | EN |

## Instalação

```bash
git clone https://github.com/elissoncardoso1/claude-skills.git
cd claude-skills
# todas
for s in skills/*; do ln -s "$PWD/$s" ~/.claude/skills/; done
# ou só uma
ln -s "$PWD/skills/roteiro" ~/.claude/skills/roteiro
```

Abra uma nova sessão do Claude Code; a skill dispara pela `description` ou com `/nome-da-skill`.

As skills de *Craft (DesignCraft, EffectCraft, FilmCraft, PhotoCraft, VectorCraft) e a de After Effects exigem o respectivo app/CLI instalado. A `esp32-cyd` espera a variável `ESP32_HOME` apontando para a pasta dos seus projetos ESP32.

## Licença

[CC BY 4.0](LICENSE). Livros, papers e datasheets citados nas referências não são distribuídos aqui; pertencem aos seus autores.

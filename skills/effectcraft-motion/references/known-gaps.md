# Limitações conhecidas (EffectCraft 0.17.0, alpha)

Fontes: `docs/gaps.md` do repo (tag v0.17.0) + o que o laboratório encontrou. Informe ao usuário as que afetam o pedido.

## Não suportado
| Limitação | Consequência | Fonte |
|---|---|---|
| Não abre `.aep`/`.aepx`/`.mogrt`/`.ffx` | projetos e presets do After Effects não entram; refaça por comandos | gaps.md #1, #23 |
| Plug-ins do After Effects não rodam (Trapcode Particular/Form, Element 3D, Saber, Optical Flares…) | use os nativos: CC Particle World, Particle Playground, Glow, Fractal Noise… (`effects-catalog.md`) | gaps.md #19 |
| Templates Essential Graphics são `.ectemplate`, não `.mogrt` | editores do Premiere não usam diretamente | gaps.md #23 |
| 54 presets próprios (46 em `anim.builtinPresets` + 8 de texto) contra 621 do AE | sem Behaviors/Shapes/Synthetics; monte a animação por keys | gaps.md #7; lab/11 |
| Lottie: só 5 efeitos + controles exportam; sem fundo; texto depende de fonte | ver `export-formats.md` | crates/lottie; lab/09, lab/14 |

## Fidelidade e bugs abertos
- Fidelidade com o AE medida só para ease escalar (168 amostras); qualquer outro recurso pode diferir do AE (gaps.md #2). **Sempre olhe os frames.**
- Grupos de shape: bugs abertos em toggles e operadores (#959/#960) (gaps.md #8).
- Texto: CJK (#453) e alinhamento de parágrafo (#316) com problemas reportados (gaps.md #11). Latin com acentos (Ç, Í, ã) renderiza corretamente (lab/14).
- Cor: ProRes 4444 marcado bt709 mas codificado em sRGB (#340) (gaps.md #10).
- Encoders HEVC/AV1 sem B-frames: arquivos maiores (gaps.md #22).
- Plataforma mais testada: macOS. Linux/Windows têm bugs de interação abertos (gaps.md #6).

## Armadilhas encontradas no laboratório (não documentadas como bug)
1. **Precompor depois de parentear a um null que fica fora do precomp quebra o layout** sem erro (as posições locais viram absolutas). Precomponha primeiro e depois parenteie o layer do precomp, ou inclua o null no precomp (lab/08).
2. **Erro de expressão não falha o comando** (exit 0) → `expr.errors` antes de renderizar.
3. **Parâmetro com tipo errado é ignorado sem aviso**: `comp.new {"width":"wide"}` cria 1920×1080 @ 29,97 fps, 10,01 s.
4. **Valor com forma errada é aceito**: `set … transform/opacity '[1,2]'` grava 1.
5. **`render` sobrescreve** a saída existente sem perguntar.
6. **Sem `--project`/`--empty`, o CLI abre o projeto demo**: edições "somem" num projeto que não é o seu.
7. `comp.new` sem `frameRate` = 29,97 fps; sem `duration` = 10,01 s. Passe sempre os dois.
8. Frame em t = duration sai vazio (último = duration − 1/fps).
9. Sobrescrever o binário `effectcraft-cli` no lugar (cp por cima) faz o macOS matar o processo (exit 137): `rm` e depois `cp`.
10. `script`: os matchNames do AE para animadores de texto não resolveram (`TypeError`); use os paths do engine (`text/animators/…`).
11. Sem `--help` por subcomando; use `command.describe` / `describe_command` e `references/`.

# Exportar Lottie para web (e conferir num player real)

**Especificação:** qualquer comp; exemplo: o lower third  
**Script verificado:** `$SK/recipes/lottie-web-export.sh` (projeto validado, `expr.errors` = 0, frames inspecionados)

```bash
SK=~/.claude/skills/effectcraft-motion   # rode na pasta de trabalho do usuário, não dentro da skill
$SK/recipes/lottie-web-export.sh lt.ecproj "Lower Third" web/lower-third
$SK/scripts/preview.sh lt.ecproj "Lower Third" 6   # contact sheet → inspecione antes do render
```

![referência](frames/lottie-web-export.png)  
*Frame de referência: lottie-web 5.12.2 no Chrome, frames 45/90/135.*

## Como funciona
- Exporta `.json` e `.lottie` (`file.exportLottie`) e imprime os `warnings`, que devem ser repassados ao usuário.
- Padrão `textAsShapes:true` (4º argumento `1`): o texto vira glifos, sem depender de fonte no navegador. Passe `0` para texto vivo (o navegador precisa da fonte; sem ela cai para serifada, verificado).
- Renderiza 3 frames no lottie-web real (`scripts/lottie_preview.sh`, Chrome headless + cdnjs). O fundo aparece transparente (cinza da página): o Lottie não leva a cor de fundo da comp.
- Antes de exportar, projete para Lottie: só shapes/texto/transform; efeitos só Gaussian Blur, Tint, Tritone, Drop Shadow, Fill; sem layer styles; 1 selector por animador; expressões → keys.

**Parâmetros:** projeto, comp, caminho base de saída, `1|0` para textAsShapes.

**Lottie:** É a receita.

**Render:** Saídas: `web/lower-third.json`, `web/lower-third.lottie`, `web/lottie-check/web_sheet.png`.

# Title card com kinetic type

**Especificação:** 1920×1080 · 30 fps · 4 s · 3 palavras com 0,2 s de stagger  
**Script verificado:** `$SK/recipes/title-card-kinetic-type.sh` (projeto validado, `expr.errors` = 0, frames inspecionados)

```bash
SK=~/.claude/skills/effectcraft-motion   # rode na pasta de trabalho do usuário, não dentro da skill
W1=MAKE W2=IT W3=MOVE ACCENT="#ffd23f" $SK/recipes/title-card-kinetic-type.sh tc.ecproj
$SK/scripts/preview.sh tc.ecproj "Title Card" 6   # contact sheet → inspecione antes do render
```

![referência](frames/title-card-kinetic-type.png)  
*Frame de referência: t = 2 s.*

## Como funciona
- Cada palavra é uma text layer (Inter Bold 200, `tracking -20`), com o anchor no meio da altura das maiúsculas (`anchor [0,-70,0]`, `position y-70`) para escalar a partir do centro visual.
- Pop com overshoot: `scale` 0 → 112 (0,28 s) → 100 (0,5 s) + opacity 0→100 em 0,15 s, Easy Ease em todas as keys.
- Sublinhado: rect com `layer.addShapeItem kind:trim` e `contents/trim/end` 0→100 (Trim Paths funciona em shapes preenchidos).
- Saída: tudo parenteado a um null `Drift` (`layer.setParent`), que sobe 70 px enquanto as layers fazem fade (3,2–3,8 s).
- Baselines em 430/620/810: bloco centrado na comp.

**Parâmetros:** `W1`, `W2`, `W3`, `ACCENT`. Palavras longas: reduza `size` para caber em 80% da largura.

**Lottie:** Sim (texto, trim, parenting). Fonte por nome: use `textAsShapes` se não houver animador de texto.

**Render:** `$SK/scripts/render.sh tc.ecproj "Title Card" tc.mp4 h264`

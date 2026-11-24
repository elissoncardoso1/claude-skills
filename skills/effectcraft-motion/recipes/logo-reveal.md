# Logo reveal (write-on + glow)

**Especificação:** 1920×1080 · 30 fps · 4 s  
**Script verificado:** `$SK/recipes/logo-reveal.sh` (projeto validado, `expr.errors` = 0, frames inspecionados)

```bash
SK=~/.claude/skills/effectcraft-motion   # rode na pasta de trabalho do usuário, não dentro da skill
BRAND="NOVA" ACCENT="#36c5ff" $SK/recipes/logo-reveal.sh lr.ecproj
$SK/scripts/preview.sh lr.ecproj "Logo Reveal" 6   # contact sheet → inspecione antes do render
```

![referência](frames/logo-reveal.png)  
*Frame de referência: t = 2,5 s.*

## Como funciona
- Anel: `layer.newShape kind:ellipse fillType:none stroke strokeWidth 12`, `stroke/cap 1` (Round), Trim `end` 0→100 + `offset` −90→0 em 1,2 s (desenha girando).
- Marca: `kind:star`, `scale` 0→115→100 + `rotation` −72→0 (0,8–1,4 s).
- Wordmark: Inter SemiBold 110, `tracking 300`, sobe 40 px + fade (1,3–1,9 s).
- Glow (`effect.apply Glow` + `effects/#1/threshold 20, radius 45, intensity 1.6`) no anel e na marca.
- Para usar um logo real (SVG/PNG): `file.import {paths:[…]}` e anime a layer de footage; não exercitado no lab.

**Parâmetros:** `BRAND`, `ACCENT`.

**Lottie:** **Parcial**: Glow é descartado (`Ring ▸ Glow: effect not supported by Lottie (skipped)`); o resto exporta.

**Render:** ProRes 4444 com alpha: crie a comp sem fundo e `$SK/scripts/render.sh lr.ecproj "Logo Reveal" lr.mov prores --prores 4444 --channels rgba`.

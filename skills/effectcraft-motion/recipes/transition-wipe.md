# Transição wipe entre cenas

**Especificação:** 1920×1080 · 30 fps · 4 s · wipe 1,5–2,3 s  
**Script verificado:** `$SK/recipes/transition-wipe.sh` (projeto validado, `expr.errors` = 0, frames inspecionados)

```bash
SK=~/.claude/skills/effectcraft-motion   # rode na pasta de trabalho do usuário, não dentro da skill
A_TEXT="CAPÍTULO 1" B_TEXT="CAPÍTULO 2" $SK/recipes/transition-wipe.sh tw.ecproj
$SK/scripts/preview.sh tw.ecproj "Wipe" 6   # contact sheet → inspecione antes do render
```

![referência](frames/transition-wipe.png)  
*Frame de referência: t = 1,9 s.*

## Como funciona
- Cena B (solid + título) embaixo; cena A (solid + título) por cima, **precomposta** (`layer.precompose {layers, name:"Scene A", mode:"move"}`) para o wipe agir na cena inteira.
- Linear Wipe no precomp: `effects/#1/completion` 0→100, `angle 90` (vem da esquerda; 0 = de cima, 180 = de baixo, 270 = da direita, testado), `feather 60`.
- Barra de borda: rect 14 px que percorre −20→1940 com o mesmo timing e ease.
- Alternativa sem keys manuais: `time.set {time:T}` + `anim.applyBuiltinPreset {preset:"wipeOutToRight"|"clockWipeOut"|…}` (keys a partir do CTI; wipe de 1 s).
- **Ordem importa**: precomponha antes de parentear qualquer coisa a layers que ficarão fora do precomp.

**Parâmetros:** `A_TEXT`, `B_TEXT`; cores no script.

**Lottie:** **Não**: Linear Wipe não exporta. Para Lottie, use máscara/track matte (não exercitado) ou escala/posição de um shape.

**Render:** `$SK/scripts/render.sh tw.ecproj Wipe tw.mp4 h264`

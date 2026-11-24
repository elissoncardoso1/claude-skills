# Keyframes, interpolação e easing

## Criar keyframes
| Via | Forma | Interpolação resultante |
|---|---|---|
| MCP | `add_keyframe {layer, path, keys:[{time,value},…], interpolation:"easyEase"}` | Bezier com Easy Ease (a forma mais curta) |
| MCP/CLI | `prop.addKey {layer, path, time, value}` · CLI `set C L PATH V --time T` | **Linear** |
| script | `prop.setValueAtTime(t, v)` (t em tempo de **comp**) | Linear |

`interpolation` do `add_keyframe`: `linear | bezier | hold | easyEase`.

## Aplicar ease depois (CLI ou `command_batch`): selecionar e aplicar no mesmo `run`/batch
```
keys.selectAll {"layers":["Title","Panel"]}          # todas as keys dessas layers
keys.select    {"keys":[{"layer":"Title","path":"transform/position","time":0}]}   # keys específicas (tempo de layer)
keys.easyEase  {}            # {"which":"in"|"out"} para um lado só; = F9 do After Effects
keys.easyEaseIn {} / keys.easyEaseOut {}
keys.toggleHold {}
keys.interpolation {"interpolation":"linear|bezier|continuousBezier|autoBezier|hold", "in"?, "out"?, "spatial"?}
keys.velocity  {"inSpeed"?, "inInfluence"? (%), "outSpeed"?, "outInfluence"? (%)}   # curva custom
keys.setEase   {"layer","path","time","side":"in|out","speed"?,"influence"? (%)}       # uma key, sem seleção
```
A seleção **não** persiste entre chamadas do CLI (cada chamada reabre o arquivo).
Verificado (opacity 0→100 em 1 s, valor em t=0,25): linear 25 · `keys.velocity` com influence 80/80 = 4,76 · `keys.setEase` out 80 só na 1ª key = 2,7 · `keys.interpolation hold` = 0. Easy Ease em position 640→540 em 0,8 s: 624,4 em t=0,2 (linear 615).

## Semântica (crates/keyframe/src/lib.rs)
- Easy Ease = speed 0, influence 33,33% nos dois lados; ease padrão de uma key Bezier = influence 16,67%.
- Influence alta (60–85%) = aceleração e desaceleração mais dramáticas. Para "snap" de UI: `outInfluence` 70–85 na key de saída, `inInfluence` 70–85 na key de chegada.
- Overshoot/bounce sem expressão: 3 keys (0 → 110–115% → 100%) com Easy Ease; ver `recipes/title-card-kinetic-type.md`.
- Propriedades espaciais (position): o ease é um único valor ao longo do motion path; as tangentes ficam em `keys.setSpatialTangents`.

## Tempo
- Tempo de keyframe = **tempo de layer** (o padrão de `prop.addKey`, `add_keyframe`, `set --time`). Em layers deslocadas (`layer.timing {start}`) ou esticadas, passe `"timeBase":"comp"` para escrever em segundos de comp.
- Leituras (`get --time`, `get_property`, `render_frame`) usam tempo de comp. As respostas trazem `time`/`layerTime` e `compTime`.
- Tempos são ajustados ao frame mais próximo da comp.
- Último frame renderizável = `duration − 1/fps`.

## Timing de referência (motion design)
| Elemento | Duração típica |
|---|---|
| Entrada/saída de UI, lower third, títulos | 0,3–0,8 s |
| Stagger entre elementos/palavras | 0,05–0,2 s |
| Hold mínimo de texto legível | ~0,3 s por palavra + 1 s (6 palavras ≈ 3 s) |
| Transição entre cenas | 0,5–1,0 s |
| Loop de fundo | ciclo inteiro, primeiro frame = frame em t=duration |

Movimento linear só quando há motivo (loops contínuos, rotação constante, scroll de grid). O resto leva ease.

## Presets que criam keys (começam no tempo atual, CTI)
`time.set {"time":T}` antes, no mesmo `run`/batch:
- `anim.applyBuiltinPreset {"preset":"fadeIn"|"wipeInFromLeft"|…,"layers":[…]}`: 23 transições e 23 fundos (`anim.builtinPresets`). `fadeIn` = 0,5 s; `wipeInFromLeft` = 1 s (Linear Wipe `completion` 100→0).
- `layer.applyTextPreset {"layer","preset":"typewriter|fadeUpCharacters|bounceInWords|trackingIn|scramble|blurIn|jitter|dropInLines"}`.

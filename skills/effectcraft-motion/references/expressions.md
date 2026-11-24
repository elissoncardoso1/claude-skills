# Expressões (JavaScript, modelo de expressões do After Effects)

## Atribuir e conferir
- CLI/MCP: `prop.setExpression {"layer","path","expression":"wiggle(2,30)"}`; desligar: `{"layer","path","enabled":false}`.
- MCP: `set_property {layer, path, expression}`.
- CLI `set C L PATH VALUE --expression E` exige um VALUE válido (ex.: o valor atual).
- **Expressão com erro não falha o comando (exit 0).** Antes de renderizar, sempre rode `exec expr.errors '{"comp":"Main"}' P --json` e confira `count == 0`. Por propriedade: `get …` traz `evaluated` (o que renderiza) e `expressionError`. Erro de sintaxe deixa a expressão gravada, porém desabilitada.

## Padrões testados no 0.17.0 (lab/04, lab/14)
| Objetivo | Propriedade | Expressão | Resultado verificado |
|---|---|---|---|
| Tremor orgânico | `transform/position` | `wiggle(2,60)` | posição varia ±60 px, 2×/s |
| Repetir a animação dos keys | `transform/rotation` (keys 0→90 em 1 s) | `loopOut("cycle")` | 45° em 0,5 / 1,5 / 2,5 s |
| Seguir outra layer | `transform/position` | `thisComp.layer("Jitter").transform.position + [0,200]` | Follower = Jitter + 200 px em y |
| Rotação constante | `transform/rotation` | `time*90` | 90°/s |
| Evolução em loop perfeito | `effects/#1/evolution` (Fractal Noise com `evolutionOptions/cycleEvolution` true, `cycle` 2) | `time / thisComp.duration * 360 * effect("Fractal Noise")("Evolution Options")("Cycle (in Revolutions)")` | evolution 0 e 720 renderizam idênticos (RMSE 0) |

## Referenciar parâmetros de efeito
- Parâmetro de topo: `effect("Fractal Noise")("Complexity")` ✔ · `effect(1)("Complexity")` ✔
- Parâmetro **dentro de grupo**: inclua o grupo pelo nome exibido: `effect("Fractal Noise")("Evolution Options")("Cycle (in Revolutions)")` ✔. Sem o grupo → `Property "…" not found in "Fractal Noise"`.
- Os nomes exibidos dos grupos e parâmetros estão em `effects-catalog.md` (ids) e em `effectcraft-cli exec effect.list --json` (campo `name`).

## Disponível no runtime (crates/expr/src/prelude.js)
- Globais: `time`, `value`, `thisComp`, `thisLayer`, `index`, `comp("Nome")`, `footage()`.
- Métodos de propriedade: `valueAtTime`, `velocityAtTime`, `speedAtTime`, `key(n)`, `nearestKey`, `numKeys`, `wiggle`, `temporalWiggle`, `smooth`, `loopIn`, `loopOut`, `loopInDuration`, `loopOutDuration`, `points/inTangents/outTangents/isClosed`, `pointOnPath`, `tangentOnPath`, `normalOnPath`.
- `loopOut(type)` / `loopIn(type)`: `"cycle"` (padrão) | `"pingpong"` | `"offset"` | `"continue"`.
- Matemática: `add sub mul div clamp dot cross length normalize lookAt degreesToRadians radiansToDegrees`; interpolação `linear ease easeIn easeOut`; aleatório `seedRandom random gaussRandom noise`; tempo `timeToFrames framesToTime timeToTimecode posterizeTime`; cor `rgbToHsl hslToRgb hexToRgb`; `createPath`.
- Layer: `effect()`, `mask()`, `content()`, `toComp`, `fromComp`, `toWorld`, `fromWorld`, `sourceRectAtTime`, `sampleImage`.
- Arrays somam como vetores (`position + [0,200]`).

Fora dos padrões testados acima, trate cada expressão como hipótese: aplique, confira `expressionError`/`evaluated` em 2–3 tempos e olhe o frame.

## Lottie
Expressões **não** vão para o Lottie, a menos que `file.exportLottie {…,"includeExpressions":true}` (exportadas como `x`; a maioria dos players as ignora). Para web, prefira keys (`prop.convertExpressionToKeyframes {layer, path}` existe no registro; não exercitado no lab).

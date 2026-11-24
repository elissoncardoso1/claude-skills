# Troubleshooting: erros reais do 0.17.0 e como se recuperar

Exit codes do CLI: `1` = erro de comando/projeto; `2` = erro de uso (opção desconhecida, JSON inválido). No MCP: `isError:true` com a mesma mensagem; argumento desconhecido numa tool → JSON-RPC `-32602`.

| Mensagem (literal) | Causa | Correção |
|---|---|---|
| ``unknown command `layer.doMagic` `` | id inventado ou com erro de digitação | procure em `references/command-catalog.md` ou `effectcraft-cli commands --filter …`; nunca invente ids |
| ``invalid parameters for `layer.newSolid`: unknown parameter(s) `colour`; accepted: name, color, …`` | chave errada | use exatamente uma das chaves listadas na própria mensagem |
| `params are not valid JSON: key must be a string at line 1 column 2` (exit 2) | JSON malformado ou com aspas do shell | use aspas simples em volta do JSON no shell, ou `run --args-file` |
| ``unknown option `--bogus` `` (exit 2) | flag inexistente | ver `cli-reference.md` |
| `no composition "Nope"` | nome de comp errado | `effectcraft-cli info --project P` lista as comps |
| `no layer "Ghost"` / `no layer "#9"` | nome ou índice errado | `info` lista `#n id tipo nome` da comp ativa; `exec comp.info '{"comp":"X"}'` para outra |
| ``no property `transform/positon` `` | path errado | `effectcraft-cli props C L P --flat` |
| `` `effects/#1` is a property group; use layer.tree (MCP: get_layer) `` | path de grupo em get/set | aponte para uma folha (`effects/#1/blurriness`) |
| `can't use "abc" for a scalar property` | tipo de valor incompatível | número para scalar, `[x,y,z]` para vec3, `"#hex"` para cor |
| ``unknown effect `Optical Flares` `` | plug-in do AE ou nome inexistente | `effects-catalog.md`; plug-ins de terceiros não existem |
| `step 2 (prop.set): … no property \`effects/#1/radiu\`; the batch was rolled back (nothing changed)` | erro dentro de `add_effect`/`batch` | corrija o passo; nada foi aplicado |
| `invalid parameters for \`renderQueue.add\`: H.264 has no alpha channel` | alpha num formato sem alpha | prores 4444, webm vp9, png, gif |
| `AV1 WebM has no alpha channel (VP9 WebM has)` | `--webm-codec av1` com rgba | `--webm-codec vp9` |
| `format: h264\|hevc\|av1\|prores\|…` | `--format` inválido | um dos formatos listados |
| `cannot read nope.ecproj: No such file or directory` | caminho errado | confira o cwd; paths relativos são relativos ao diretório atual |
| `F.ecproj is not a project EffectCraft can open: invalid type: floating point …` | `.ecproj` editado à mão com tipo errado (ex.: tempo em segundos em vez de Tick) | regere por comandos; `scripts/validate_ecproj.py F --engine` |
| `run: main.ecproj: unknown command \`main.ecproj\`` | projeto dentro do `--args-file` | o arquivo leva só pares id/json; projeto e flags vão na linha de comando |
| `set: invalid parameters for \`prop.set\`: can't use "x" …` com `--expression` | `set` exige VALUE válido | `exec prop.setExpression '{"layer","path","expression"}'` |
| `Error at line 1: Property "X" not found in "Fractal Noise"` (em `expressionError` / `expr.errors`) | parâmetro de efeito dentro de grupo referenciado sem o grupo | `effect("Fractal Noise")("Evolution Options")("Cycle (in Revolutions)")` |
| `Error at line 1: Layer named "Nope" does not exist` | `thisComp.layer("…")` com nome errado | confira nomes com `info` |
| `Error at line 1: SyntaxError: …` | sintaxe JS | a expressão fica gravada mas desabilitada; corrija e reaplique |
| exit 137 (SIGKILL) ao rodar o CLI | binário assinado sobrescrito no lugar (macOS) | `rm` no binário antigo e depois `cp` do novo |
| `run` falhou no meio | um passo inválido | **nada foi salvo** (o arquivo fica intacto): corrija e rode o `run` inteiro de novo |

## Falhas silenciosas: detectar ativamente
| Sintoma | Verificação |
|---|---|
| Comp com tamanho/fps inesperado | `exec comp.info` logo após criar; confira `width/height/frameRate/duration` |
| Valor gravado diferente do pedido | `get … --json` após `set` em propriedades vetoriais |
| Expressão não funciona, mas o comando passou | `exec expr.errors '{"comp":"C"}'` → `count` deve ser 0 |
| Saída antiga sobrescrita | `scripts/render.sh` (recusa sobrescrever) |
| Frame vazio | o tempo pedido é ≥ duration, ou está fora do in/out da layer |
| Layout quebrado após precompose | ver `known-gaps.md` item 1 |

## Recuperação no MCP
- `undo {}` / `history {}` → `history {"goto": n}`.
- Sem `--autosave`, um restart do servidor perde o trabalho: `save_project` a cada marco.
- Com `--autosave`, os checkpoints ficam em `~/Library/Application Support/EffectCraft/EffectCraft Auto-Save/MCP/<sessão>/` (macOS); recupere com `open_project {path}` e depois `save_project`.

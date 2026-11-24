# effectcraft-cli 0.17.0: referência verificada

Todo exemplo abaixo foi executado em macOS arm64 com o binário 0.17.0. **Não existe `--help` por subcomando**: `effectcraft-cli <qualquer> --help` imprime o help global.

## Regras gerais

- **Sem projeto, o CLI abre o DEMO.** Sempre passe `--project F.ecproj`, um `F.ecproj` posicional (último argumento) ou `--empty`.
- `--save` regrava o projeto aberto; `--save-as F` grava em outro arquivo. Sem eles, nada é persistido.
- `--json`: um único documento JSON compacto no stdout.
- Códigos de saída: `0` ok; `1` erro (`{"error":…}` com `--json`, ou `effectcraft-cli <sub>: msg` no stderr); `2` erro de uso (opção desconhecida, JSON de parâmetros inválido).
- `<comp>` = nome, id ou `-` (comp ativa). `<layer>` = nome, id ou `'#n'` (1 = topo). `<value>` = JSON (`50`, `[960,540,0]`, `"#ff0000"`) ou string sem aspas.
- Tempos em segundos. `set --time` e `prop.addKey` usam **tempo de layer**; `get --time`, `render-frame --time` usam **tempo de comp** (iguais enquanto a layer começa em 0 e não está esticada).

## Subcomandos

| Uso | Exemplo verificado | Saída |
|---|---|---|
| `info` | `effectcraft-cli info --project p.ecproj` | itens do projeto + layers da comp ativa (`#n id tipo nome`) |
| `commands [--filter T] [--enabled]` | `effectcraft-cli commands --filter keys --empty` | lista de ids |
| `exec ID [--params JSON] \| ID 'JSON'` | `effectcraft-cli exec comp.new --params '{"name":"Main","width":1920,"height":1080,"frameRate":30,"duration":5}' --empty --save-as main.ecproj` | `{"result":{"comp":1},"saved":"main.ecproj"}` |
| `run ID 'JSON' [ID 'JSON'…]` | `effectcraft-cli run main.ecproj layer.newSolid '{"name":"BG","color":"#101828"}' layer.newText '{"text":"HELLO","name":"Title","size":140}' --save --json` | `{"result":[{"command":…,"result":{"layer":4}},…],"saved":…}` |
| `run --args-file F` | `effectcraft-cli run --args-file steps.txt main.ecproj --save` | igual a `run`; **F contém só linhas id / json alternadas**; projeto e flags vão na linha de comando |
| `props COMP LAYER [--flat] [--time S]` | `effectcraft-cli props Main Title main.ecproj --flat` | todos os paths: `transform/position  vec3  [960.0,540.0,0.0]  [2 keys]` |
| `get COMP LAYER PATH [--time S]` | `effectcraft-cli get Main Title transform/position --time 0.4 main.ecproj --json` | `{value, evaluated?, expression, keys:[{time,compTime,layerTime,in,out,value}], type, uid}` |
| `set COMP LAYER PATH VALUE [--time S] [--expression E]` | `effectcraft-cli set Main Title transform/opacity 40 main.ecproj --save` | com `--time` cria keyframe (Linear). `--expression` exige um VALUE válido; para só a expressão, use `exec prop.setExpression` |
| `render-frame [--comp C] [--time S\|--frame N] [--max-side PX\|--scale K] [--out F.png] [--transparent]` | `effectcraft-cli render-frame main.ecproj --comp Main --time 1 --max-side 640 --out f.png` | `rendered 640x360 at 1.000s in 13 ms -> f.png` (stderr). O último frame é `duration − 1/fps` |
| `render` | ver `export-formats.md` | `done: Main → /abs/out.mp4 in 0.35s` |
| `script FILE.jsx [P] \| --eval CODE` | `effectcraft-cli script --eval 'app.project.activeItem.name' main.ecproj` | resultado em JSON; erro → exit 1 com `file:line:col` |
| `mcp [--autosave \| --bridge PORT]` | ver `mcp-tools.md` | servidor stdio |
| `render/render-frame --template T.ectemplate [--values V.json]` | (doc; não exercitado no lab) | UNVERIFIED |

## Padrões que funcionaram

```bash
E=effectcraft-cli
# 1) projeto novo (sempre --empty)
$E exec comp.new --params '{"name":"Main","width":1920,"height":1080,"frameRate":30,"duration":5,"background":"#101828"}' --empty --save-as main.ecproj
# 2) várias edições numa chamada (a seleção de keyframes vale só dentro do mesmo run)
$E run main.ecproj \
  layer.newText '{"text":"HELLO","name":"Title","font":"Inter","style":"Bold","size":140,"fill":"#ffffff","position":[960,560]}' \
  prop.addKey '{"layer":"Title","path":"transform/opacity","time":0,"value":0}' \
  prop.addKey '{"layer":"Title","path":"transform/opacity","time":0.6,"value":100}' \
  keys.selectAll '{"layers":["Title"]}' keys.easyEase '{}' --save
# 3) checar erros de expressão antes de renderizar
$E exec expr.errors '{"comp":"Main"}' main.ecproj --json     # {"count":0,"errors":[]}
# 4) preview e render com verificação
scripts/preview.sh main.ecproj Main 6
scripts/render.sh main.ecproj Main out.mp4 h264
```

- **Easy Ease pelo CLI:** `prop.addKey` cria keys **lineares**. Em seguida, no mesmo `run`: `keys.selectAll {"layers":[…]}` (ou `keys.select {"keys":[{layer,path,time}…]}`) + `keys.easyEase {}`. `keys.easyEase {"which":"in"|"out"}` para um lado só.
- Comandos que dependem do tempo atual (presets) precisam de `time.set {"time":T}` antes, no mesmo `run`.
- `exec comp.info '{"comp":"Main"}' P --json` → `{duration, frameRate, width, height, background, layers:[…]}`.
- `exec command.describe '{"command":"ID"}' --empty --json` → params + JSON Schema de um comando.
- `exec text.fonts '{"query":"Inter"}' --empty --json` → famílias e estilos. Embutidas (funcionam em qualquer máquina): **Inter** (Regular, Medium, SemiBold, Bold, Italic), **JetBrains Mono** (Regular), **Noto Serif** (Regular).

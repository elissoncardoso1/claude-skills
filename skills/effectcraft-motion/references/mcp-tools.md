# Tools MCP do EffectCraft 0.17.0

Servidor: `effectcraft-cli mcp` (JSON-RPC 2.0 por stdio; protocolos 2025-06-18, 2025-03-26, 2024-11-05). serverInfo `EffectCraft (headless)` 0.17.0.
Flags: `--autosave` (checkpoint a cada edição), `--bridge PORT` (dirige o app aberto com `--control PORT`), `--automation-read-root DIR` / `--automation-write-root DIR` (confinam os arquivos; com eles, scripts e `ui_*` são recusados), `--gpu`, `--project F` / `--demo`.
Resources: `effectcraft://document` (= `doc_inspect`), `effectcraft://commands` (= `command_list`). Não há prompts.

## As 27 tools do modo headless (tabela gerada do `tools/list` real; `?` = opcional)

| tool | argumentos | o que faz |
|---|---|---|
| `list_commands` | enabled_only?, filter?, schemas? | List engine commands: id, label, menu path, shortcut, `params` doc (e.g |
| `describe_command` | command?, id? | One command in full: id, label, menu path, shortcut, the `params` doc, a JSON Schema of its parameters (`schema`: properties, required, addi |
| `execute_command` | command?, id?, params? | Run any engine command by id with JSON params; edits are undoable |
| `run_script` | code, name? | Run JavaScript with an After Effects-style scripting object model (app, app.project, items.addComp, comp.layers.addSolid/addText/addShape/ad |
| `get_project` |  | Project overview: file path, dirty flag, bit depth, every item (id, name, type Composition/Footage/Solid/Folder, size, duration, layer count |
| `get_comp` | comp? | A composition: id, name, size, frame rate, duration, work area, background and its layers top to bottom (id, index, name, type, in/out/start |
| `get_layer` | comp?, depth?, flat?, layer, time? | A layer's property tree (transform, masks, effects, text, shape contents, ...): leaf properties have a `path` usable with get_property/set_p |
| `get_property` | comp?, layer, path, time? | Read one property: type, value at `time` (comp seconds; default the current time), whether it is animated, its keyframes (time, value, in/ou |
| `set_property` | comp?, expression?, layer, path, time?, timeBase?, value? | Set a property |
| `add_keyframe` | comp?, interpolation?, keys?, layer, path, time?, timeBase?, value? | Add keyframes to a property (turns the stopwatch on): one with `time` (+ optional `value`, default the current value) or many with `keys: [{ |
| `add_effect` | comp?, effect, layer, values? | Apply an effect to a layer and optionally set its parameters in one undoable call |
| `list_effects` | filter? | The effect registry: id, After Effects name, category, GPU and 32-bpc support |
| `list_fonts` | query?, rescan?, variable? | The font families text layers can use, bundled and installed on this machine: family, styles, origin (bundled / system / user), whether it i |
| `get_state` |  | Where things stand: the editor state (active comp, current time, selected layers/keys/items, open comps, tool, work area) plus what this bui |
| `render_frame` | comp?, inline?, max_side?, path?, time?, transparent? | Render a composition frame (default: the active comp at the current time) and return it as a PNG image, longest side `max_side` (default 960 |
| `open_project` | demo?, new?, path? | Open a project: `path` to an .ecproj file, `demo: true` for the built-in demo project, or `new: true` for an empty project |
| `save_project` | path? | Save the project to its current file, or to `path` (Save As, .ecproj). |
| `undo` | steps? | Undo the last `steps` edits (default 1) |
| `redo` | steps? | Redo `steps` undone edits (default 1). |
| `history` | goto? | The branching undo history (History panel): without arguments lists every state {index, id, label, parent, depth (0 = working line, >0 = bra |
| `script_ui` | action?, result?, value?, widget?, window? | Drive ScriptUI windows that scripts opened (dialogs, palettes, dockable panels) |
| `batch` | atomic?, label?, steps | Run several engine commands in one call as ONE undo step (engine.batch) |
| `command_list` | enabled_only?, filter?, schemas? | List engine commands: id, label, menu path, shortcut, `params` doc (e.g |
| `command_run` | id, params? | Run any engine command by id with JSON params; edits are undoable |
| `render_preview` | comp?, max_side?, time?, transparent? | Render a composition frame (default: the active comp at the current time) and return it as a PNG image, longest side `max_side` (default 960 |
| `command_batch` | steps, stop_on_error? | Run commands in order, returning each result or error |
| `doc_inspect` |  | Inspect the project overview and active composition (null when no composition is active). |
**Modo bridge** (`mcp --bridge 9877`, com o app aberto via `/Applications/EffectCraft.app/Contents/MacOS/EffectCraft --control 9877`): 36 tools, ou seja, as 27 acima mais `control {method, params}`, `screenshot {panel?, id?, max_side?, path?}`, `ui_click`, `ui_drag`, `ui_elements {prefix?}`, `ui_inspect`, `ui_key`, `ui_set` e `ui_type`. Fechar o app: `control {method:"app.quit", params:{force:true}}`.

## Comportamentos verificados

- `execute_command` / `command_run` executam **qualquer** id do registro (ver `command-catalog.md`). Chave de parâmetro desconhecida → `isError:true` com a lista de chaves aceitas.
- Argumento desconhecido numa **tool** → erro JSON-RPC `-32602` (`unknown argument "x" for set_property; expected: …`).
- `add_effect {layer, effect, values}` aplica e configura num único passo de undo e devolve `path` (`effects/#n`) e os paths de todos os parâmetros. Um valor inválido faz rollback: "the batch was rolled back (nothing changed)".
- `add_keyframe {layer, path, keys:[{time,value}…], interpolation:"easyEase"|"linear"|"bezier"|"hold"}` é a forma mais curta de criar keyframes com ease.
- `set_property {…, expression}` atribui uma expressão. A resposta traz `evaluated` e `expressionError`.
- `batch {steps:[{command, params}], atomic?}`: um passo de undo; `"$1.layer"` reaproveita o resultado do passo 1; se algum passo falhar, desfaz tudo.
- `command_batch {steps:[{id, params}], stop_on_error?}`: um passo de undo por comando; continua após erro se `stop_on_error:false`.
- `render_frame {comp?, time (s de comp), max_side?, path?, transparent?}` devolve a **imagem inline** e grava o PNG se receber `path`.
- `open_project {path | demo:true | new:true}` e `save_project {path}`. **Sem `--autosave`, o trabalho headless vive só na memória**: salve a cada marco.
- Todos os erros vêm com `isError:true` e a mesma mensagem do CLI (ver `troubleshooting.md`).

## Quando usar MCP, CLI ou script

| Situação | Via | Por quê |
|---|---|---|
| Criar e iterar visualmente uma peça | **MCP** | estado em memória, `render_frame` com imagem inline, `add_keyframe` com ease, erros estruturados |
| Tarefa pontual num `.ecproj` existente (trocar texto, renderizar, exportar) | **CLI** `exec`/`run`/`set`/`render` | uma linha, sem estado, reproduzível |
| Gerar muitas variações / lote | **CLI** `run --args-file` dentro de um shell script | determinístico; o arquivo de argumentos não tem limite de tamanho |
| Lógica com laços e condicionais sobre o projeto | `script --eval` / MCP `run_script` (JS no modelo do AE) ou `app.run(id, params)` dentro do script | loops; atenção: o `setValueAtTime` usa tempo de comp e os matchNames do AE nem sempre resolvem |
| Ver a interface do app ao vivo | MCP `--bridge` | `screenshot`, `ui_*` |

Se as tools `mcp__effectcraft__*` estiverem disponíveis na sessão, use-as. Senão, use o CLI; os ids e parâmetros são **os mesmos**.

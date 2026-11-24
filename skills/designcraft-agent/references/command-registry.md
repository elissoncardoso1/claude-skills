# Command registry and discovery

## Shape [O][S]
Every action is a `CommandSpec`: `{id, label, menu: [path], params: "<human-readable signature>",
shortcut, enabled}`. `params` is documentation text, **not** JSON Schema: `?` = optional,
`a|b` = enum, `→ {...}` = result. `enabled` reflects the current state (e.g. needs a selection);
547 commands headless on 0.17.2, of which ~30 are enabled with nothing selected — a disabled
command fails with `command \`x\` is not available right now: <reason>`.

Namespaces (count): object 60, type 43, table 41, file 37, layout 28, style 28, edit 18, text 17,
path 15, swatch 13, transform 10, book 10, guide 10, xml 10, data 10, note 9, story 9, layer 9,
library 8, select 8, links 7, … (full list: `evidence/commands-0.17.2.json`).

## Discovery loop (use instead of memory)
```sh
designcraft-cli commands wrap | python3 -c "import json,sys;[print(c['id'],'—',c['label']) for c in json.load(sys.stdin)]"
designcraft-cli describe object.textWrap
```
MCP: `list_commands {filter}`; app: `engine.commands` (adds UI-only commands like `view.*`).
Then try the command on a scratch document and inspect the result before using it in real work.

## Validation behaviour [O][S `engine/src/cmd/params.rs`]
- Unknown key → `unknown parameter \`k\`; the command takes: a, b` (or `did you mean \`x\`?`).
- Missing required → `missing rect`; bad enum → `unknown variant \`justify\`, expected one of …`.
- Unknown id → `unknown command \`x\``. UI command headless → `\`view.zoomIn\` is a UI command; it needs the desktop app`.

## Version drift — check after every upgrade
```sh
designcraft-cli --version
designcraft-cli commands > /tmp/cmds-new.json
python3 - <<'PY'
import json
old = {c["id"]: c["params"] for c in json.load(open("<skill>/evidence/commands-0.17.2.json"))}
new = {c["id"]: c["params"] for c in json.load(open("/tmp/cmds-new.json"))}
print("added:", sorted(new.keys() - old.keys()))
print("removed:", sorted(old.keys() - new.keys()))
print("params changed:", sorted(k for k in old.keys() & new.keys() if old[k] != new[k]))
PY
python3 <skill>/scripts/dc_mcp.py --tools      # compare with evidence/mcp-tools-0.17.2.json
python3 <skill>/tests/test_scripts.py          # scripts still work
```
Any command used in references/ that appears in "removed" or "params changed" must be re-described
and re-tested before relying on it. Re-run the scenario suite in `tests/scenarios.md`.

## Commands used by this skill's workflows (all exercised on 0.17.2)
file.new · file.presets · file.place · file.exportPdf · file.exportPptx · layout.pages.insert ·
frame.create · line.create · object.color · object.fill · object.stroke · object.gradient ·
object.opacity · object.dropShadow · object.cornerOptions · object.align · object.distribute ·
object.group · object.rename · object.arrange · object.fit · object.setLayer · object.textWrap ·
object.textFrameOptions · transform.set · layer.new · layer.set · layer.activate · selection.set ·
text.select · text.selectStory · text.placeCaret · text.insert · text.release · text.thread ·
story.setText · story.get · type.char · type.para · style.paragraph.create · style.paragraph.apply ·
style.character.create · style.character.apply · swatch.create · toc.generate · document.inspect ·
document.list · font.list · preflight.run · edit.undo · type.selectionAttrs · type.onPath

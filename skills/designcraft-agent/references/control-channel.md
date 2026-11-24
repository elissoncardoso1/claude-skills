# Desktop app and control channel

## Start the app [O]

```sh
# isolated profile so tests don't touch the user's prefs/recovery
DESIGNCRAFT_CONFIG_DIR=/tmp/dc-profile \
  /Applications/DesignCraft.app/Contents/MacOS/DesignCraft --control 7979 > /tmp/dc-app.log 2>&1 &
until nc -z 127.0.0.1 7979; do sleep 0.5; done
```
`DESIGNCRAFT_CONTROL_PORT` is the env alternative [D]. Listens on 127.0.0.1 only, **no
authentication** — quit when done: `designcraft-cli app --method app.quit` (quits without asking
to save) [O]. The app starts with an empty "Untitled-1" document [O].

## Protocol [D][O]

JSON lines over TCP. Request `{"id"?, "method", "params"?}` → reply `{"id", "ok": true, "result"}` or
`{"id", "ok": false, "error"}`. A line that isn't a JSON object with `method` gets an error **and the
connection is closed** [O]. Unknown command params → `ok:false` naming the accepted keys [O].

```sh
printf '%s\n' '{"id":1,"method":"engine.execute","params":{"command":"frame.create","params":{"rect":[36,36,300,200],"content":"text"}}}' | nc -w 2 127.0.0.1 7979
```

| Method | Verified | Use |
|---|---|---|
| `engine.execute {command, params}` | [O] | any command (also via `app CMD JSON`, `script --connect`) |
| `engine.commands` | [O] | registry incl. UI commands |
| `document.inspect` | [O] | errors "no document open" if none |
| `ui.inspect` | [O] | activeDocument, documents, tool, view, canvasRect, dialog, docking |
| `ui.screenshot {path?}` | [O] | whole window PNG (2880×1800 on Retina) |
| `ui.render {path?, page?, scale?, bleed?}` | [O] | page PNG |
| `ui.menu.list`, `ui.menu.invoke {command, params?}` | [O] list / [D] invoke | menu tree; invoke without params opens the dialog |
| `ui.dialog.set/confirm/cancel`, `ui.pointer`, `ui.key`, `ui.text`, `ui.click`, `ui.drag`, `ui.set` | [D] | UI automation; prefer `engine.execute` |
| `app.quit` | [O] | quit without save prompt |

## CLI front-ends [O]

```sh
designcraft-cli app --port 7979 file.new '{"preset":"A4"}'           # one command
designcraft-cli app --port 7979 --method ui.screenshot '{"path":"/abs/w.png"}'
designcraft-cli script steps.dcs --connect 7979 --save /abs/out.designcraft
python3 scripts/dc_mcp.py calls.json -- --connect 7979               # MCP tools incl. screenshot
```
Use the app when the user wants to watch, needs a window screenshot, or a UI-only command/dialog.
Everything else is faster and reproducible headless.

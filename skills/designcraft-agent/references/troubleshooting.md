# Troubleshooting (messages observed on 0.17.2)

| Symptom / message | Cause | Fix |
|---|---|---|
| text unchanged after `type.char`/`style.paragraph.apply` (both success and no-op return `null`) | nothing targeted | `selection.set {ids:[frame]}` or `text.select` first |
| `unknown parameter \`story\`; the command takes: frame, point` | wrong key (e.g. `text.selectStory` takes `frame`) | use the listed keys; `describe` |
| `unknown variant \`justify\`, expected one of …` | enum value | pick from the list (`leftJustified`) |
| `missing rect` / `missing layer` | required param absent or wrong type (`object.setLayer` needs the layer **id**) | pass it |
| `give two of from, to and rect` | `text.thread` | `{from, rect}` or `{from, to}` |
| `no spread Doc(1)` | spread doesn't exist yet | `layout.pages.insert` first; facing docs: page 2 is spread 1 |
| `no swatch named \`X\`` | swatch missing | `swatch.create` first; names are exact |
| `no such story s9` | stale/hard-coded id | use `$N.story` or `document.inspect` |
| `\`$5.id\`: step 5 hasn't run (only 0 have)` | bad script reference | indexes are 0-based steps, comments excluded |
| `line 1: key must be a string …` | invalid JSON in script | quote keys; one step per line |
| `command \`x\` is not available right now: no document open` | app has no document | `file.new` / `file.open` |
| `\`view.zoomIn\` is a UI command; it needs the desktop app` / `screenshot is not available headless` | UI-only | use the app (control-channel.md) or skip |
| `automation path rejected: outside the write root …` | MCP roots | write inside the root |
| `--export x.docx: unknown file type (...)` | unsupported extension | supported list in export.md |
| `--scale has no --export or --all-pages after it` | option order | put options before their export |
| Font looks wrong / `styleSubstitute` | style not available (Inter Bold) | use an available style (Source Sans 3 Bold) |
| Object missing from render | on a hidden layer, or created while a hidden layer was active | `layer.set {visible:true}` / `object.setLayer` |
| Text cut off | overset | `story.get` → thread/enlarge/shorten |
| Page 2 objects appear on page 1 or at wrong x | facing spreads | read page bounds from `document.inspect` |
| `script --keep-going` exit 0 but things missing | errors recorded in results; file saved anyway; failed steps' `$N` refs cascade | grep results for `"error"`, fix the **first** one, rerun without `--keep-going` |
| Second `--export` has bleed/marks too | `--pdf-options` is sticky | `--pdf-options '{}'` before the next export |
| Control port: `{"ok":false,"error":"bad JSON … closing the connection"}` | non-JSON line | reconnect; send one JSON object per line |

Recovery rules: fix one thing per retry; after a failed step earlier steps are already applied in
that session (script: nothing is saved, rerun the whole script — it is deterministic). In MCP/app
sessions use `edit.undo` or `document.inspect` to see the real state before retrying; a failed
connected request is not resent and may have completed.

# Architecture

```
intent → workflow → operation → route (MCP headless | CLI | MCP bridge)
       → [MCP: automation roots gate] → session (docs, history, jobs) | one-shot CLI process
       → engine command registry (924 ids, params doc, enabled/disabledReason)
       → document (layers, masks, adjustments, smart objects/filters, type, shapes, styles)
       → inspection + preview → validation → artefact (.pcraft/.psd + flat export)
```

- **Registry**: every menu action is a command id (`namespace.group.name`). MCP `command_list` and CLI `commands --json` return the same list and docs; only MCP reflects the open document in `enabled`.
- **MCP headless** (`photocraft-cli mcp --automation-read-root R --automation-write-root W`): persistent session with several documents (`session_list`, `doc_select`), one history step per command, background jobs.
- **CLI**: each call opens → runs → saves; no roots; `batch`/`droplet` for folders.
- **serve**: same session model over JSON lines on stdio or `127.0.0.1:<port>`; methods `engine.execute {command, params}`, `doc.*`, `jobs.*`, `session.list`, `batch`, `methods`.
- **Bridge**: `photocraft --control <port> --control-token-file F` + `photocraft-cli mcp --bridge 127.0.0.1:<port> --control-token-file F`; adds `ui_*`, previews become window screenshots. Not verified.
- Native format `.pcraft` (lossless). `.psd` written by PhotoCraft and reopened by PhotoCraft kept type layers, adjustment layers, layer effects and smart filters; layer ids changed and opacity was 8-bit quantised (0.5 → 0.502). Compatibility with Adobe Photoshop is not verified.
- Layer ids are stable within a session/run, **not** across save/reopen — re-read ids from `doc_inspect`/`info` after reopening.

# Architecture (what matters for the agent)

- One Rust engine behind the desktop app (0.16.0), the CLI and the MCP server (both `vectorcraft-cli` 0.15.0).
- Every action is a command in one registry (802 in 0.15.0): menus, CLI `run --cmd`, MCP `command_run` and the dedicated tools all end there. Dedicated tools (`draw_shape`, `export`…) are wrappers that batch a few commands into one undo step.
- MCP server = `vectorcraft-cli mcp`. With `--automation-*-root` it is **headless**: an in-process session that lives as long as the server; several documents can be open; `file.new`/`open_file` switch the active one (`document.activate {index}` to go back).
- CLI `run` = a fresh headless session per invocation; selection does not survive between runs, but object ids of the same saved `.vectorcraft` are stable across runs.
- Live = the app started with `--control <port>` + server `--connect`; tool calls drive the real window. Not configured.
- Rendering is CPU (vello_cpu). Saves are atomic. Undo is unlimited.
- One call at a time; per the upstream docs (not observed here) a call running > 2 s makes new requests fail with `-32003 busy` (retry later).
- Session state that leaks between steps and documents: selection, current layer, **default paint for new art** (fill, stroke, weight, cap, dash: M31), current tool, recent colours. `select.none` + `paint.default` resets the paint (regression test M31); explicit paint per object does the rest.

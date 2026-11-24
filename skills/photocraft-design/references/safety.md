# Safety

## Files
- Outputs go to new paths (e.g. `<name>-edit.pcraft`, `out/`). Check `test -e` before CLI `convert`/`run --out` and before MCP `doc_export`; all overwrite silently.
- Never call `doc_save` without `path` unless the user asked to update that file.
- Batch: `--out` must be a new folder; never pass `--in-place` unless asked.
- Don't experiment on the user's files; copy to a scratch folder inside the root first.

## Roots (MCP / serve)
- Configured root here: `~/photocraft-work` (read and write). It holds real projects — touch only the files the task is about.
- Rejected: absolute paths outside, `..`, symlinks that lead outside. Without roots the server grants no file access at all.
- Don't widen the roots (e.g. to `~`) for convenience; copy the asset into the root instead, or use the CLI on that exact file.

## CLI
No sandbox: it reads/writes anything the user can. Use explicit paths, never globs over home directories.

## Bridge / live app
Only start `photocraft --control <port>` / `mcp --bridge` when the user asks. Prefer `--control-token-file` over `--control-token` (keeps the token out of `ps`). Stop it when done. Listener binds 127.0.0.1.

## Untrusted inputs
- Actions (`.atn`, actions JSON), droplets and `file.scripts.browse` run arbitrary command sequences; `file.scripts.scriptEventsManager` binds scripts to events. Read them before running.
- PSDs from others: read `doc_open` warnings (missing fonts, links).
- Don't put secrets in filenames, layer names or `file.fileInfo` metadata.

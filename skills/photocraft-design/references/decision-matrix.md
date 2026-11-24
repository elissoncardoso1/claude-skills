# MCP or CLI

Both run the same engine and the same 924-command registry with identical `params` docs. They differ in state, file access, preview and safety.

| Situation | Use | Reason |
|---|---|---|
| Several dependent edits, needs inspection/preview between steps | MCP | persistent session, stable layer ids, `render_preview` |
| "Is this command available right now?" | MCP `command_list {filter, enabled_only:true}` with the doc open | `enabled`/`disabledReason` reflect the live doc; CLI `commands` has no doc, so nearly everything shows disabled |
| Single deterministic transform / format conversion | CLI `run` / `convert` | one reproducible line; any failing `--cmd` aborts without writing `--out` |
| Many files with the same treatment | CLI `batch` | continues past failures, prints `ok`/`FAIL`, exit 1 if any failed |
| Input or output outside `~/photocraft-work` | CLI, or copy into the root and use MCP | MCP rejects paths outside the root |
| Long filter with progress/cancel | MCP `command_run {wait:false}` + `jobs_list` / `jobs_cancel` | CLI always waits |
| Operate the visible app window | MCP bridge (`ui_*`) | only when the user started the app with `--control`; not verified |

## Path rules

- MCP: paths relative to the root (`_project/in/photo.jpg`) or absolute inside it. `..`, absolute paths outside, and symlinks leading out are rejected.
- CLI: any path the OS user can reach. Be deliberate.

## Mixing routes

Fine to do it: e.g. CLI to convert/prepare inputs into the root, MCP to compose and preview, CLI `info` (scripts/pc_summary.py) to audit outputs. A file saved by MCP is just a file to the CLI.

## Exit codes (CLI)

0 success · 1 command/file error (or any batch failure) · 2 bad flag for the subcommand.

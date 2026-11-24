# designcraft-cli reference (0.17.2)

`designcraft-cli <sub> --help` prints that subcommand's usage line (exit 0); an unknown subcommand
prints the full usage and exits 1 [O]. Errors go to stderr as `designcraft-cli: <message>` [O].

| Subcommand | Syntax | Notes |
|---|---|---|
| `run` | `run [--in FILE \| --sample] [--cmd ID[=JSON]]... [--page N] [--scale S] [--pdf-options JSON] [--export OUT] [--all-pages DIR]` | Arguments processed **in order**. Each `--cmd` prints its non-null result as one JSON line [O]. `$N.path` refers to earlier `--cmd` results [S]. |
| `script` | `script [FILE\|-] [--in FILE \| --sample] [--connect PORT] [--save OUT] [--export OUT]... [--keep-going]` | Main automation entry. Prints `{"completed", "results"}` (+`failedIndex`,`failedCommand`,`error`); exit 1 on failure [O]. |
| `commands` | `commands [FILTER]` | JSON array `{id,label,menu,params,shortcut,enabled}`. FILTER matches id, label, menu **and params text** [O]. |
| `describe` | `describe COMMAND` | One entry; unknown → `no command \`x\``, exit 1 [O]. |
| `app` | `app [--port PORT] COMMAND [JSON]` / `app [--port PORT] --method METHOD [JSON]` | Running desktop app only; default port 7979 [S]. |
| `mcp` | `mcp [--connect PORT] [--sample] [--automation-read-root DIR]... [--automation-write-root DIR]...` | See mcp.md. Roots + `--connect` → error, exit 1 [O]. |
| `validate-pdf` | `validate-pdf FILE.pdf [--standard x4\|x1a]` | JSON `{valid, issues, standard, warnings}`; exit 1 when invalid [O]. |
| `thumbnail` | `thumbnail FILE.designcraft OUT.png [SIZE]` | Saved first-page preview, longest side ≤ SIZE [O]. |
| `perf`, `bench` | `perf [--pages N] [--runs N] [--strict]`, `bench FILE [--runs N]` | Developer benchmarks [D]; not needed for design work. |
| `links`, `--version` | | Community links; version string [O]. |

## run

- `--in` accepts `.designcraft` and `.idml` (IDML opened with `file.openIdml`) [S][O]. Missing file →
  `No such file or directory (os error 2)`, exit 1 [O].
- Without `--in`/`--sample` the document is the empty Letter one [S].
- `--export OUT` by extension: `.png .jpg` (one page: `--page N`, 0-based, default 0), `.pdf`,
  `.designcraft`, `.idml`, `.epub`, `.pptx`, `.html`, `.rtf`/`.txt` (current/selected story) [O][S].
  No extension → PNG. Other extensions → error before anything runs, exit 1 [O].
- `--scale` default **1.0** (1 px per point) [S][O]. `--all-pages DIR` writes `DIR/page-001.png`… [O].
- `--page/--scale/--pdf-options` apply to all following exports and **stay in effect** until given
  again (`--pdf-options '{}'` resets) [O]. Trailing option with no export after it → error [O].
- `--pdf-options` takes the `file.exportPdf` params (`bleed`, `marks`, `standard`, `pages`, …) [O].

```sh
designcraft-cli run --in doc.designcraft --cmd document.inspect > inspect.json
designcraft-cli run --in doc.designcraft --scale 0.5 --all-pages review/ --export doc.pdf
designcraft-cli run --in doc.designcraft --pdf-options '{"standard":"x4","bleed":true,"marks":true}' --export print.pdf
```

## script

Syntax (also printed by `script --help`) [O][S]:
```
command.id {"param": 1}          # also command.id={json} or bare command.id ; # and // comments
{"command": "command.id", "params": {...}}     # JSON lines, or a JSON array of these
```
- References: `"$N.path"` = value from result of step N (0-based, comments/blank lines not counted);
  `"$last"`; `"${N.path}"` interpolates in longer strings; `$$` = literal `$`. Referencing a step that
  hasn't run → `` `$5.id`: step 5 hasn't run (only 0 have) `` [O].
- Text params: `\n` new paragraph, `\u2028` forced line break, `\t` tab; `\ue000` = current page
  number marker (use on parent pages) [O][S `doc/src/story.rs`].
- Invalid JSON → `line N: <serde error>`, exit 1, nothing runs [O].
- **Unknown params are rejected** (`unknown parameter \`x\`; the command takes: …` or `did you mean`)
  — the help text's claim that most commands ignore them is stale (string still in the binary) [O][S].
- `--in F` opens F as the active document (no extra empty doc becomes active); `--save NEW` writes
  the edited document to NEW and leaves F unchanged [O].
- Steps run until the first failure; earlier steps stay applied (in memory). Without `--keep-going`,
  `--save/--export` run **only if all steps succeed** [S].
- `--keep-going`: failures become `{"error","command"}` results; **exit 0** anyway, and `--save`/
  `--export` **still run** on the partial document [O][S]. A failed step has no `id`, so later `$N`
  references to it fail too (`` `$2.id`: no `id` in {...} ``) and can hide later real errors — use
  `--keep-going` only for diagnosis; fix and rerun without it [O].
- `--save OUT` = Save As (`file.saveAs`); `--export X.designcraft` = save a copy [S].
- `--export` image = **page 1 only at 2× scale** (`app.export`) [S][O]. For other pages use
  `run --in saved.designcraft --page N` or `--all-pages`.
- Export warnings (e.g. missing alt text, PDF/X colour issues) go to stderr as `warning: …` [O].
- `--connect PORT` runs the steps in the desktop app (see control-channel.md); `--save` works there too [O].

## Exit codes [O]
0 success · 1 any error (bad args, failed step, invalid PDF, missing file). `--keep-going` → 0.

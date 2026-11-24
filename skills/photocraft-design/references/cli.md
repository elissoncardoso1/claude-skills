# photocraft-cli

Help for any subcommand: `photocraft-cli <sub> --help`. Unknown flag → exit 2.

```bash
photocraft-cli --version
photocraft-cli info <file> [--compact]                       # JSON: width,height,mode,depth,layers[],warnings
photocraft-cli commands [--json] [--filter <text>]           # registry (matches id and label)
photocraft-cli convert <in> <out> [--format ext] [--quality 1-100] [--tiff-layers]
photocraft-cli run (<file> | --new '<json>') --cmd <id> [--params '<json>'] [--cmd …] [--out <file>]
photocraft-cli batch --actions <actions.json|set.atn> [--action name] --in <dir> --out <dir> [--format ext] [--quality n] [--in-place]
photocraft-cli droplet <file.pcdroplet> <file-or-dir>… [--out dir]
photocraft-cli mcp | serve …                                 # servers; see architecture.md
```

## `run`
- Commands execute in order; each `--params` belongs to the preceding `--cmd`. One JSON line per command: `{"command","result"}`.
- Without `--out` nothing is written — use it for queries (`type.fonts`, `document.sampleColor`, `layer.list`, `type.info`).
- If any command fails, the process exits 1 and `--out` is **not** written.
- `run` also takes `--format` and `--quality 1-100` (JPEG/WebP); pass `--quality` explicitly — the default is not documented.
- Output format = `--out` extension. `.pcraft`/`.psd` keep layers; png/jpg/webp flatten (warning on stderr).
- Selection, undo and history exist only inside one invocation.
- Quote JSON with single quotes in the shell.

## `convert`
Flatten warnings go to stderr: `N layer(s) flattened; layers, masks and blend modes are not kept`, `lossy compression`, `resolution (DPI) not supported` (WebP). WebP without `--quality` is lossless. Overwrites the target silently.

## `batch` actions file
A JSON list of `[id, params]` pairs, `{"command": id, "params": {…}}` objects, or bare ids; also `{"actions": …}` / `{"steps": …}`, or a Photoshop `.atn` set with `--action <name>`.

```json
[["image.imageSize", {"width": 1080}], ["layer.newAdjustmentLayer.vibrance", {"vibrance": 20}]]
```
Output: `ok    in/a.png -> out/a.jpg` / `FAIL  in/b.png: <reason>`, summary `N succeeded, M failed`, exit 1 if any failed. `--out` equal to `--in` is refused unless `--in-place`.

## Verify outputs
`python3 scripts/pc_summary.py <file>` (wraps `info`), then view a PNG export with the Read tool.

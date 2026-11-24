# Choosing MCP headless, CLI or live

```
1. Needs the app window / panels / real keyboard?   → live. Not available with the current config (roots force headless).
                                                       Tell the user; only enable if they ask (see bottom).
2. Input outside the MCP read root(s)?              → ask: copy it into a read root (MCP) or use the CLI with output next to it (new name).
   MCP writes only under its write root(s): create a subfolder per project there (Bash `mkdir -p`; export does not create folders).
   The roots are this machine's: `scripts/vc_preflight.py` prints them from the MCP configuration (never assume a path).
3. Same transformation on many files?               → CLI loop, after one verified sample.
4. Plain format conversion?                          → CLI convert.
5. Create/edit iteratively and look at it?           → MCP headless.
6. Tie                                               → MCP (sandboxed, has previews).
```

| | MCP headless | CLI | live |
|---|---|---|---|
| state | session: docs, ids, selection, default paint, history | one `run` only | app document |
| preview | `screenshot`, `render_preview` | export PNG + Read | + window |
| file access | roots only | anything (careful) | app's own roots |
| reproducible | medium: session paint leaks (M31) unless each recipe resets it | high: byte-identical with `SOURCE_DATE_EPOCH` (references/reproducibility.md) | low |
| best for | creation, editing, inspection | batch, conversion, pipelines | UI-only features |

Mixing: build in MCP, save `.vectorcraft` inside the root, then batch-export with the CLI — fine. Do not assume a command behaves the same in all three without checking (live has extra `view.*`/`window.*`).

Enable live (only on request): start `/Applications/VectorCraft.app/Contents/MacOS/VectorCraft --control 7979 --automation-read-root D --automation-write-root D`, register a second server `vectorcraft-cli mcp --connect 127.0.0.1:7979` (roots + connect is an error). App is 0.16.0, CLI 0.15.0. The port has no auth: stop when done. The tool error suggests just `vectorcraft --control 7979`; that also works, but without roots the app is unconfined — prefer the command above.

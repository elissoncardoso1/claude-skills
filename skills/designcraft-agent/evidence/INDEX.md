# Evidence index (designcraft-cli 0.17.2, macOS 27.2 arm64, 2026-11-05)

Full investigation lives beside the skill in the project folder (`../research/`, `../experiments/`,
`../evidence/`). Files kept here:

| File | What it proves |
|---|---|
| `commands-0.17.2.json` | Registry snapshot (547 commands, headless) for version-drift diffs |
| `mcp-tools-0.17.2.json` | MCP `tools/list` (26 tools, schemas) |

Key observations and where they were made (experiment folders under `../experiments/`):

| Claim | Evidence |
|---|---|
| `type.char` after `frame.create` is a silent no-op; `selection.set`/`text.select` fix it | `mcp/tc.dcs`, `tc.png` |
| unknown params rejected despite help text | `t02` error log; `../evidence/rea/strings-checks.md`; source `engine/src/cmd/params.rs` |
| Inter Bold → SemiBold substitution | `t02/out.json` font.list |
| align enum (`leftJustified`, not `justify`) | `t02` first-run error |
| `object.setLayer` needs layer id | `t03` first-run error |
| facing default, spread math, parent folios `\ue000`, autoflow adds pages | `t04` |
| new objects on active (possibly hidden) layer; arrange; fit; units don't change coords | `t06` |
| setText keeps formatting | `t06b.png` |
| exports png/jpg/pdf/idml/html/epub/pptx; idml reopens | `t03`, `t05`, `t07` |
| `--pdf-options` sticky; bleed/marks boxes | `t07` |
| PDF/X-4 valid flyer | `wf/flyer-print.pdf` |
| keep-going exit 0, ref errors, roots | `t05` |
| control channel, connected MCP, screenshot | `control/` |
| default scales 1/2 | source `mcp/src/headless.rs`, `apps/designcraft-cli/src/main.rs` |

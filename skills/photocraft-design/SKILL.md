---
name: photocraft-design
description: Edit images and build graphic designs with PhotoCraft (Photoshop-like editor) through its MCP server (mcp__photocraft__*) or photocraft-cli. Use when the user asks to resize, crop, reframe, color-correct, retouch, add text/titles, compose social posts or banners, apply filters, mask, export PNG/JPG/PSD/.pcraft, or batch-process images with PhotoCraft — or mentions PhotoCraft, .pcraft, photocraft-cli. Covers choosing MCP vs CLI, discovering engine commands live, non-destructive editing, inspection and visual verification.
---

# PhotoCraft design

Turn design requests into verified PhotoCraft operations. Investigated against photocraft-cli **0.12.0 (6a2d027ee)**; if `photocraft-cli --version` differs, trust the live registry over these notes.

## Core loop

```
request → inspect assets → name the intent → split into operations
→ look up capability (references/capabilities.md) → pick MCP or CLI (references/decision-matrix.md)
→ discover the command + read its params LIVE → run ONE step
→ inspect structure + render preview → judge → fix or continue
→ save editable + export → report
```

## Non-negotiable rules

1. **Never invent command ids or param keys.** Find them with `command_list {filter:"<word>"}` (MCP) or `photocraft-cli commands --json --filter <word>`. Use only keys that appear in the `params` doc.
2. **Always verify after each command.** The engine silently ignores unknown keys and clamps out-of-range values (`imageSize {width:-5}` → 1×1, success). Check returned values, `doc_inspect`/`photocraft-cli info`, and a preview.
3. **Inspect before editing** an existing file: size, mode, depth, layer tree, text layers, selection, warnings.
4. **Never write over originals.** Always pass an explicit new output path. `doc_save` without `path`, `doc_export`, `convert` and `run --out` all overwrite silently. Check the target does not exist first.
5. **Prefer editable over destructive**: `layer.newAdjustmentLayer.*` over `image.adjustments.*`; `doc_place` (smart object) over pasting pixels; `filter.convertForSmartFilters` before filters; masks over erasing; keep text as Type layers. Save `.pcraft` or `.psd` alongside any flat export.
6. **Work incrementally**: one change → inspect → preview → next. Use `command_batch` only for steps already proven, and remember it has no rollback.
7. **A success result is not a good design.** For subjective goals, look at the preview, name concrete problems, change one thing, look again, and say the judgement is visual.
8. **Diagnose errors, don't retry blindly.** Read `disabledReason` / the error, fix the state. See references/troubleshooting.md.

## MCP vs CLI (short version)

- **MCP** (`mcp__photocraft__*`, headless): multi-step/iterative work, previews (`render_preview`), checking what is enabled *now*, long filters as jobs. Paths are **relative to the automation root** (`~/photocraft-work` here); files elsewhere must be copied in.
- **CLI** (`photocraft-cli`): one-shot conversions, deterministic transforms, scripts, **batch** of many files, files outside the root. No sandbox, no preview — export a PNG and view it.
- `ui_*` / `control_call` need bridge mode (live app). Don't start it unless the user asks.

## Quick facts that prevent mistakes

- Bounds: `info`/`doc_inspect`/`shape.create rect` = `[x,y,w,h]`; `type.*` bounds and `edit.transform rect` = `[x0,y0,x1,y1]`.
- `layer.setProps` opacity 0..1; layer styles/fill opacity 0..100. CLI/MCP save quality 1..100; export commands' `quality` 0..12.
- `type.create` x,y is the text **baseline**; `align:"center"` makes x the centre; character keys (`font`, `fontStyle`, `size`, `color`, `tracking`…) are those of `type.setStyle`. A missing font only produces a warning (CLI exit 0): stop, offer installed alternatives, ask the user.
- Fonts: list families with `photocraft-cli run <any image> --cmd type.fonts` (no params → `{families}`, ~10 KB). Avoid `type.fonts {family}` over MCP: it repeats faces (1470 rows for 14 faces) and can overflow output. Unknown family → `{faces:[]}`.
- Change aspect ratio with `image.crop {…, targetWidth, targetHeight}` or `image.canvasSize`; `image.imageSize` with both sides distorts. Default: photos → crop around the subject; layouts with elements near the edges → pad with `canvasSize`. State the choice in the report; ask only if both would lose something the user cares about.
- Filters take no `layer` param — they act on the active layer. `filter.convertForSmartFilters` returns a **new layer id**. Filters need a pixel layer or smart object.
- Mask commands consume the active selection.
- `doc_save {path}` retargets the open document to that path; later saves without a path go there, not to the original.
- Files outside the MCP root: confirm with the user before touching them with the CLI, and say where outputs will go (default: a new file next to the original, never over it).

## When to read the references

| Need | Read |
|---|---|
| Decide MCP or CLI, path rules | references/decision-matrix.md |
| Map an intent to commands + how to verify | references/capabilities.md |
| MCP tool list and return shapes | references/mcp.md |
| CLI subcommands, batch actions format | references/cli.md |
| Step-by-step design workflows | references/workflows.md |
| Paths, roots, overwrite, bridge, untrusted files | references/safety.md |
| An error or surprising result | references/troubleshooting.md |
| How the pieces fit (session, registry, jobs) | references/architecture.md |

`scripts/pc_summary.py <file>` prints a compact structural summary (size, mode, layers with kind/bounds/text/adjustment/smart filters, warnings) via `photocraft-cli info` — use it to verify CLI outputs. `examples/` has a worked social-post (MCP) and a batch (CLI).

## Report

End with: inputs, operations run (tool + command ids + key params), output paths (editable + exported), warnings, what was verified structurally vs visually, and anything left unverified.

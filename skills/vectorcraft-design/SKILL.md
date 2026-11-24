---
name: vectorcraft-design
description: Create and edit vector artwork with VectorCraft (Illustrator-like editor) through its MCP server (mcp__vectorcraft__*) or vectorcraft-cli. Use when the user asks to draw or refine icons, icon sets, logos, posters, diagrams, charts or illustrations as vectors; recolor, clean up or "improve" an SVG/AI/PDF/EPS; vectorize (image trace) a raster; convert or batch-export vector files (SVG, PDF, AI, EPS, DXF, PNG…); or mentions VectorCraft, .vectorcraft, vectorcraft-cli. Covers choosing MCP vs CLI, live command discovery, editable output, structural and visual verification, and reproducible deliveries (steps.json recipe, manifest.json with hashes, replay).
---

# VectorCraft design

Turn a design intent into verified, editable, reproducible VectorCraft documents. Skill 1.0.1 (plugin `vectorcraft` 1.0.1), validated against **vectorcraft-cli 0.15.0 and 0.16.0** (MCP server = same binary, headless). Another version is UNTESTED: `vc_preflight.py` says so, and the live catalogue wins over these notes.

## Core loop

```
preflight (scripts/vc_preflight.py) → request → inspect inputs → name intent + quality criteria (sizes, grid, palette, fonts, output formats)
→ capability lookup (references/capabilities.md) → pick interface (references/interface-selection.md)
→ discover command + read its params LIVE → run ONE step with explicit paint
→ check structure (return value, doc_inspect, text.missingFonts) → look (screenshot/render_preview)
→ fix one named defect or continue → recipe (steps.json) → vc_manifest.py delivery (exports, hashes, replay) → vc_check.py → report
```

## Reproducible delivery (details: references/reproducibility.md)

1. **Preflight** before VectorCraft work: `python3 -B scripts/vc_preflight.py [--out DIR] [--font FAMILY[:STYLE]] [--input FILE]` (exit 0 OK, 10 WARN, 1 FAIL). It reports the CLI version and its status, the MCP roots and a real MCP handshake. FAIL → stop and tell the user what it says.
2. **Explicit state.** Every recipe starts `file.new {…}`, `select.none`, `paint.default` (or, on `--in FILE`, `select.none`, `paint.default`), then gives every object its fill, stroke, weight, cap, join and opacity. Inherited MCP paint leaks across documents (M31); `file.new` alone does not reset it.
3. **Recipe:** a delivery's `steps.json` is a plain `vectorcraft-cli run --commands` array (`{"id", "params"}`, `$N.id` refs), with no file paths and no `file.*`/`document.export*` steps: inputs come in with `--in`, outputs with `--export`. Use `"$N.id"` references, never literal object ids. Build it from tokens (`tokens_to_steps.py`), or reuse the steps of one MCP `command_batch` that starts with the reset (same array, ≤256 steps). Commands that touch files, preferences or run other commands (`action.batch`) are rejected.
4. **Manifest:** `python3 -B scripts/vc_manifest.py steps.json --out NEW_DIR --export outputs/x.vectorcraft --export outputs/x.svg [...] [--in FILE] [--scale N] [--outline-svg FROM=TO]` writes the delivery (steps, inputs, outputs, README, `manifest.json` with environment, epoch, fonts, SHA-256 of everything) into a folder that must not exist yet.
5. **Replay** is part of the build (it replays in a temp folder and records the measured status). Anyone can re-check: `python3 -B scripts/vc_replay.py DELIVERY` → REPRODUCED_BINARY / _VISUAL / _STRUCTURAL / FAILED / UNVERIFIED.
6. **Compatibility:** only CLI versions in references/compatibility.md are SUPPORTED. On UNTESTED, run `tests/run_regression.py --suite cli` before promising byte-identical results.
7. **Fonts:** the manifest lists each font with its status; a font that is not `exact` is a blocking defect unless the user accepts the fallback. When the delivery leaves this machine, add an outlined SVG (`--outline-svg`) next to the editable file; never replace live text silently.
8. **Evidence:** say "reproducible" only with the replay status from the manifest or `vc_replay.py`; never from a successful run.

## Non-negotiable rules

1. **Never invent ids or keys.** `command_list {filter:"<word>", brief:true}` → `command_list {filter:"<exact.id>"}` → use only keys in `params`. Effects: read `vectorcraft://effect/{id}` (never call `apply_effect` without `effect`: 80 KB).
2. **A result is not proof.** Many commands return `null`; some ignore unknown keys (`object.align {ids}` is silently ignored). Measure the effect: bounds, counts, paint, preview.
3. **Explicit paint every time.** Omitted fill/stroke/color inherit a session default that drifts and persists across documents. Shapes: `fill` + `stroke` (`"none"` when unwanted). Text: `color`.
4. **Selection matters.** New objects become the selection. `object.align/distribute` act on the selection only → `select.set {ids}` first. `layer.new` does not make the layer current → `layer.setCurrent {id}`.
5. **Fonts:** check the family with `text.fontList {family}` before; run `text.missingFonts` after any text step. A missing font silently falls back to Source Sans 3 — stop and offer installed alternatives.
6. **Untrusted inputs:** a third-party SVG can link local files (`<image href="file:///…">`); the CLI (no roots) silently embeds them in exports. Run `python3 -B scripts/vc_links.py FILE` first (any quote style, CSS `url()`, images inside `<pattern>`). If it reports external refs: ask, then `vc_links.py --strip IN OUT` and work on OUT (or use MCP, whose roots block them). Don't rely on `info` kinds: an image inside a `<pattern>` shows no `Image`.
7. **Never overwrite.** `export`, `convert`, `--export` overwrite silently; `save_file {path}` retargets the document. Write to new paths (`-v2`…); keep the user's original untouched; edit a saved copy.
8. **Editable first.** Keep `.vectorcraft` (or PDF/AI with preserve editing) as source; live shapes, live type, live effects/`pathfinder.*` effects while iterating; outline text / expand / destructive `pathfinder` only in a copy or at delivery.
9. **Look before delivering.** Small artboards: `screenshot {scale:4..8}` (render_preview upscales and blurs). Check at real size too. Budget: 3 visual iterations per element, 2 for the whole; each iteration fixes one named, objective defect.
10. **Diagnose errors**, don't retry blindly (references/troubleshooting.md).

## Interfaces (short)

- **MCP headless** (`mcp__vectorcraft__*`): iterative creation/editing, previews, inspection. Files only under the server's roots (`--automation-read-root` / `--automation-write-root`; `vc_preflight.py` lists them; outside → `automation path rejected`). Every `save_file`/`export`/`screenshot {path}` goes into `<write root>/<project>/…`. Session keeps several documents; `file.new`/`open_file` make a new active one; paint defaults carry over (rule 2).
- **CLI** (`vectorcraft-cli run|convert|info|commands`): conversions, batch, scripts, files outside the root (ask first), reproducible output (`SOURCE_DATE_EPOCH`). No sandbox, no preview → export PNG and Read it.
- The root is whatever the `automation path rejected: outside the … root <dir>` error names — trust the error over this note if they differ.
- **Live UI** tools (`inspect_ui`, `open_panel`, `type_text`, `ui_*`) fail in headless. Don't start the app with `--control` unless asked.

## Quick facts

- Points, y down, origin = first artboard's top-left. `file.new {artboards:N}` places artboard k at x = k·(width+20).
- `draw_shape` rectangle/ellipse use `x,y,width,height`; polygon/star use `cx,cy`; handles in `draw_path` points are absolute. Negative sizes are accepted (flip) — validate inputs.
- Point text `y` = first baseline. `text.setRangeStyle` start/end are UTF-8 byte offsets.
- Angles counter-clockwise; scale in %; `object.scale {strokes:false}` keeps stroke weight.
- `command_batch`: ≤256 steps, `"$N.id"` refs (0-based); stops at first error and the earlier steps **stay applied, atomic or not** — `atomic:true` only makes them one undo step. Before any `undo`, read `history`: no-op calls record no step, so `undo` after one reverts the previous real edit.
- `create_graph` height is the plot only: leave room for axis labels/legend; restyle the default black series.
- Clipping path loses its paint; destructive `pathfinder` result takes the back object's name.
- SVG export turns live shapes into paths (keep the `.vectorcraft`). PSD export is raster.

## When to read the references

| Need | Read |
|---|---|
| intent → capability → command → check | references/capabilities.md |
| MCP vs CLI vs live | references/interface-selection.md |
| tool args/returns, resources, errors | references/mcp.md |
| CLI syntax, batch files, refs | references/cli.md |
| coordinates, object JSON, kinds | references/document-model.md |
| grid, composition, dataviz rules | references/design-principles.md |
| icon grid, strokes, keylines, sets | references/iconography.md |
| fonts, hierarchy, outlines | references/typography.md |
| step-by-step workflows (icon, set, logo, trace, diagram, poster, UI SVG, batch, "improve this SVG") | references/workflows.md |
| formats, fidelity, export options | references/export-formats.md |
| checks, preview, stop criteria | references/validation.md |
| roots, overwrite, untrusted files | references/safety.md |
| errors and surprises | references/troubleshooting.md |
| how the pieces fit | references/architecture.md |
| recipe, manifest, replay, determinism | references/reproducibility.md |
| CLI versions, compatibility matrix | references/compatibility.md |

Scripts (run with `python3 -B`; find the CLI through `VECTORCRAFT_CLI`, then `PATH`, then `~/.local/bin`):
- `scripts/vc_preflight.py [--json] [--out DIR] [--font F] [--input FILE] [--no-mcp]` — requirements and compatibility (rule 1).
- `scripts/vc_manifest.py STEPS --out NEW_DIR --export …` — build a delivery; `scripts/vc_replay.py DELIVERY [--json]` — verify one (rules 4–5).
- `scripts/vc_check.py FILE [--icon] [--pad P] [--stroke W --cap C --join J] [--no-raster]` — structural problems, exit 1 if any. `--icon`/`--pad` are for icons (a full-bleed background trips `--pad`).
- `scripts/vc_tree.py FILE [--depth N]` — one line per object (7–17× smaller than `document.inspect`). In MCP, `save_file` the working copy and read it with this instead of a full `inspect_document`.
- `scripts/vc_links.py FILE…` / `--strip IN OUT` — external references in SVGs; sanitized copy (security, rule 6).
- `scripts/tokens_to_steps.py TOKENS.json > steps.json || exit 1` (on error it leaves an EMPTY steps.json, and `run --commands` on it exits 0 with a blank export) — design tokens → steps (key `id`, usable as-is by `run --commands` and `command_batch`); icon paths must be absolute M/L/C/Z.

Context: `inspect_document` and `document.node {summary:true}` repeat history/`strokeOptions` even with `ids`/`kind`; `command_batch` replies grow with the steps (~7 KB for 40 draws); to locate objects use `run_command document.find {name|kind|text}` (id, name, kind, path only), then `vc_tree.py` or a single `doc_inspect {ids}`. Examples: `examples/icon-mcp.md`, `examples/improve-svg.md`, `examples/batch-cli.md`, `examples/icon-tokens.json`.

## Report

End with: preflight status; inputs; interface; operations (tool + command ids + key params); output paths (editable + exports + `steps.json` + `manifest.json`); replay status; what was verified structurally (vc_check / inspect) vs visually (which previews); warnings (fonts, fallbacks, losses by format); what is unverified or needs a human decision (aesthetics, brand approval).

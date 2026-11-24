---
name: designcraft-agent
description: Create, edit, inspect, lay out, render and export page-layout documents with DesignCraft (open-source InDesign-class app) through designcraft-cli (run/script), its MCP server, or the running desktop app's control channel. Use when the user asks to design or typeset a report, flyer, poster, magazine/editorial page, brochure, ebook, multi-page document or paginated presentation, place images and text frames, apply paragraph/character styles, threads text, export PDF / PDF/X / PNG / JPG / IDML / EPUB / HTML / PPTX, preflight or validate a PDF, or mentions DesignCraft, designcraft-cli, .designcraft files, diagramar/diagramação, relatório, revista, folheto, cartaz, ebook, exportar PDF para impressão.
---

# DesignCraft agent

Verified against **designcraft-cli 0.17.2** (macOS arm64, 2026-11-05). Every rule below was observed
on that build; see `evidence/INDEX.md`. On another version, run discovery first (step 0) and trust
the installed binary over this text.

## 0. Discover before you act (always)

```sh
designcraft-cli --version                  # compare with 0.17.2; if different read references/command-registry.md
designcraft-cli commands <word>            # search ids/labels/menus/params (JSON array)
designcraft-cli describe <command.id>      # exact params of ONE command — read it before first use
```
Never invent a command id or a parameter. Unknown params are **rejected** (error names the
accepted keys), so a failed call tells you how to fix it — read the message, don't guess twice.

## 1. Pick the interface

| Need | Use | Reference |
|---|---|---|
| Build/edit a file and export, reproducibly (default) | `designcraft-cli script FILE.dcs --save out.designcraft --export out.pdf` | references/cli.md |
| One-off command or export of an existing file | `designcraft-cli run --in F --cmd ID=JSON --export out.png` | references/cli.md |
| Iterative visual work from an MCP client (images come back) | `designcraft-cli mcp` (registered tools, or `scripts/dc_mcp.py`) | references/mcp.md |
| Drive the visible desktop app, window screenshots, dialogs | `DesignCraft --control 7979` + `mcp --connect 7979` / `script --connect` / `app` | references/control-channel.md |

## 2. Workflow: INSPECT → PLAN → CREATE/EDIT → RENDER → VERIFY → SAVE/EXPORT

1. **INSPECT** — existing file: `designcraft-cli run --in F --cmd document.inspect` (pages, spreads,
   items with ids/bounds, stories with overset, layers, styles, swatches).
2. **PLAN** — page size, margins, columns, grid; define paragraph styles and color swatches first;
   write coordinates in **points**, y down, per spread (references/document-model.md).
3. **CREATE/EDIT** — one script; later steps reference earlier results with `"$N.id"` / `"$N.story"`.
   Never hard-code ids you did not get back from a result or `document.inspect`.
4. **RENDER** — export PNGs of every page (`--all-pages DIR`, or `render_page`) and **look at them**.
5. **VERIFY** — `python3 scripts/dc_check.py out.designcraft --margins` (overset, font
   substitution, items past page edge, preflight), then fix and re-render. Command success ≠ good design.
6. **SAVE/EXPORT** — `.designcraft` + the requested formats; for print run
   `designcraft-cli validate-pdf out.pdf`. Inspect exported files (`pdfinfo`, render PDF pages).

## 3. Critical rules (each one bit during testing)

- **Text formatting needs a target.** `type.char`, `type.para`, `style.paragraph.apply` act on the
  current text selection or selected text frames. Right after `frame.create` nothing is targeted and
  the call **silently does nothing**. It returns `null` — but so does a successful call, so
  the return value proves nothing: verify with `type.selectionAttrs` (resolved attributes of the
  selected text) or a render. First `selection.set {"ids":["$N.id"]}` (whole
  story) or `text.select {"story":…, "anchor":…, "focus":…}` (byte range). references/typography.md
- **Text offsets are UTF-8 bytes**, not characters (é = 2, — = 3).
- **Fonts:** only bundled faces are guaranteed: Inter (Regular/Medium/SemiBold — **no Bold**),
  Source Sans 3 (`Regular`/`Italic`/`Semibold`/`Bold`), Source Serif 4 (`Regular`/`Italic`/`Semibold`/`Bold`/`Bold Italic`),
  JetBrains Mono Regular. Installed system fonts also work. A missing style is substituted silently;
  `font.list` / `dc_check.py` report it.
- **Paragraph align values:** `left|center|right|leftJustified|centerJustified|rightJustified|fullyJustified|towardsSpine|awayFromSpine` (not `justify`).
- **New objects go on the active layer** — hiding/locking that layer hides/locks them too.
  `layer.new` makes the new layer active and on top. `object.setLayer` takes the layer **id**.
- **Coordinates are always points**, even when `file.new` sets `units` (units affect UI only).
- **Facing pages are the default** for presets: page 2 starts spread 1 (left page). Use
  `"facingPages": false` for single pages, or compute right-page x as `pageWidth + x`.
- **Script/MCP sessions start with an empty Letter document** (index 0); `file.new` creates and
  activates a second one. `--save`/`--export` act on the active document. `script --in F` opens F
  as the active document; `--save NEW` writes the edited copy and leaves F untouched.
- **Default PNG scale differs:** `script --export` / `export_png` = 2× (1 px = 0.5 pt);
  `run --export`/`--all-pages` = 1× unless `--scale` and **include the bleed area**; `render_page` = 1× unless `scale`. `script --export x.png` writes **page 1 only**; use `run --in F --all-pages DIR` for all pages.
- **Overset is not an error to the engine.** Check `story.get` → `overset`/`oversetChars` or
  inspect `stories[].overset`; fix by `text.thread`, a bigger frame, or less text.
- `script --keep-going` exits 0 even when steps failed — scan results for `"error"`.
- Do not use UI-only commands (`view.*`, `window.*`, `help.*`) headless; they need the app.
- Ask before overwriting a user file; write experiments to a scratch folder. Don't leave the app's
  `--control` port open when finished (no authentication) — `app.quit` via `app --method app.quit`.

## 4. Routing

| Topic | File |
|---|---|
| Install, first document in 2 minutes | references/getting-started.md |
| CLI subcommands, flags, exit codes, script syntax | references/cli.md |
| MCP tools, headless vs connected, file-access roots | references/mcp.md |
| Desktop app control channel (JSON lines over TCP) | references/control-channel.md |
| Document model: documents, pages, spreads, parents, layers, coordinates, geometry | references/document-model.md |
| Frames, shapes, lines, paths, groups, align/distribute, z-order | references/frames-and-shapes.md |
| Text, styles, fonts, threading, overset, page numbers | references/typography.md |
| Swatches, colors, gradients, strokes, effects | references/styles-and-colors.md |
| Images: place, fit, resolution | references/images.md |
| Render, export, PDF options, PDF/X, preflight | references/export.md |
| Command registry, discovery, version drift | references/command-registry.md |
| Error messages → fixes | references/troubleshooting.md |
| Recipes: report, editorial/magazine, multi-page/ebook, poster/flyer, slides | references/workflows/ |

## 5. Verification checklist (before reporting success)

- [ ] Every page rendered to PNG and viewed; layout matches the brief.
- [ ] `dc_check.py` has 0 errors (no overset, no font substitution) and every warning is intended.
- [ ] Alignment/spacing consistent (shared x edges, equal gaps); hierarchy readable at page size.
- [ ] Margins respected unless bleed art is intended (bleed set in `file.new` or `layout.documentSetup`,
      art extended into it, exported with `bleed:true`).
- [ ] Exported files exist, open (`pdfinfo` page count/size) and look like the PNG renders.
- [ ] Report what was not verified or could not be done; never claim an unsupported feature worked.

## 6. When something fails

Read the error (it names valid keys, variants, swatches or the step index), fix one thing, rerun.
After two failed attempts on the same step, `describe` the command and search `commands` for an
alternative; see references/troubleshooting.md. If a capability is absent in the registry, say so.

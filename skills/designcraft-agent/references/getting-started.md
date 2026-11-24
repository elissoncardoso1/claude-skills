# Getting started

Status tags used in every reference: **[O]** observed on 0.17.2 · **[S]** confirmed in source
(`storytold/designcraft` @0e85e9e, workspace 0.17.0) · **[D]** official docs only · **[U]** unverified.

## Locate the CLI [O]

| Install | Path |
|---|---|
| Standalone (this machine) | `~/.local/bin/designcraft-cli` (on PATH) |
| macOS app bundle | `/Applications/DesignCraft.app/Contents/MacOS/designcraft-cli` (same version; desktop app binary is `.../MacOS/DesignCraft`) |
| Linux packages [D] | `/usr/bin/designcraft-cli` |

```sh
command -v designcraft-cli || ls /Applications/DesignCraft.app/Contents/MacOS/
designcraft-cli --version        # "designcraft-cli 0.17.2"
```
No license, login or network is needed for headless use [O].

## First document [O]

```sh
mkdir -p /tmp/dc && cd /tmp/dc
cat > hello.dcs <<'DCS'
file.new {"preset": "A4", "facingPages": false, "margins": 48}
style.paragraph.create {"name": "Title", "chars": {"fontFamily": "Source Sans 3", "fontStyle": "Bold", "size": 32}}
frame.create {"rect": [48, 48, 547, 120], "content": "text", "text": "Hello DesignCraft"}
selection.set {"ids": ["$2.id"]}
style.paragraph.apply {"name": "Title"}
frame.create {"rect": [48, 140, 547, 400], "content": "graphic"}
object.color {"color": "#1F4E79", "ids": ["$5.id"]}
DCS
designcraft-cli script hello.dcs --save hello.designcraft --export hello.pdf --export hello.png
python3 <skill>/scripts/dc_check.py hello.designcraft
```
Then open `hello.png` (page 1, 2× scale) and look at it.

## Mental model

- Every change is an engine **command** (`id` + JSON params). 547 commands headless on 0.17.2 [O].
- A **session** holds documents; the active one receives commands. Headless sessions start with an
  empty Letter document [O]/[S `Headless::with_document`].
- Results are JSON; creation commands return `{"id": N}` (frames also `"story": M`) [O].
- Exports write files; `.designcraft` is a zip (`document.json`, `meta.json`, `preview.png`,
  `assets/` with embedded placed images) [O].

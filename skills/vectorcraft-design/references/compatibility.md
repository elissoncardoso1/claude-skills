# Compatibility

| Item | Version |
|---|---|
| plugin `vectorcraft` | 1.0.1 |
| skill `vectorcraft-design` | 1.0.1 |
| recipe format | `vectorcraft-steps/1` |
| manifest format | `vectorcraft-delivery/1` |
| Python | ≥ 3.9 (tested 3.14.7) |

| vectorcraft-cli | Status | Evidence |
|---|---|---|
| 0.15.0 | SUPPORTED | `tests/golden/0.15.0/`, full regression suite (macOS 27 arm64, 2026-10-24) |
| 0.16.0 | SUPPORTED | `tests/golden/0.16.0/`, full regression suite incl. MCP (macOS 27 arm64, 2026-10-24); release zip SHA-256 checked against SHA256SUMS.txt, signed by the same team as 0.15.0 |
| any other | UNTESTED | `vc_preflight.py` warns (exit 10); run the suite, then add a row |

No version is INCOMPATIBLE yet. The desktop app ships without updating the CLI (separate `vectorcraft-cli-<v>-macos-universal.zip`). Only the CLI version matters for recipes and replays.

## Across versions (0.15.0 → 0.16.0, same recipes)

| Format | Same bytes? | Why |
|---|---|---|
| SVG, PNG, DXF | yes (S01–S03, S06, S07, S11) | no version recorded |
| .vectorcraft, PDF, EPS | no; REPRODUCED_STRUCTURAL | the file records `generator: VectorCraft <version>` (PDF/EPS through their editing data and document id) |

Catalogue: same 802 ids; one parameter change: `shapeBuilder.merge` gained `rect` (Shift-drag marquee) in 0.16.0. `--help` identical. M31 (paint leak in MCP) still present in 0.16.0. A delivery made with one version and replayed with the other reports REPRODUCED_STRUCTURAL, which is the expected result; for byte equality, replay with the CLI version named in the manifest.

## Testing a new CLI version

```bash
python3 -B scripts/vc_preflight.py --no-mcp                 # UNTESTED + catalogue drift (missing commands → FAIL)
python3 -B tests/run_regression.py --report new.json        # PASS_NO_BASELINE = expectations met; kinds compared with 0.15.0
python3 -B tests/run_regression.py --suite cli --update-golden   # only after reviewing new.json
```
Then add the version to `VALIDATED_CLI` in `scripts/vc_common.py` (or `INCOMPATIBLE_CLI` when the suite fails for a real reason), add a row above, and note it in the plugin CHANGELOG.

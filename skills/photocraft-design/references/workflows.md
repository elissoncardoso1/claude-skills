# Design workflows

Every workflow: originals untouched, one change at a time, preview between steps, save editable + export flat.

## Objective transform (resize, crop, convert)
1. `info` / `doc_inspect` → current size and ratio.
2. Same ratio: `image.imageSize {width}` (one side). Different ratio, keep framing: choose a crop rectangle with the target ratio around the subject → `image.crop {x,y,width,height,targetWidth,targetHeight}`; or keep everything and pad → `image.canvasSize {anchor:"center", extensionColor}`. Ask if it's unclear whether cropping is acceptable.
3. Write to a new path; verify dims; look at the result.

## Photo correction (non-destructive)
1. Inspect + preview; state the goal in words (e.g. "lift shadows, warmer, less saturated greens").
2. Global: `layer.newAdjustmentLayer.curves|levels|colorBalance|hueSaturation|photoFilter` → preview.
3. Local: make a selection (`select.*`), then create the adjustment layer — the selection becomes its mask. Or add `layer.layerMask.*` to an existing one.
4. Tweak with `layer.setAdjustment`; compare before/after (toggle `layer.setProps {visible}` and preview).
5. `doc_save` .pcraft/.psd + `doc_export` jpg/png.

## Social post / banner
1. `doc_new {width:1080, height:1350, background}` (or the user's size).
2. `doc_place` the photo (`center`, `scale`) → smart object.
3. Grade only the photo: adjustment layer + `layer.createClippingMask`.
4. Graphics: `shape.create`, `layer.newFillLayer.gradient` (scrims behind text for contrast).
5. Type: check `type.fonts {family}`; `type.create {x: W/2, y: baseline, align:"center", font, fontStyle, size, color}`; read `warnings`.
6. Align: `layer.align.horizontalCenters {to:"canvas"}`; check margins from `type.info`/`doc_inspect` bounds.
7. Preview at ≤1024 and judge: hierarchy, contrast/legibility, safe margins, balance. Fix one thing at a time.
8. Save `.pcraft` + export `.png`.

## Composite
Smart object contents: `layer.smartObjects.editContents {layer}` opens them as a new document (inspect it, e.g. that text is still a Type layer; not verified), `layer.smartObjects.saveContents` writes back.

Open base → `doc_place` each asset → position (`edit.transform {layer,dx,dy,scaleX,scaleY}` — not yet verified on smart objects; check bounds after) → masks for cut-outs → styles/smart filters → harmonise with clipped adjustments → preview.

## Batch
1. `info` on one sample; agree the treatment.
2. Prove it on one file: `photocraft-cli run sample --cmd … --out test.ext` → look at it.
3. Write `actions.json` with exactly those steps.
4. `photocraft-cli batch --actions actions.json --in IN --out NEW_DIR [--format --quality]`. Flat formats bake adjustment layers in; if the user wants to keep editing, run a second pass with `--format pcraft` into another folder.
5. Audit: count `ok`/`FAIL`, `pc_summary.py` on a few outputs, view 1–2. For colour treatments measure it: `document.sampleColor {x,y}` on the same point before and after. Report failures with reasons; don't silently retry.

## Subjective request ("make it better", "improve composition")
Preview → describe what you see → list specific problems with proposed command ids → apply one → preview → re-evaluate. Say clearly that the assessment is visual judgement and offer alternatives rather than claiming it is "fixed".

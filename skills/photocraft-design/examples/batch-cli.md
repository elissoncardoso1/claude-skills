# Example: same treatment on a folder (CLI) — executed 2026-10-22

```bash
photocraft-cli info batch-in/img1.png --compact            # inspect a sample
photocraft-cli run batch-in/img1.png \
  --cmd image.imageSize --params '{"width":540}' \
  --cmd image.adjustments.hueSaturation --params '{"saturation":-40}' \
  --out /tmp-or-out/test-one.jpg                            # prove on one file, then look at it
cat > actions.json <<'J'
[["image.imageSize",{"width":540}],["image.adjustments.hueSaturation",{"saturation":-40}]]
J
photocraft-cli batch --actions actions.json --in batch-in --out batch-out --format jpg --quality 80
#  FAIL  batch-in/broken.png: codec: unrecognized image format
#  ok    batch-in/img1.png -> batch-out/img1.jpg   (×3)
#  3 succeeded, 1 failed        exit=1
python3 scripts/pc_summary.py batch-out/*.jpg               # audit sizes
```
Flat JPG output, so the destructive `image.adjustments.*` is acceptable here; for editable outputs use `layer.newAdjustmentLayer.*` and `--format pcraft`.

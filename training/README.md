# Training / fine-tuning

Fine-tune TATR on labeled construction-schedule tables.

## Approach

Reuse the upstream training loop from microsoft/table-transformer rather than vendoring it. This directory holds:

- Dataset conversion scripts: our labeled schedules -> PubTables-1M-compatible format expected by TATR's trainer.
- Training configs (learning rate, freeze schedule, augmentations tuned for dense grids and small text).
- Checkpoint registry: which model was trained on which data, and its score on the eval set.

## Order of operations

1. Hit a stable eval baseline with stock TATR weights on the eval set.
2. Label ~200 table images (can be drawn from the same PDFs as eval, on DIFFERENT pages - no leakage).
3. Fine-tune structure-recognition head only first; detection head if needed.
4. Re-score on eval. Only keep checkpoints that beat the baseline.

Nothing in this directory is implemented yet.

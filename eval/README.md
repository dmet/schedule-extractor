# Evaluation set

Ground truth for measuring end-to-end extraction quality on real construction schedules. Build this BEFORE any fine-tuning - otherwise changes to the model or pipeline cannot be evaluated.

## Target size

- v0: 20 schedules, 2-5 pages each, hand-labeled.
- v1: 100+, covering varied contractors, templates, and schedule types (bar-chart, tabular, phased).

## Format

Each schedule has a paired JSON file matching schema.json:

eval/data/
  acme-tower-2024.pdf
  acme-tower-2024.json

The JSON captures the logical table (header tree + body rows) rather than cell bboxes, so it is robust to detector changes. Bounding boxes can be added later for detector-only eval.

## Metric

Two numbers per schedule, averaged:

- Header-tree F1: node-level match on (level, column range, text).
- Row-cell accuracy: cell-text match after header alignment.

Detector-level GriTS comes from the upstream TATR repo and is reported separately.

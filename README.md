# schedule-extractor

Domain-focused table extraction for complex construction schedules, built on Table Transformer (TATR): <https://github.com/microsoft/table-transformer>

## Why a separate project

TATR is a research codebase for general table detection and structure recognition. This project adds the pieces needed to extract usable data from construction schedules specifically:

- PDF ingest with word-level coordinates
- N-level hierarchical header reconstruction (beyond 2-level MultiIndex)
- Multi-page table stitching with repeating-header detection
- A labeled evaluation set of real schedules
- A fine-tuning pipeline that uses TATR's training code on domain data

TATR is consumed as a pinned dependency. Only fork it if the model or training loop itself needs to change.

## Status

Design scaffold. Nothing is implemented yet - modules are stubs with interfaces to react to.

## Layout

src/schedule_extractor/
  ingest.py      PDF -> pages + word boxes (pypdfium2)
  detect.py      thin wrapper over TATR inference
  structure.py   dataclasses for cells, spans, tables
  headers.py     spanning-cell grid -> N-level header tree
  stitch.py      multi-page table stitching
  cli.py         command-line entry point
eval/            ground-truth format + (eventually) labeled schedules
training/        fine-tuning configs and notes
tests/

## Getting started

pip install -e .
schedule-extract path/to/schedule.pdf

## License

TBD. TATR is MIT; pypdfium2 is Apache-2.0 / BSD-3 dual.

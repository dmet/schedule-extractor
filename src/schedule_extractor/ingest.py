from __future__ import annotations

from pathlib import Path

from schedule_extractor.structure import Page


def load_pdf(path: str | Path) -> list[Page]:
    """Open a PDF and return one Page per page, each with rendered image and word boxes.

    Planned: use pypdfium2 for both rasterization and text extraction so word boxes
    align with the image coordinates passed to the detector.
    """
    raise NotImplementedError

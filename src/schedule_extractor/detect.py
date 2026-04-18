from __future__ import annotations

from schedule_extractor.structure import Cell, Page


def detect_tables(page: Page) -> list[tuple[float, float, float, float]]:
    """Run TATR table detection on a page image. Returns table bounding boxes."""
    raise NotImplementedError


def recognize_structure(page: Page, table_bbox: tuple[float, float, float, float]) -> list[Cell]:
    """Run TATR structure recognition on a cropped table. Returns cells with spans."""
    raise NotImplementedError

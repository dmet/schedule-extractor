from __future__ import annotations

from schedule_extractor.structure import Table


def stitch_pages(per_page_tables: list[Table]) -> list[Table]:
    """Merge tables that continue across pages into single logical tables.

    Schedules often repeat the header band on every page. Strategy: detect
    repeating header rows and column-count/column-x-alignment matches across
    consecutive pages, then concatenate body rows.
    """
    raise NotImplementedError

from __future__ import annotations

from schedule_extractor.structure import Cell, HeaderNode


def build_header_tree(cells: list[Cell]) -> list[HeaderNode]:
    """Turn header cells (with row/col spans) into an N-level header tree.

    Construction schedules routinely have 3+ header levels (phase -> activity group
    -> week/day). gmft's MultiIndex output flattens past two levels, so we build
    our own tree. Input: cells with is_header=True. Output: forest of HeaderNodes
    covering the column range.
    """
    raise NotImplementedError

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class WordBox:
    text: str
    x0: float
    y0: float
    x1: float
    y1: float
    page: int


@dataclass(frozen=True)
class Cell:
    row: int
    col: int
    row_span: int
    col_span: int
    text: str
    is_header: bool
    bbox: tuple[float, float, float, float]


@dataclass
class HeaderNode:
    text: str
    level: int
    col_start: int
    col_end: int
    children: list["HeaderNode"] = field(default_factory=list)


@dataclass
class Page:
    index: int
    width: float
    height: float
    words: list[WordBox]


@dataclass
class Table:
    page_range: tuple[int, int]
    bbox_per_page: dict[int, tuple[float, float, float, float]]
    cells: list[Cell]
    header_tree: list[HeaderNode]

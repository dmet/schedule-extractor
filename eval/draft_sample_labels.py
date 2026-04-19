"""Draft ground-truth JSON for SCAHC_ASI.04_Arch_A600.pdf.

Run once: writes eval/data/SCAHC_ASI.04_Arch_A600.json next to the PDF.
This is a first-pass extraction for human review, not a labeled artifact yet.
"""
from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

from schedule_extractor.ingest import load_pdf

PDF = Path("eval/data/SCAHC_ASI.04_Arch_A600.pdf")
OUT = PDF.with_suffix(".draft.json")

# Left table column boundaries (midpoints between adjacent header-label bboxes),
# with 17|18 (Jamb|Remarks) pulled leftward because the Remarks cell body
# begins well to the left of the centered "Remarks" header label.
LEFT_BOUNDS = [
    154.2, 235.85, 278.65, 323.65, 386.05, 440.85, 483.8, 523.25, 566.75,
    605.8, 645.15, 681.95, 733.0, 786.75, 832.95, 907.5, 979.15, 1050.0,
]
NCOL = len(LEFT_BOUNDS) + 1  # 19
RIGHT_OFFSET = 1109.0  # observed x-shift from left table to right table

HEADER_TREE = [
    {"text": "Num.", "col_start": 0, "col_end": 0},
    {"text": "To Room: Name", "col_start": 1, "col_end": 1},
    {"text": "Fire Rating", "col_start": 2, "col_end": 2},
    {"text": "Door", "col_start": 3, "col_end": 9, "children": [
        {"text": "Type", "col_start": 3, "col_end": 3},
        {"text": "Material", "col_start": 4, "col_end": 4},
        {"text": "Finish", "col_start": 5, "col_end": 5},
        {"text": "Leafs", "col_start": 6, "col_end": 6},
        {"text": "Width", "col_start": 7, "col_end": 7},
        {"text": "Height", "col_start": 8, "col_end": 8},
        {"text": "Thick", "col_start": 9, "col_end": 9},
    ]},
    {"text": "Glass", "col_start": 10, "col_end": 10, "children": [
        {"text": "Type", "col_start": 10, "col_end": 10},
    ]},
    {"text": "Frame", "col_start": 11, "col_end": 13, "children": [
        {"text": "Type", "col_start": 11, "col_end": 11},
        {"text": "Material", "col_start": 12, "col_end": 12},
        {"text": "Finish", "col_start": 13, "col_end": 13},
    ]},
    {"text": "Hardware", "col_start": 14, "col_end": 14, "children": [
        {"text": "Set", "col_start": 14, "col_end": 14},
    ]},
    {"text": "STC Rating", "col_start": 15, "col_end": 15},
    {"text": "Head Detail", "col_start": 16, "col_end": 16},
    {"text": "Jamb Detail", "col_start": 17, "col_end": 17},
    {"text": "Remarks", "col_start": 18, "col_end": 18},
]

HDR_YMAX = 2035.0


def col_of_x(x: float, bounds: list[float]) -> int:
    for i, b in enumerate(bounds):
        if x < b:
            return i
    return len(bounds)


def cell_text(words):
    if not words:
        return None
    ws = sorted(words, key=lambda w: (-((w.y0 + w.y1) / 2), w.x0))
    lines, cur, cur_y = [], [], None
    for w in ws:
        yc = (w.y0 + w.y1) / 2
        if cur_y is None or abs(yc - cur_y) <= 3:
            cur.append(w)
            cur_y = yc if cur_y is None else (cur_y + yc) / 2
        else:
            lines.append(sorted(cur, key=lambda w: w.x0))
            cur, cur_y = [w], yc
    if cur:
        lines.append(sorted(cur, key=lambda w: w.x0))
    return " ".join(" ".join(w.text for w in line) for line in lines)


def extract_rows(words, xmin, xmax, num_xmin, num_xmax, bounds):
    anchors = sorted(
        [w for w in words
         if num_xmin <= w.x0 <= num_xmax and w.y1 < HDR_YMAX
         and re.match(r"^\d+[A-Z]?$", w.text)],
        key=lambda w: -w.y0,
    )
    body = [w for w in words if xmin <= w.x0 <= xmax and w.y1 < HDR_YMAX]
    rows = []
    for i, anc in enumerate(anchors):
        top = anc.y1 + 2
        if i + 1 < len(anchors):
            bottom = anchors[i + 1].y1 + 0.5
        else:
            bottom = anc.y0 - 25
        in_band = [w for w in body if bottom <= (w.y0 + w.y1) / 2 <= top]
        cells = defaultdict(list)
        for w in in_band:
            cells[col_of_x((w.x0 + w.x1) / 2, bounds)].append(w)
        rows.append([cell_text(cells[c]) for c in range(len(bounds) + 1)])
    return rows


def main() -> None:
    pages = load_pdf(PDF)
    assert len(pages) == 1, f"expected 1 page, got {len(pages)}"
    page_words = pages[0].words

    left_rows = extract_rows(
        page_words, xmin=115, xmax=1180, num_xmin=120, num_xmax=155, bounds=LEFT_BOUNDS
    )
    right_bounds = [b + RIGHT_OFFSET for b in LEFT_BOUNDS]
    right_rows = extract_rows(
        page_words,
        xmin=115 + RIGHT_OFFSET,
        xmax=1180 + RIGHT_OFFSET,
        num_xmin=120 + RIGHT_OFFSET,
        num_xmax=155 + RIGHT_OFFSET,
        bounds=right_bounds,
    )

    doc = {
        "source_pdf": PDF.name,
        "notes": (
            "First-pass auto-draft from word-box column snapping. Two side-by-side "
            "Door Schedule tables on one page; both share the same header tree."
        ),
        "tables": [
            {"page_range": [1, 1], "header_tree": HEADER_TREE, "rows": left_rows},
            {"page_range": [1, 1], "header_tree": HEADER_TREE, "rows": right_rows},
        ],
    }
    OUT.write_text(json.dumps(doc, indent=2))
    print(f"wrote {OUT}  left_rows={len(left_rows)}  right_rows={len(right_rows)}")


if __name__ == "__main__":
    main()

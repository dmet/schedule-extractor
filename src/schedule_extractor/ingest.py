from __future__ import annotations

from pathlib import Path

import pypdfium2 as pdfium

from schedule_extractor.structure import Page, WordBox


def load_pdf(path: str | Path) -> list[Page]:
    """Open a PDF and return one Page per page, each with word boxes.

    Coordinates are PDF points with the origin at the bottom-left of the page
    (pypdfium2 native). Downstream code that needs image coordinates must flip
    y against Page.height and scale by the render factor.
    """
    pdf = pdfium.PdfDocument(str(path))
    pages: list[Page] = []
    try:
        for i, page in enumerate(pdf):
            textpage = page.get_textpage()
            try:
                words = _extract_words(textpage, i)
            finally:
                textpage.close()
            pages.append(
                Page(
                    index=i,
                    width=page.get_width(),
                    height=page.get_height(),
                    words=words,
                )
            )
            page.close()
    finally:
        pdf.close()
    return pages


def _extract_words(textpage: pdfium.PdfTextPage, page_index: int) -> list[WordBox]:
    n = textpage.count_chars()
    if n == 0:
        return []
    text = textpage.get_text_range(0, n)
    words: list[WordBox] = []
    buf: list[str] = []
    x0 = y0 = float("inf")
    x1 = y1 = float("-inf")

    def flush() -> None:
        nonlocal buf, x0, y0, x1, y1
        if buf:
            words.append(
                WordBox(
                    text="".join(buf),
                    x0=x0, y0=y0, x1=x1, y1=y1,
                    page=page_index,
                )
            )
            buf = []
            x0 = y0 = float("inf")
            x1 = y1 = float("-inf")

    for i, ch in enumerate(text):
        if ch.isspace():
            flush()
            continue
        left, bottom, right, top = textpage.get_charbox(i)
        buf.append(ch)
        if left < x0:
            x0 = left
        if bottom < y0:
            y0 = bottom
        if right > x1:
            x1 = right
        if top > y1:
            y1 = top
    flush()
    return words

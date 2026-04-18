from pathlib import Path

import pytest

from schedule_extractor.ingest import load_pdf

SAMPLE_PDF = (
    Path(__file__).resolve().parents[1]
    / "eval"
    / "data"
    / "SCAHC_ASI.04_Arch_A600.pdf"
)


@pytest.mark.skipif(not SAMPLE_PDF.exists(), reason=f"sample PDF not present: {SAMPLE_PDF}")
def test_load_pdf_returns_words_on_page_0():
    pages = load_pdf(SAMPLE_PDF)
    assert len(pages) > 0

    page0 = pages[0]
    assert page0.index == 0
    assert page0.width > 0 and page0.height > 0
    assert page0.words, "expected non-empty word boxes on page 0"
    assert all(w.page == 0 for w in page0.words)
    assert all(w.text.strip() for w in page0.words)

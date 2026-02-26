import pytest
from utils.pdf_parser import extract_text

def test_extract_text():
    text, chunks = extract_text("data\\sample_papers\\sample.pdf")
    assert text is not None
    assert len(chunks) > 0
    assert isinstance(text, str)
    assert isinstance(chunks, list)
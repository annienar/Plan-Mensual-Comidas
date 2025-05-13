import pytest
from core.extraction.pdf import PDFExtractor
from pathlib import Path

@pytest.mark.parametrize("pdf_path,expected_text", [
    ("tests/fixtures/sample.pdf", ""),  # Replace with actual expected text if available
])
def test_pdf_extractor_extract(pdf_path, expected_text):
    extractor = PDFExtractor()
    result = extractor.extract(pdf_path)
    # If you have a real fixture, check for expected text
    # Otherwise, just check that it returns a string
    assert isinstance(result, str) 
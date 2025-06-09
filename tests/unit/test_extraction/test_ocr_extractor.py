from core.application.recipe.extractors.ocr import OCRExtractor
from pathlib import Path

import pytest
@pytest.mark.parametrize("ocr_path", [
    "tests / fixtures / sample_image.png",  # Replace with actual fixture path if available
    "tests / fixtures / sample_ocr.pdf",   # Replace with actual fixture path if available
])

def test_ocr_extractor_extract(ocr_path):
    extractor = OCRExtractor()
    result = extractor.extract(ocr_path)
    assert isinstance(result, str)

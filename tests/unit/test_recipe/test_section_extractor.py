from core.domain.recipe.extractors.sections import SectionExtractor
from pathlib import Path
import re

import pytest
RECIPE_FILES = [
    "tests/fixtures/recipes/sin_procesar/test_01_basic_recipe.txt",
    "tests/fixtures/recipes/sin_procesar/test_02_fractions_ranges.txt",
    "tests/fixtures/recipes/sin_procesar/test_03_missing_metadata.txt",
    "tests/fixtures/recipes/sin_procesar/test_04_mixed_languages.txt",
    "tests/fixtures/recipes/sin_procesar/test_05_unusual_format.txt",
    "tests/fixtures/recipes/sin_procesar/test_06_standard_url.txt",
    "tests/fixtures/recipes/sin_procesar/test_07_multiple_sources.txt",
    "tests/fixtures/recipes/sin_procesar/test_08_nonstandard_source.txt",
    "tests/fixtures/recipes/sin_procesar/test_09_embedded_source.txt",
    "tests/fixtures/recipes/sin_procesar/test_10_formatting_chars.txt",
    "tests/fixtures/recipes/sin_procesar/test_11_mixed_units.txt",
    "tests/fixtures/recipes/sin_procesar/test_12_complex_format.txt",
    "tests/fixtures/recipes/sin_procesar/test_13_special_chars.txt",
    "tests/fixtures/recipes/sin_procesar/test_14_large_recipe.txt",
]

@pytest.mark.parametrize("txt_path", RECIPE_FILES)
def test_section_extractor_sections(txt_path):
    content = Path(txt_path).read_text(encoding="utf-8")
    sections = SectionExtractor().extract(content)
    assert isinstance(sections, dict)
    assert set(sections.keys()) == {"ingredients", "instructions", "notes"}

    # Check each section
    for key in sections:
        assert isinstance(sections[key], list)
        # Each section should be a list of non - empty strings
        for line in sections[key]:
            assert isinstance(line, str)
            assert line.strip()

    # For basic recipes, at least one section should not be empty
    assert any(sections[key] for key in sections)

    # Check for common patterns
    if sections["instructions"]:
        # Instructions often start with numbers, bullets, or other markers
        assert any(re.match(r"^\d+[\.\)]|\-|\*|>", line) for line in sections["instructions"])

    if sections["ingredients"]:
        # Ingredients often contain quantities
        assert any(re.search(r"\d+", line) for line in sections["ingredients"])

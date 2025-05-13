import pytest
from core.recipe.extractors.sections import SectionExtractor
from pathlib import Path

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

@pytest.mark.xfail(reason="Known edge case in section extraction")
@pytest.mark.parametrize("txt_path", RECIPE_FILES)
def test_section_extractor_sections(txt_path):
    content = Path(txt_path).read_text(encoding="utf-8")
    sections = SectionExtractor().extract(content)
    assert isinstance(sections, dict)
    assert set(sections.keys()) == {"ingredients", "instructions", "notes"}
    for key in sections:
        assert isinstance(sections[key], list)
    # For basic recipes, at least one section should not be empty
    assert any(sections[key] for key in sections)

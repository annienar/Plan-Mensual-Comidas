from core.domain.recipe.extractors.metadata import MetadataExtractor
from pathlib import Path

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
def test_metadata_extractor(txt_path):
    content = Path(txt_path).read_text(encoding="utf-8")
    metadata = MetadataExtractor().extract(content)
    assert isinstance(metadata, dict)
    expected_fields = {
        "title", "url", "porciones", "calorias", "tipo", "tags", 
        "hecho", "date", "dificultad", "tiempo_preparacion", 
        "tiempo_coccion", "tiempo_total", "notas"
    }
    assert set(metadata.keys()) == expected_fields
    assert isinstance(metadata["title"], str)
    assert metadata["title"]
    assert isinstance(metadata["url"], (str, type(None)))
    assert isinstance(metadata["porciones"], (int, type(None)))
    assert isinstance(metadata["calorias"], (int, type(None)))
    assert isinstance(metadata["tipo"], (str, type(None)))
    assert isinstance(metadata["tags"], list)
    assert isinstance(metadata["hecho"], bool)
    assert isinstance(metadata["date"], (str, type(None)))
    assert isinstance(metadata["dificultad"], (str, type(None)))
    assert isinstance(metadata["tiempo_preparacion"], (int, type(None)))
    assert isinstance(metadata["tiempo_coccion"], (int, type(None)))
    assert isinstance(metadata["tiempo_total"], (int, type(None)))
    assert isinstance(metadata["notas"], (str, type(None)))

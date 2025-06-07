from core.domain.recipe.normalizers.text import TextNormalizer

import pytest
@pytest.mark.parametrize("text, expected", [
    ("  Hello world  ", "hello world"), 
    ("\n\tRecipe Title\n", "recipe title"), 
    ("No extra space", "no extra space"), 
    ("   ", ""), 
])

def test_text_normalizer(text, expected):
    result = TextNormalizer().normalize(text)
    assert isinstance(result, str)
    assert result == expected

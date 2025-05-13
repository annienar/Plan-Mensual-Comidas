import pytest
from core.recipe.normalizers.text import TextNormalizer

@pytest.mark.parametrize("text,expected", [
    ("  Hello world  ", "Hello world"),
    ("\n\tRecipe Title\n", "Recipe Title"),
    ("No extra space", "No extra space"),
    ("   ", ""),
])
def test_text_normalizer(text, expected):
    result = TextNormalizer().normalize(text)
    assert isinstance(result, str)
    assert result == expected

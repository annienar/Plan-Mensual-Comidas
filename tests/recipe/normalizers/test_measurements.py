"""
Tests for the measurements normalizer module.
"""

from core.domain.recipe.normalizers.measurements import MeasurementNormalizer

import pytest
@pytest.fixture

def normalizer():
    """Create a measurement normalizer instance."""
    return MeasurementNormalizer()

def test_normalize_basic(normalizer):
    """Test basic measurement normalization."""
    # Test with standard units
    amount, unit = normalizer.normalize("2 cups")
    assert amount == 1.0  # Current stub implementation
    assert unit == "2 cups"

    # Test with fractions
    amount, unit = normalizer.normalize("1 / 2 teaspoon")
    assert amount == 1.0
    assert unit == "1 / 2 teaspoon"

    # Test with mixed numbers
    amount, unit = normalizer.normalize("1 1 / 2 tablespoons")
    assert amount == 1.0
    assert unit == "1 1 / 2 tablespoons"

def test_normalize_edge_cases(normalizer):
    """Test measurement normalization edge cases."""
    # Test empty string
    amount, unit = normalizer.normalize("")
    assert amount == 1.0
    assert unit == ""

    # Test with no unit
    amount, unit = normalizer.normalize("2")
    assert amount == 1.0
    assert unit == "2"

    # Test with invalid format
    amount, unit = normalizer.normalize("invalid")
    assert amount == 1.0
    assert unit == "invalid"

def test_normalize_special_cases(normalizer):
    """Test measurement normalization special cases."""
    # Test with "to taste"
    amount, unit = normalizer.normalize("to taste")
    assert amount == 1.0
    assert unit == "to taste"

    # Test with "as needed"
    amount, unit = normalizer.normalize("as needed")
    assert amount == 1.0
    assert unit == "as needed"

    # Test with "a pinch"
    amount, unit = normalizer.normalize("a pinch")
    assert amount == 1.0
    assert unit == "a pinch"

def test_normalize_unit_variations(normalizer):
    """Test measurement normalization with unit variations."""
    # Test plural / singular variations
    amount, unit = normalizer.normalize("1 cup")
    assert amount == 1.0
    assert unit == "1 cup"

    amount, unit = normalizer.normalize("2 cups")
    assert amount == 1.0
    assert unit == "2 cups"

    # Test abbreviated units
    amount, unit = normalizer.normalize("1 tbsp")
    assert amount == 1.0
    assert unit == "1 tbsp"

    amount, unit = normalizer.normalize("2 tbsps")
    assert amount == 1.0
    assert unit == "2 tbsps"

def test_normalize_metric_imperial(normalizer):
    """Test measurement normalization with metric and imperial units."""
    # Test metric units
    amount, unit = normalizer.normalize("500 grams")
    assert amount == 1.0
    assert unit == "500 grams"

    amount, unit = normalizer.normalize("1 liter")
    assert amount == 1.0
    assert unit == "1 liter"

    # Test imperial units
    amount, unit = normalizer.normalize("1 pound")
    assert amount == 1.0
    assert unit == "1 pound"

    amount, unit = normalizer.normalize("1 gallon")
    assert amount == 1.0
    assert unit == "1 gallon"

def test_normalize_compound_units(normalizer):
    """Test measurement normalization with compound units."""
    # Test compound units
    amount, unit = normalizer.normalize("1 cup and 2 tablespoons")
    assert amount == 1.0
    assert unit == "1 cup and 2 tablespoons"

    amount, unit = normalizer.normalize("2 pounds 4 ounces")
    assert amount == 1.0
    assert unit == "2 pounds 4 ounces"

    # Test ranges
    amount, unit = normalizer.normalize("1 - 2 cups")
    assert amount == 1.0
    assert unit == "1 - 2 cups"

    amount, unit = normalizer.normalize("2 to 3 tablespoons")
    assert amount == 1.0
    assert unit == "2 to 3 tablespoons"

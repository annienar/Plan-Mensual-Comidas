import pytest
from core.recipe.normalizers.measurements import MeasurementNormalizer

@pytest.mark.parametrize("measurement", [
    "100 g",
    "1 taza",
    "2.5 kg",
    "3 cucharadas",
    "0.5 l",
    "1/2 cdta",
])
def test_measurement_normalizer(measurement):
    value, unit = MeasurementNormalizer().normalize(measurement)
    assert isinstance(value, float)
    assert isinstance(unit, str)

from core.domain.recipe.normalizers.measurements import MeasurementNormalizer

import pytest
@pytest.mark.parametrize("measurement", [
    "100 g", 
    "1 cup", 
    "2.5 kg", 
    "3 tablespoons", 
    "0.5 l", 
    "0.5 tsp", 
])

def test_measurement_normalizer(measurement):
    value, unit = MeasurementNormalizer().normalize(measurement)
    assert isinstance(value, float)
    assert isinstance(unit, str)

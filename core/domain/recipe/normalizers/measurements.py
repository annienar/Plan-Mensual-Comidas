"""
Measurement normalizer for converting between different units.
"""
from typing import Tuple, Dict, Optional, Any
import re

from .base import BaseNormalizer
from fractions import Fraction
UNIT_CONVERSIONS = {'weight': {'g': 1.0, 'gram': 1.0, 'grams': 1.0, 'kg':
    1000.0, 'kilogram': 1000.0, 'kilograms': 1000.0, 'oz': 28.35, 'ounce':
    28.35, 'ounces': 28.35, 'lb': 453.59, 'pound': 453.59, 'pounds': 453.59
    }, 'volume': {'ml': 1.0, 'milliliter': 1.0, 'milliliters': 1.0, 'l':
    1000.0, 'liter': 1000.0, 'liters': 1000.0, 'tsp': 4.93, 'teaspoon':
    4.93, 'teaspoons': 4.93, 'tbsp': 14.79, 'tablespoon': 14.79, 
    'tablespoons': 14.79, 'cup': 236.59, 'cups': 236.59, 'qt': 946.35, 
    'quart': 946.35, 'quarts': 946.35, 'gal': 3785.41, 'gallon': 3785.41, 
    'gallons': 3785.41}, 'count': {'piece': 1.0, 'pieces': 1.0, 'whole':
    1.0, 'slice': 1.0, 'slices': 1.0}, 'other': {'pinch': 1.0, 'to taste':
    1.0, 'as needed': 1.0}}
UNIT_ABBREVIATIONS = {'g': 'gram', 'kg': 'kilogram', 'oz': 'ounce', 'lb':
    'pound', 'ml': 'milliliter', 'l': 'liter', 'tsp': 'teaspoon', 'tbsp':
    'tablespoon', 'qt': 'quart', 'gal': 'gallon'}

class MeasurementNormalizer(BaseNormalizer):
    """Normalize measurements to standard units."""

    def __init__(self: Any) -> None:
        """Initialize the normalizer with unit conversions."""
        self.unit_conversions = UNIT_CONVERSIONS
        self.unit_abbreviations = UNIT_ABBREVIATIONS

    def _parse_quantity(self: Any, quantity_str: str) -> float:
        """
        Parse a quantity string into a float.

        Args:
            quantity_str: String containing a quantity (e.g., "1 1 / 2", "0.5", "2", "1½", "3-4")

        Returns:
            Parsed quantity as a float

        Raises:
            ValueError: If the quantity string is invalid
        """
        quantity_str = quantity_str.strip()
        
        # Handle ranges (e.g., "3-4", "2-3") - use average
        range_match = re.match(r'^(\d+(?:\.\d+)?)-(\d+(?:\.\d+)?)$', quantity_str)
        if range_match:
            start = float(range_match.group(1))
            end = float(range_match.group(2))
            return (start + end) / 2.0
        
        # Handle unicode fractions (½, ¼, ¾, ⅓, ⅔, ⅛, ⅜, ⅝, ⅞)
        unicode_fractions = {
            '½': 0.5, '¼': 0.25, '¾': 0.75, '⅓': 0.333, '⅔': 0.667,
            '⅛': 0.125, '⅜': 0.375, '⅝': 0.625, '⅞': 0.875, '⅙': 0.167,
            '⅚': 0.833, '⅕': 0.2, '⅖': 0.4, '⅗': 0.6, '⅘': 0.8
        }
        
        # Check for mixed unicode fractions (e.g., "1½", "2¼")
        unicode_mixed_match = re.match(r'^(\d+)([½¼¾⅓⅔⅛⅜⅝⅞⅙⅚⅕⅖⅗⅘])$', quantity_str)
        if unicode_mixed_match:
            whole = int(unicode_mixed_match.group(1))
            fraction_char = unicode_mixed_match.group(2)
            return whole + unicode_fractions[fraction_char]
        
        # Check for standalone unicode fractions
        if quantity_str in unicode_fractions:
            return unicode_fractions[quantity_str]
        
        # Handle regular mixed fractions (e.g., "1 1/2")
        mixed_match = re.match(r'^(\d+)\s+(\d+)/(\d+)$', quantity_str)
        if mixed_match:
            whole = int(mixed_match.group(1))
            numerator = int(mixed_match.group(2))
            denominator = int(mixed_match.group(3))
            return whole + numerator / denominator
        
        # Handle regular fractions (e.g., "1/2")
        fraction_match = re.match(r'^(\d+)/(\d+)$', quantity_str)
        if fraction_match:
            numerator = int(fraction_match.group(1))
            denominator = int(fraction_match.group(2))
            return numerator / denominator
        
        # Handle decimal numbers and integers
        try:
            return float(quantity_str)
        except ValueError:
            raise ValueError(f'Invalid quantity format: {quantity_str}')

    def _normalize_unit(self: Any, unit: str) -> Tuple[str, str]:
        """
        Normalize a unit to its standard form and determine its category.

        Args:
            unit: Unit to normalize (e.g., "tbsp", "tablespoon")

        Returns:
            Tuple of (normalized_unit, category)

        Raises:
            ValueError: If the unit is not recognized
        """
        unit = unit.lower().rstrip('s')
        if unit in self.unit_abbreviations:
            unit = self.unit_abbreviations[unit]
        for category, units in self.unit_conversions.items():
            if unit in units:
                return unit, category
        raise ValueError(f'Unrecognized unit: {unit}')

    def normalize(self: Any, measurement: str) ->Tuple[float, str]:
        """
        Convert a measurement to standard units.

        Args:
            measurement: String containing a measurement (e.g., "1 1/2 cups", "2 tbsp")

        Returns:
            Tuple of (quantity, normalized_unit)

        Raises:
            ValueError: If the measurement string is invalid
        """
        measurement = measurement.strip()
        if not measurement:
            raise ValueError('Empty measurement string')
        
        # Handle mixed fractions with units (e.g., "2 1/3 cups")
        mixed_with_unit_match = re.match(r'^(\d+)\s+(\d+)/(\d+)\s+(.+)$', measurement)
        if mixed_with_unit_match:
            whole = int(mixed_with_unit_match.group(1))
            numerator = int(mixed_with_unit_match.group(2))
            denominator = int(mixed_with_unit_match.group(3))
            unit = mixed_with_unit_match.group(4)
            quantity = whole + numerator / denominator
        else:
            # Split by spaces to separate quantity and unit
            parts = measurement.split()
            try:
                quantity = self._parse_quantity(parts[0])
            except ValueError as e:
                raise ValueError(f'Invalid quantity in measurement: {str(e)}')
            
            if len(parts) > 1:
                unit = ' '.join(parts[1:])
            else:
                unit = ''
        
        if not unit:
            return quantity, ''
        
        try:
            normalized_unit, category = self._normalize_unit(unit)
        except ValueError as e:
            raise ValueError(f'Invalid unit in measurement: {str(e)}')
        
        if category in ['weight', 'volume']:
            conversion = self.unit_conversions[category][normalized_unit]
            quantity *= conversion
            normalized_unit = 'g' if category == 'weight' else 'ml'
        
        return quantity, normalized_unit

    def denormalize(self: Any, quantity: float, unit: str) ->str:
        """
        Convert a normalized measurement back to a human - readable format.

        Args:
            quantity: Quantity in base units
            unit: Unit to convert to

        Returns:
            Human - readable measurement string

        Raises:
            ValueError: If the unit is not recognized
        """
        if not unit:
            return str(quantity)
        try:
            normalized_unit, category = self._normalize_unit(unit)
        except ValueError as e:
            raise ValueError(f'Invalid unit for denormalization: {str(e)}')
        if category in ['weight', 'volume']:
            conversion = self.unit_conversions[category][normalized_unit]
            quantity /= conversion
        if quantity.is_integer():
            quantity_str = str(int(quantity))
        else:
            try:
                f = Fraction(quantity).limit_denominator(8)
                if f.denominator == 1:
                    quantity_str = str(f.numerator)
                elif f.numerator < f.denominator:
                    quantity_str = f'{f.numerator}/{f.denominator}'
                else:
                    whole = f.numerator // f.denominator
                    remainder = f.numerator % f.denominator
                    if remainder == 0:
                        quantity_str = str(whole)
                    else:
                        quantity_str = f'{whole} {remainder}/{f.denominator}'
            except (ValueError, ZeroDivisionError):
                quantity_str = str(quantity)
        return f'{quantity_str} {normalized_unit}'

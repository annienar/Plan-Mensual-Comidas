"""
Ingredient service.

This module contains the ingredient domain service.
"""

from ...exceptions.recipe import RecipeValidationError
from ..models.ingredient import Ingredient
from typing import List, Optional

from decimal import Decimal

class IngredientService:
    """Ingredient service.

    This service handles ingredient - related business logic.
    """

    @staticmethod
    def normalize_quantity(quantity: float, unit: Optional[str] = None) -> tuple[float, Optional[str]]:
        """Normalize ingredient quantity and unit.

        Args:
            quantity: Ingredient quantity
            unit: Ingredient unit

        Returns:
            tuple[float, Optional[str]]: Normalized quantity and unit

        Raises:
            RecipeValidationError: If quantity or unit is invalid
        """
        # Convert to Decimal for precise calculations
        quantity = Decimal(str(quantity))

        # Handle common unit conversions
        if unit:
            unit = unit.lower()

            # Volume conversions
            if unit in ["ml", "milliliter", "milliliters"]:
                if quantity >= 1000:
                    quantity = quantity / 1000
                    unit = "l"
                else:
                    unit = "ml"
            elif unit in ["l", "liter", "liters"]:
                if quantity < 1:
                    quantity = quantity * 1000
                    unit = "ml"
                else:
                    unit = "l"

            # Weight conversions
            elif unit in ["g", "gram", "grams"]:
                if quantity >= 1000:
                    quantity = quantity / 1000
                    unit = "kg"
                else:
                    unit = "g"
            elif unit in ["kg", "kilogram", "kilograms"]:
                if quantity < 1:
                    quantity = quantity * 1000
                    unit = "g"
                else:
                    unit = "kg"

            # Count conversions
            elif unit in ["pcs", "piece", "pieces"]:
                unit = "pcs"

        # Convert back to float
        quantity = float(quantity)

        return quantity, unit

    @staticmethod
    def scale_ingredients(ingredients: List[Ingredient], factor: float) -> List[Ingredient]:
        """Scale ingredient quantities.

        Args:
            ingredients: Ingredients to scale
            factor: Scaling factor

        Returns:
            List[Ingredient]: Scaled ingredients

        Raises:
            RecipeValidationError: If factor is invalid
        """
        if factor <= 0:
            raise RecipeValidationError("Scaling factor must be positive")

        scaled_ingredients = []
        for ingredient in ingredients:
            # Scale quantity
            scaled_quantity = ingredient.quantity * factor

            # Normalize quantity and unit
            normalized_quantity, normalized_unit = IngredientService.normalize_quantity(
                scaled_quantity, 
                ingredient.unit
)

            # Create scaled ingredient
            scaled_ingredient = Ingredient(
                name = ingredient.name, 
                quantity = normalized_quantity, 
                unit = normalized_unit
)

            scaled_ingredients.append(scaled_ingredient)

        return scaled_ingredients

    @staticmethod
    def merge_ingredients(ingredients: List[Ingredient]) -> List[Ingredient]:
        """Merge duplicate ingredients.

        Args:
            ingredients: Ingredients to merge

        Returns:
            List[Ingredient]: Merged ingredients
        """
        # Group ingredients by name and unit
        groups = {}
        for ingredient in ingredients:
            key = (ingredient.name.lower(), ingredient.unit)
            if key in groups:
                groups[key].append(ingredient)
            else:
                groups[key] = [ingredient]

        # Merge ingredients in each group
        merged_ingredients = []
        for (name, unit), group in groups.items():
            # Sum quantities
            total_quantity = sum(ingredient.quantity for ingredient in group)

            # Normalize quantity and unit
            normalized_quantity, normalized_unit = IngredientService.normalize_quantity(
                total_quantity, 
                unit
)

            # Create merged ingredient
            merged_ingredient = Ingredient(
                name = name, 
                quantity = normalized_quantity, 
                unit = normalized_unit
)

            merged_ingredients.append(merged_ingredient)

        return merged_ingredients

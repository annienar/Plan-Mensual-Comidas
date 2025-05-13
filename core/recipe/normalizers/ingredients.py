from typing import List, Dict, Any
from core.recipe.models.ingredient import Ingredient
from .base import BaseNormalizer

class IngredientNormalizer(BaseNormalizer):
    def normalize(self, ingredients: List[Dict[str, Any]]) -> List[Ingredient]:
        """Normalize ingredient data to standard format."""
        return [Ingredient(
            name=ing.get('nombre', ''),
            quantity=ing.get('cantidad', 0.0),
            unit=ing.get('unidad', ''),
        ) for ing in ingredients] 
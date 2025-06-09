from core.domain.recipe.models.ingredient import Ingredient
from typing import List, Dict, Any

from .base import BaseNormalizer

class IngredientNormalizer(BaseNormalizer):
    """Class IngredientNormalizer."""

    def normalize(self, ingredients: List[Dict[str, Any]]) -> List[Ingredient]:
        """Normalize ingredient data to standard format."""
        normalized = []
        for ing in ingredients:
            unit = ing.get('unidad', ing.get('unit'))
            if not unit or unit.strip() == '':
                unit = 'pieza'  # Default unit for ingredients without specific units
            
            # Handle overly long ingredient names (likely extraction errors)
            name = ing.get('nombre', ing.get('name', ''))
            if len(name) > 100:
                # Skip ingredients that are clearly not ingredients (likely notes or instructions)
                continue
                
            normalized.append(Ingredient(
                nombre = name, 
                cantidad = ing.get('cantidad', ing.get('quantity', 1.0)), 
                unidad = unit
))
        return normalized

    def normalize_single(self, ingredient: Dict[str, Any]) -> Ingredient:
        """Normalize a single ingredient entry to standard format."""
        unit = ingredient.get('unidad', ingredient.get('unit'))
        if not unit or unit.strip() == '':
            unit = 'pieza'  # Default unit for ingredients without specific units
        return Ingredient(
            nombre = ingredient.get('nombre', ingredient.get('name', '')), 
            cantidad = ingredient.get('cantidad', ingredient.get('quantity', 1.0)), 
            unidad = unit
)

    def denormalize(self, ingredient: Ingredient) -> Dict[str, Any]:
        """Convert a normalized ingredient back to dict format."""
        return {
            'nombre': ingredient.nombre,
            'cantidad': ingredient.cantidad,
            'unidad': ingredient.unidad
        }

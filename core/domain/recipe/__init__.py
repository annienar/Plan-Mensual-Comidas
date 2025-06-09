"""
Recipe domain package.

This package contains the core recipe domain logic, including:
- Recipe models
- Recipe extractors
- Recipe normalizers
- Recipe generators
- Recipe validation
"""

from .models import Recipe, Ingredient
# RecipeProcessor is in application layer, not domain
from .validators import validate_recipe

__all__ = [
    'Recipe', 
    'Ingredient', 
    'validate_recipe', 
]

"""
Domain layer package.

This package contains the core business logic of the application:
- Recipe domain: Recipe management and processing
- Meal Plan domain: Meal planning and scheduling
"""

from .recipe import Recipe, Ingredient
from .meal_plan import MealPlan

__all__ = [
    'Recipe', 
    'Ingredient', 
    'MealPlan', 
]

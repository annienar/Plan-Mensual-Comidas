"""
Domain events module.

This module contains the domain events system.
"""

from .base import DomainEvent
from .recipe import (
    RecipeCreated, 
    RecipeUpdated, 
    RecipeDeleted, 
    RecipeScaled
)
from .meal_plan import (
    MealPlanCreated, 
    MealPlanUpdated, 
    MealPlanDeleted, 
    MealAdded, 
    MealRemoved
)

__all__ = [
    "DomainEvent", 
    "RecipeCreated", 
    "RecipeUpdated", 
    "RecipeDeleted", 
    "RecipeScaled", 
    "MealPlanCreated", 
    "MealPlanUpdated", 
    "MealPlanDeleted", 
    "MealAdded", 
    "MealRemoved", 
]

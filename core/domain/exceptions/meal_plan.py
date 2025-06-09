"""
Meal plan exceptions.

This module contains meal plan - related exceptions.
"""

from .base import DomainError

class MealPlanError(DomainError):
    """Base meal plan error."""
    pass

class MealPlanValidationError(MealPlanError):
    """Validation error."""
    pass

class MealPlanGenerationError(MealPlanError):
    """Generation error."""
    pass

class MealPlanNotFoundError(MealPlanError):
    """Not found error."""
    pass

class MealPlanDuplicateError(MealPlanError):
    """Duplicate error."""
    pass

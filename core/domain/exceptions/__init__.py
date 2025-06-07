"""
Domain exceptions.

This module contains all domain - related exceptions.
"""

from .base import DomainError
from .recipe import (
    RecipeError, 
    RecipeValidationError, 
    RecipeGenerationError, 
    RecipeExtractionError, 
    RecipeNotFoundError, 
    RecipeDuplicateError
)
from .meal_plan import (
    MealPlanError, 
    MealPlanValidationError, 
    MealPlanGenerationError, 
    MealPlanNotFoundError, 
    MealPlanDuplicateError
)
from .llm import (
    LLMError, 
    LLMValidationError, 
    LLMGenerationError, 
    LLMTimeoutError, 
    LLMRateLimitError
)
from .notion import (
    NotionError, 
    NotionRateLimitError, 
    NotionTimeoutError, 
    NotionValidationError
)

__all__ = [
    "DomainError", 
    "RecipeError", 
    "RecipeValidationError", 
    "RecipeGenerationError", 
    "RecipeExtractionError", 
    "RecipeNotFoundError", 
    "RecipeDuplicateError", 
    "MealPlanError", 
    "MealPlanValidationError", 
    "MealPlanGenerationError", 
    "MealPlanNotFoundError", 
    "MealPlanDuplicateError", 
    "LLMError", 
    "LLMValidationError", 
    "LLMGenerationError", 
    "LLMTimeoutError", 
    "LLMRateLimitError", 
    "NotionError", 
    "NotionRateLimitError", 
    "NotionTimeoutError", 
    "NotionValidationError"
]

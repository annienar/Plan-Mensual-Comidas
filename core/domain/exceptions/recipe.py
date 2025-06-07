"""
Recipe exceptions.

This module contains recipe - related exceptions.
"""

from .base import DomainError

class RecipeError(DomainError):
    """Base recipe error."""
    pass

class RecipeValidationError(RecipeError):
    """Validation error."""
    pass

class RecipeGenerationError(RecipeError):
    """Generation error."""
    pass

class RecipeExtractionError(RecipeError):
    """Extraction error."""
    pass

class RecipeNotFoundError(RecipeError):
    """Not found error."""
    pass

class RecipeDuplicateError(RecipeError):
    """Duplicate error."""
    pass

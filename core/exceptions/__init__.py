"""Core exceptions module."""

from .infrastructure import (
    InfrastructureError, 
    LLMError, 
    ModelNotFoundError, 
    InvalidResponseError, 
    CircuitBreakerOpenError, 
    LLMValidationError, 
    LLMRateLimitError, 
    LLMTimeoutError, 
)

from .config import (
    ConfigError, 
    ConfigNotFoundError, 
    ConfigValidationError, 
)

class BaseError(Exception):
    """Base exception for all application errors."""
    pass

class NotionError(BaseError):
    """Base exception for Notion - related errors."""
    pass

class RecipeError(BaseError):
    """Base exception for recipe - related errors."""
    pass

class MealPlanError(BaseError):
    """Base exception for meal plan - related errors."""
    pass

__all__ = [
    "BaseError", 
    "InfrastructureError", 
    "LLMError", 
    "ModelNotFoundError", 
    "InvalidResponseError", 
    "CircuitBreakerOpenError", 
    "LLMValidationError", 
    "LLMRateLimitError", 
    "LLMTimeoutError", 
    "ConfigError", 
    "ConfigNotFoundError", 
    "ConfigValidationError", 
    "NotionError", 
    "RecipeError", 
    "MealPlanError", 
]

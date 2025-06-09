"""
Core module.

This module contains the core functionality of the application.
"""

from .config import Settings, ConfigLoader
from .exceptions import (
    BaseError, 
    ConfigError, 
    LLMError, 
    NotionError, 
    RecipeError, 
    MealPlanError
)

__version__ = "0.1.0"

__all__ = [
    "Settings", 
    "ConfigLoader", 
    "BaseError", 
    "ConfigError", 
    "LLMError", 
    "NotionError", 
    "RecipeError", 
    "MealPlanError", 
]

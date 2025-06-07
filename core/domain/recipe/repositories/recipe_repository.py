"""
Recipe repository interface.

This module contains the abstract recipe repository interface.
"""

from ..models.recipe import Recipe
from typing import List, Optional

from abc import ABC, abstractmethod

class RecipeRepository(ABC):
    """Abstract recipe repository interface."""

    @abstractmethod
    async def save(self, recipe: Recipe) -> None:
        """Save a recipe."""
        pass

    @abstractmethod
    async def delete(self, recipe: Recipe) -> None:
        """Delete a recipe."""
        pass

    @abstractmethod
    async def find_by_title(self, title: str) -> Optional[Recipe]:
        """Find a recipe by title."""
        pass

    @abstractmethod
    async def find_all(self) -> List[Recipe]:
        """Find all recipes."""
        pass

    @abstractmethod
    async def search(self, query: str) -> List[Recipe]:
        """Search recipes."""
        pass

"""
Meal plan repository interface.

This module contains the abstract meal plan repository interface.
"""

from typing import List, Optional

from ..models.meal_plan import MealPlan
from abc import ABC, abstractmethod

class MealPlanRepository(ABC):
    """Abstract meal plan repository interface."""

    @abstractmethod
    async def save(self, meal_plan: MealPlan) -> None:
        """Save a meal plan."""
        pass

    @abstractmethod
    async def delete(self, meal_plan: MealPlan) -> None:
        """Delete a meal plan."""
        pass

    @abstractmethod
    async def find_by_title(self, title: str) -> Optional[MealPlan]:
        """Find a meal plan by title."""
        pass

    @abstractmethod
    async def find_all(self) -> List[MealPlan]:
        """Find all meal plans."""
        pass

    @abstractmethod
    async def search(self, query: str) -> List[MealPlan]:
        """Search meal plans."""
        pass

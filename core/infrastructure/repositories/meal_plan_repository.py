"""
Meal plan repository.

This module contains the meal plan repository implementation.
"""

from datetime import datetime
from typing import List, Optional

from ...domain.events.dispatcher import EventDispatcher
from ...domain.events.meal_plan import (
    MealPlanCreated, 
    MealPlanUpdated, 
    MealPlanDeleted
)
from ...domain.meal_plan.models.meal_plan import MealPlan
from ...domain.meal_plan.repositories.meal_plan_repository import MealPlanRepository

class InMemoryMealPlanRepository(MealPlanRepository):
    """In - memory meal plan repository.

    This repository stores meal plans in memory.
    """

    def __init__(self, event_dispatcher: EventDispatcher):
        """Initialize the repository.

        Args:
            event_dispatcher: Event dispatcher
        """
        self.meal_plans: List[MealPlan] = []
        self.event_dispatcher = event_dispatcher

    async def save(self, meal_plan: MealPlan) -> None:
        """Save a meal plan.

        Args:
            meal_plan: Meal plan to save
        """
        # Check if meal plan exists
        existing_meal_plan = await self.find_by_title(meal_plan.title)

        if existing_meal_plan:
            # Update existing meal plan
            index = self.meal_plans.index(existing_meal_plan)
            self.meal_plans[index] = meal_plan

            # Create event
            event = MealPlanUpdated(meal_plan, {})

            # Dispatch event
            await self.event_dispatcher.dispatch(event)
        else:
            # Add new meal plan
            self.meal_plans.append(meal_plan)

            # Create event
            event = MealPlanCreated(meal_plan)

            # Dispatch event
            await self.event_dispatcher.dispatch(event)

    async def delete(self, meal_plan: MealPlan) -> None:
        """Delete a meal plan.

        Args:
            meal_plan: Meal plan to delete
        """
        # Remove meal plan
        self.meal_plans = [mp for mp in self.meal_plans if mp.title != meal_plan.title]

        # Create event
        event = MealPlanDeleted(meal_plan.title)

        # Dispatch event
        await self.event_dispatcher.dispatch(event)

    async def find_by_title(self, title: str) -> Optional[MealPlan]:
        """Find a meal plan by title.

        Args:
            title: Meal plan title

        Returns:
            Optional[MealPlan]: Meal plan if found, None otherwise
        """
        for meal_plan in self.meal_plans:
            if meal_plan.title == title:
                return meal_plan

        return None

    async def find_all(self) -> List[MealPlan]:
        """Find all meal plans.

        Returns:
            List[MealPlan]: All meal plans
        """
        return self.meal_plans.copy()

    async def search(self, query: str) -> List[MealPlan]:
        """Search meal plans.

        Args:
            query: Search query

        Returns:
            List[MealPlan]: Matching meal plans
        """
        query = query.lower()

        return [
            meal_plan for meal_plan in self.meal_plans
            if query in meal_plan.title.lower() or
            any(query in meal.type.lower() for meal in meal_plan.meals) or
            any(query in recipe.title.lower() for meal in meal_plan.meals for recipe in meal.recipes)
        ]

    async def find_by_date_range(
        self, 
        start_date: str, 
        end_date: str
) -> List[MealPlan]:
        """Find meal plans within a date range.

        Args:
            start_date: Start date in YYYY - MM - DD format
            end_date: End date in YYYY - MM - DD format

        Returns:
            List[MealPlan]: Meal plans within the date range
        """
        return [
            meal_plan for meal_plan in self.meal_plans
            if start_date <= meal_plan.metadata.start_date <= end_date or
            start_date <= meal_plan.metadata.end_date <= end_date
        ]

    async def find_by_recipe(self, recipe_title: str) -> List[MealPlan]:
        """Find meal plans containing a specific recipe.

        Args:
            recipe_title: Recipe title

        Returns:
            List[MealPlan]: Meal plans containing the recipe
        """
        return [
            meal_plan for meal_plan in self.meal_plans
            if any(
                recipe_title == recipe.title
                for meal in meal_plan.meals
                for recipe in meal.recipes
)
        ]

"""
Meal plan service.

This module contains the meal plan domain service.
"""

from datetime import datetime, timedelta
from typing import List, Optional

from ...events.dispatcher import EventDispatcher
from ...events.meal_plan import (
    MealPlanCreated, 
    MealPlanUpdated, 
    MealPlanDeleted, 
    MealAdded, 
    MealRemoved
)
from ...exceptions.meal_plan import MealPlanValidationError
from ..models.meal import Meal
from ..models.meal_plan import MealPlan
from ..models.metadata import MealPlanMetadata
from .meal_service import MealService
from .metadata_service import MetadataService

class MealPlanService:
    """Meal plan service.

    This service handles meal plan - related business logic.
    """

    def __init__(self, event_dispatcher: EventDispatcher):
        """Initialize the service.

        Args:
            event_dispatcher: Event dispatcher
        """
        self.meal_service = MealService()
        self.metadata_service = MetadataService()
        self.event_dispatcher = event_dispatcher

    async def create_meal_plan(self, meal_plan: MealPlan) -> MealPlan:
        """Create a meal plan.

        Args:
            meal_plan: Meal plan to create

        Returns:
            MealPlan: Created meal plan

        Raises:
            MealPlanValidationError: If meal plan is invalid
        """
        # Validate meal plan
        self.validate_meal_plan(meal_plan)

        # Create event
        event = MealPlanCreated(meal_plan)

        # Dispatch event
        await self.event_dispatcher.dispatch(event)

        return meal_plan

    async def update_meal_plan(
        self, 
        meal_plan: MealPlan, 
        changes: dict
) -> MealPlan:
        """Update a meal plan.

        Args:
            meal_plan: Meal plan to update
            changes: Changes to apply

        Returns:
            MealPlan: Updated meal plan

        Raises:
            MealPlanValidationError: If meal plan is invalid
        """
        # Validate meal plan
        self.validate_meal_plan(meal_plan)

        # Create event
        event = MealPlanUpdated(meal_plan, changes)

        # Dispatch event
        await self.event_dispatcher.dispatch(event)

        return meal_plan

    async def delete_meal_plan(self, meal_plan: MealPlan) -> None:
        """Delete a meal plan.

        Args:
            meal_plan: Meal plan to delete
        """
        # Create event
        event = MealPlanDeleted(meal_plan.title)

        # Dispatch event
        await self.event_dispatcher.dispatch(event)

    async def add_meal(self, meal_plan: MealPlan, meal: Meal) -> MealPlan:
        """Add a meal to a meal plan.

        Args:
            meal_plan: Meal plan to add meal to
            meal: Meal to add

        Returns:
            MealPlan: Updated meal plan

        Raises:
            MealPlanValidationError: If meal is invalid
        """
        # Validate meal
        self.meal_service.validate_meal(meal)

        # Validate meal date is within plan dates
        if not (meal_plan.metadata.start_date <= meal.date <= meal_plan.metadata.end_date):
            raise MealPlanValidationError(
                f"Meal date {meal.date} is outside plan dates "
                f"{meal_plan.metadata.start_date} - {meal_plan.metadata.end_date}"
)

        # Add meal
        meal_plan.meals.append(meal)

        # Create event
        event = MealAdded(meal_plan, meal)

        # Dispatch event
        await self.event_dispatcher.dispatch(event)

        return meal_plan

    async def remove_meal(self, meal_plan: MealPlan, meal: Meal) -> MealPlan:
        """Remove a meal from a meal plan.

        Args:
            meal_plan: Meal plan to remove meal from
            meal: Meal to remove

        Returns:
            MealPlan: Updated meal plan
        """
        # Remove meal
        meal_plan.meals = [m for m in meal_plan.meals if m != meal]

        # Create event
        event = MealRemoved(meal_plan, meal)

        # Dispatch event
        await self.event_dispatcher.dispatch(event)

        return meal_plan

    def get_meals_by_date(self, meal_plan: MealPlan, date: str) -> List[Meal]:
        """Get meals for a specific date.

        Args:
            meal_plan: Meal plan
            date: Date in YYYY - MM - DD format

        Returns:
            List[Meal]: Meals for the date
        """
        return self.meal_service.get_meals_by_date(meal_plan.meals, date)

    def get_meals_by_type(self, meal_plan: MealPlan, type: str) -> List[Meal]:
        """Get meals of a specific type.

        Args:
            meal_plan: Meal plan
            type: Meal type

        Returns:
            List[Meal]: Meals of the type
        """
        return self.meal_service.get_meals_by_type(meal_plan.meals, type)

    def get_meals_by_time_range(
        self, 
        meal_plan: MealPlan, 
        start_time: str, 
        end_time: str
) -> List[Meal]:
        """Get meals within a time range.

        Args:
            meal_plan: Meal plan
            start_time: Start time in HH:MM format
            end_time: End time in HH:MM format

        Returns:
            List[Meal]: Meals within the time range
        """
        return self.meal_service.get_meals_by_time_range(
            meal_plan.meals, 
            start_time, 
            end_time
)

    def get_meals_by_recipe(self, meal_plan: MealPlan, recipe_title: str) -> List[Meal]:
        """Get meals containing a specific recipe.

        Args:
            meal_plan: Meal plan
            recipe_title: Recipe title

        Returns:
            List[Meal]: Meals containing the recipe
        """
        return self.meal_service.get_meals_by_recipe(meal_plan.meals, recipe_title)

    def get_all_recipes(self, meal_plan: MealPlan) -> List[str]:
        """Get all unique recipe titles in meal plan.

        Args:
            meal_plan: Meal plan

        Returns:
            List[str]: Unique recipe titles
        """
        recipes = set()
        for meal in meal_plan.meals:
            for recipe in meal.recipes:
                recipes.add(recipe.title)

        return sorted(list(recipes))

    def get_meal_distribution(self, meal_plan: MealPlan) -> dict[str, int]:
        """Get distribution of meal types.

        Args:
            meal_plan: Meal plan

        Returns:
            dict[str, int]: Meal type distribution
        """
        distribution = {}
        for meal in meal_plan.meals:
            distribution[meal.type] = distribution.get(meal.type, 0) + 1

        return distribution

    def format_meal_plan(self, meal_plan: MealPlan) -> str:
        """Format meal plan as text.

        Args:
            meal_plan: Meal plan to format

        Returns:
            str: Formatted meal plan
        """
        # Format metadata
        lines = [self.metadata_service.format_metadata(meal_plan.metadata), ""]

        # Group meals by date
        meals_by_date = {}
        for meal in meal_plan.meals:
            if meal.date not in meals_by_date:
                meals_by_date[meal.date] = []
            meals_by_date[meal.date].append(meal)

        # Format meals by date
        for date in sorted(meals_by_date.keys()):
            lines.extend([
                f"## {date}", 
                ""
            ])

            # Sort meals by time
            meals = sorted(
                meals_by_date[date], 
                key = lambda m: datetime.strptime(m.time, "%H:%M")
)

            # Format each meal
            for meal in meals:
                lines.extend([
                    self.meal_service.format_meal(meal), 
                    ""
                ])

        return "\n".join(lines)

    def validate_meal_plan(self, meal_plan: MealPlan) -> None:
        """Validate meal plan.

        Args:
            meal_plan: Meal plan to validate

        Raises:
            MealPlanValidationError: If meal plan is invalid
        """
        # Validate title
        if not meal_plan.title:
            raise MealPlanValidationError("Meal plan title is required")

        # Validate meals
        if not meal_plan.meals:
            raise MealPlanValidationError("Meal plan must have at least one meal")

        # Validate metadata
        self.metadata_service.validate_metadata(meal_plan.metadata)

        # Validate each meal
        for meal in meal_plan.meals:
            self.meal_service.validate_meal(meal)

        # Validate meal dates are within plan dates
        for meal in meal_plan.meals:
            if not (meal_plan.metadata.start_date <= meal.date <= meal_plan.metadata.end_date):
                raise MealPlanValidationError(
                    f"Meal date {meal.date} is outside plan dates "
                    f"{meal_plan.metadata.start_date} - {meal_plan.metadata.end_date}"
)

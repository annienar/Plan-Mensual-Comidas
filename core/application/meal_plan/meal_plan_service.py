"""
Meal plan application service.

This module contains the meal plan application service.
"""

from ...domain.meal_plan.repositories.meal_plan_repository import MealPlanRepository
from datetime import datetime, timedelta
from typing import List, Optional

from ...domain.events.dispatcher import EventDispatcher
from ...domain.events.handlers import MealPlanEventHandler, EventLogger
from ...domain.meal_plan.models.meal import Meal
from ...domain.meal_plan.models.meal_plan import MealPlan
from ...domain.meal_plan.models.metadata import MealPlanMetadata
from ...domain.meal_plan.services.meal_plan_service import MealPlanService

class MealPlanApplicationService:
    """Meal plan application service.

    This service handles meal plan - related use cases.
    """

    def __init__(self, meal_plan_repository: MealPlanRepository):
        """Initialize the service.

        Args:
            meal_plan_repository: Meal plan repository
        """
        # Create event dispatcher
        self.event_dispatcher = EventDispatcher()

        # Create domain service
        self.meal_plan_service = MealPlanService(self.event_dispatcher)

        # Store repository
        self.meal_plan_repository = meal_plan_repository

    async def create_meal_plan(self, meal_plan: MealPlan) -> MealPlan:
        """Create a meal plan.

        Args:
            meal_plan: Meal plan to create

        Returns:
            MealPlan: Created meal plan
        """
        # Create meal plan
        created_meal_plan = await self.meal_plan_service.create_meal_plan(meal_plan)

        # Save meal plan
        await self.meal_plan_repository.save(created_meal_plan)

        return created_meal_plan

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
        """
        # Update meal plan
        updated_meal_plan = await self.meal_plan_service.update_meal_plan(
            meal_plan, 
            changes
)

        # Save meal plan
        await self.meal_plan_repository.save(updated_meal_plan)

        return updated_meal_plan

    async def delete_meal_plan(self, meal_plan: MealPlan) -> None:
        """Delete a meal plan.

        Args:
            meal_plan: Meal plan to delete
        """
        # Delete meal plan
        await self.meal_plan_service.delete_meal_plan(meal_plan)

        # Delete from repository
        await self.meal_plan_repository.delete(meal_plan)

    async def add_meal(self, meal_plan: MealPlan, meal: Meal) -> MealPlan:
        """Add a meal to a meal plan.

        Args:
            meal_plan: Meal plan to add meal to
            meal: Meal to add

        Returns:
            MealPlan: Updated meal plan
        """
        # Add meal
        updated_meal_plan = await self.meal_plan_service.add_meal(meal_plan, meal)

        # Save meal plan
        await self.meal_plan_repository.save(updated_meal_plan)

        return updated_meal_plan

    async def remove_meal(self, meal_plan: MealPlan, meal: Meal) -> MealPlan:
        """Remove a meal from a meal plan.

        Args:
            meal_plan: Meal plan to remove meal from
            meal: Meal to remove

        Returns:
            MealPlan: Updated meal plan
        """
        # Remove meal
        updated_meal_plan = await self.meal_plan_service.remove_meal(meal_plan, meal)

        # Save meal plan
        await self.meal_plan_repository.save(updated_meal_plan)

        return updated_meal_plan

    def get_meals_by_date(self, meal_plan: MealPlan, date: str) -> List[Meal]:
        """Get meals for a specific date.

        Args:
            meal_plan: Meal plan
            date: Date in YYYY - MM - DD format

        Returns:
            List[Meal]: Meals for the date
        """
        return self.meal_plan_service.get_meals_by_date(meal_plan, date)

    def get_meals_by_type(self, meal_plan: MealPlan, type: str) -> List[Meal]:
        """Get meals of a specific type.

        Args:
            meal_plan: Meal plan
            type: Meal type

        Returns:
            List[Meal]: Meals of the type
        """
        return self.meal_plan_service.get_meals_by_type(meal_plan, type)

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
        return self.meal_plan_service.get_meals_by_time_range(
            meal_plan, 
            start_time, 
            end_time
)

    def get_all_recipes(self, meal_plan: MealPlan) -> List[str]:
        """Get all recipes in a meal plan.

        Args:
            meal_plan: Meal plan

        Returns:
            List[str]: List of recipe titles
        """
        return self.meal_plan_service.get_all_recipes(meal_plan)

    def get_meal_distribution(self, meal_plan: MealPlan) -> dict[str, int]:
        """Get meal type distribution in a meal plan.

        Args:
            meal_plan: Meal plan

        Returns:
            dict[str, int]: Meal type distribution
        """
        return self.meal_plan_service.get_meal_distribution(meal_plan)

    def format_meal_plan(self, meal_plan: MealPlan) -> str:
        """Format meal plan as text.

        Args:
            meal_plan: Meal plan

        Returns:
            str: Formatted meal plan
        """
        return self.meal_plan_service.format_meal_plan(meal_plan)

    async def get_meal_plan(self, title: str) -> Optional[MealPlan]:
        """Get a meal plan by title.

        Args:
            title: Meal plan title

        Returns:
            Optional[MealPlan]: Meal plan if found
        """
        return await self.meal_plan_repository.find_by_title(title)

    async def get_all_meal_plans(self) -> List[MealPlan]:
        """Get all meal plans.

        Returns:
            List[MealPlan]: List of meal plans
        """
        return await self.meal_plan_repository.find_all()

    async def search_meal_plans(self, query: str) -> List[MealPlan]:
        """Search meal plans.

        Args:
            query: Search query

        Returns:
            List[MealPlan]: Matching meal plans
        """
        return await self.meal_plan_repository.search(query)

    async def get_meal_plans_by_date_range(
        self, 
        start_date: str, 
        end_date: str
) -> List[MealPlan]:
        """Get meal plans within a date range.

        Args:
            start_date: Start date in YYYY - MM - DD format
            end_date: End date in YYYY - MM - DD format

        Returns:
            List[MealPlan]: Meal plans within the date range
        """
        return await self.meal_plan_repository.find_by_date_range(
            start_date, 
            end_date
)

    async def get_meal_plans_by_recipe(self, recipe_title: str) -> List[MealPlan]:
        """Get meal plans containing a recipe.

        Args:
            recipe_title: Recipe title

        Returns:
            List[MealPlan]: Meal plans containing the recipe
        """
        return await self.meal_plan_repository.find_by_recipe(recipe_title)

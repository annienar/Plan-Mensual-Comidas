"""
Meal service.

This module contains the meal domain service.
"""

from ...recipe.models.recipe import Recipe
from datetime import datetime, timedelta
from typing import List, Optional

from ...exceptions.meal_plan import MealPlanValidationError
from ..models.meal import Meal

class MealService:
    """Meal service.

    This service handles meal - related business logic.
    """

    @staticmethod
    def get_meals_by_date(meals: List[Meal], date: str) -> List[Meal]:
        """Get meals for a specific date.

        Args:
            meals: List of meals
            date: Date in YYYY - MM - DD format

        Returns:
            List[Meal]: Meals for the date
        """
        return [meal for meal in meals if meal.date == date]

    @staticmethod
    def get_meals_by_type(meals: List[Meal], type: str) -> List[Meal]:
        """Get meals of a specific type.

        Args:
            meals: List of meals
            type: Meal type

        Returns:
            List[Meal]: Meals of the type
        """
        return [meal for meal in meals if meal.type == type]

    @staticmethod
    def get_meals_by_time_range(
        meals: List[Meal], 
        start_time: str, 
        end_time: str
) -> List[Meal]:
        """Get meals within a time range.

        Args:
            meals: List of meals
            start_time: Start time in HH:MM format
            end_time: End time in HH:MM format

        Returns:
            List[Meal]: Meals within the time range

        Raises:
            MealPlanValidationError: If time format is invalid
        """
        try:
            start = datetime.strptime(start_time, "%H:%M")
            end = datetime.strptime(end_time, "%H:%M")
        except ValueError:
            raise MealPlanValidationError("Invalid time format. Must be HH:MM")

        return [
            meal for meal in meals
            if start <= datetime.strptime(meal.time, "%H:%M") <= end
        ]

    @staticmethod
    def get_meals_by_recipe(meals: List[Meal], recipe_title: str) -> List[Meal]:
        """Get meals containing a specific recipe.

        Args:
            meals: List of meals
            recipe_title: Recipe title

        Returns:
            List[Meal]: Meals containing the recipe
        """
        return [
            meal for meal in meals
            if any(recipe.title == recipe_title for recipe in meal.recipes)
        ]

    @staticmethod
    def format_meal(meal: Meal) -> str:
        """Format meal as text.

        Args:
            meal: Meal to format

        Returns:
            str: Formatted meal
        """
        # Format title
        lines = [f"# {meal.title}", ""]

        # Format metadata
        lines.extend([
            "## Metadata", 
            f"- Tipo: {meal.type}", 
            f"- Hora: {meal.time}", 
            f"- Fecha: {meal.date}", 
            ""
        ])

        # Format recipes
        lines.extend([
            "## Recetas", 
            *[f"- {recipe.title}" for recipe in meal.recipes], 
            ""
        ])

        # Format notes
        if meal.notes:
            lines.extend([
                "## Notas", 
                meal.notes, 
                ""
            ])

        return "\n".join(lines)

    @staticmethod
    def validate_meal(meal: Meal) -> None:
        """Validate meal.

        Args:
            meal: Meal to validate

        Raises:
            MealPlanValidationError: If meal is invalid
        """
        # Validate title
        if not meal.title:
            raise MealPlanValidationError("Meal title is required")

        # Validate type
        valid_types = ["Desayuno", "Almuerzo", "Cena", "Snack"]
        if meal.type not in valid_types:
            raise MealPlanValidationError(
                f"Invalid meal type: {meal.type}. Must be one of {valid_types}"
)

        # Validate time
        try:
            datetime.strptime(meal.time, "%H:%M")
        except ValueError:
            raise MealPlanValidationError("Invalid time format. Must be HH:MM")

        # Validate date
        try:
            datetime.strptime(meal.date, "%Y-%m-%d")
        except ValueError:
            raise MealPlanValidationError("Invalid date format. Must be YYYY - MM - DD")

        # Validate recipes
        if not meal.recipes:
            raise MealPlanValidationError("Meal must have at least one recipe")

        for recipe in meal.recipes:
            if not recipe.title:
                raise MealPlanValidationError("Recipe title is required")

        # Validate notes
        if meal.notes is not None and not meal.notes:
            raise MealPlanValidationError("Notes cannot be empty")

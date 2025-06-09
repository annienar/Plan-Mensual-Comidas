"""
Main application module.

This module contains the main application entry point.
"""

from core.domain.events.dispatcher import EventDispatcher
from core.domain.events.handlers import (
from core.domain.meal_plan.models.meal import Meal
from core.domain.meal_plan.models.meal_plan import MealPlan
from core.domain.meal_plan.models.metadata import MealPlanMetadata
from core.domain.recipe.models.ingredient import Ingredient
from core.domain.recipe.models.metadata import RecipeMetadata
from core.domain.recipe.models.recipe import Recipe
from datetime import datetime, timedelta
from typing import List, Optional

import asyncio
    RecipeEventHandler, 
    MealPlanEventHandler, 
    EventLogger
)
from core.domain.events import (
    RecipeCreated, 
    RecipeUpdated, 
    RecipeDeleted, 
    RecipeScaled, 
    MealPlanCreated, 
    MealPlanUpdated, 
    MealPlanDeleted, 
    MealAdded, 
    MealRemoved
)
from core.infrastructure.repositories.recipe_repository import InMemoryRecipeRepository
from core.infrastructure.repositories.meal_plan_repository import InMemoryMealPlanRepository
from core.application.recipe.service import RecipeService
from core.application.meal_plan.meal_plan_service import MealPlanApplicationService

async def main():
    """Main application entry point."""
    # Create event dispatcher
    event_dispatcher = EventDispatcher()

    # Create event handlers
    event_logger = EventLogger()
    recipe_event_handler = RecipeEventHandler(event_logger)
    meal_plan_event_handler = MealPlanEventHandler(event_logger)

    # Register event handlers
    event_dispatcher.register(
        RecipeCreated, 
        recipe_event_handler.handle_recipe_created
)
    event_dispatcher.register(
        RecipeUpdated, 
        recipe_event_handler.handle_recipe_updated
)
    event_dispatcher.register(
        RecipeDeleted, 
        recipe_event_handler.handle_recipe_deleted
)
    event_dispatcher.register(
        RecipeScaled, 
        recipe_event_handler.handle_recipe_scaled
)
    event_dispatcher.register(
        MealPlanCreated, 
        meal_plan_event_handler.handle_meal_plan_created
)
    event_dispatcher.register(
        MealPlanUpdated, 
        meal_plan_event_handler.handle_meal_plan_updated
)
    event_dispatcher.register(
        MealPlanDeleted, 
        meal_plan_event_handler.handle_meal_plan_deleted
)
    event_dispatcher.register(
        MealAdded, 
        meal_plan_event_handler.handle_meal_added
)
    event_dispatcher.register(
        MealRemoved, 
        meal_plan_event_handler.handle_meal_removed
)

    # Create repositories
    recipe_repository = InMemoryRecipeRepository(event_dispatcher)
    meal_plan_repository = InMemoryMealPlanRepository(event_dispatcher)

    # Create application services
    # Note: RecipeService requires notion_client and llm_client which we don't have in this demo
    # recipe_service = RecipeService(notion_client, llm_client, recipe_repository)
    meal_plan_service = MealPlanApplicationService(meal_plan_repository)

    # Create a recipe
    recipe = Recipe(
        title="Pasta Carbonara", 
        ingredients=[
            Ingredient(name="Spaghetti", quantity = 500, unit="g"), 
            Ingredient(name="Bacon", quantity = 200, unit="g"), 
            Ingredient(name="Eggs", quantity = 4, unit = None), 
            Ingredient(name="Parmesan cheese", quantity = 100, unit="g"), 
            Ingredient(name="Black pepper", quantity = 2, unit="tsp"), 
            Ingredient(name="Salt", quantity = 1, unit="tsp")
        ], 
        instructions=[
            "Cook pasta according to package instructions", 
            "Fry bacon until crispy", 
            "Mix eggs, cheese, and pepper", 
            "Combine pasta with bacon and egg mixture", 
            "Serve immediately"
        ], 
        metadata = RecipeMetadata(
            title="Pasta Carbonara", 
            porciones = 4, 
            calorias = 600, 
            tiempo_preparacion = 15, 
            tiempo_coccion = 20, 
            dificultad="Media", 
            date="2024 - 03 - 18", 
            tags=["pasta", "italiana", "rápida"]
)
)

    # Create meal plan
    meal_plan = MealPlan(
        title="Plan Semanal", 
        meals=[
            Meal(
                title="Almuerzo Carbonara", 
                type="Almuerzo", 
                date="2024 - 03 - 18", 
                time="13:00", 
                recipes=[recipe]
)
        ], 
        metadata = MealPlanMetadata(
            title="Plan Semanal", 
            start_date="2024 - 03 - 18", 
            end_date="2024 - 03 - 24", 
            description="Plan de comidas para la semana"
)
)

    # Save recipe (commented out - needs proper recipe service setup)
    # await recipe_service.create_recipe(recipe)

    # Save meal plan
    await meal_plan_service.create_meal_plan(meal_plan)

    # Get all recipes (commented out - needs proper recipe service setup)
    # recipes = await recipe_service.get_all_recipes()
    # print("\nRecipes:")
    # for r in recipes:
    #     print(f"- {r.title}")

    # Get all meal plans
    meal_plans = await meal_plan_service.get_all_meal_plans()
    print("\nMeal Plans:")
    for mp in meal_plans:
        print(f"- {mp.title}")

    # Format recipe (commented out - needs proper recipe service setup)
    # print("\nRecipe Format:")
    # print(recipe_service.format_recipe(recipe))

    # Format meal plan
    print("\nMeal Plan Format:")
    print(meal_plan_service.format_meal_plan(meal_plan))

if __name__ == "__main__":
    asyncio.run(main())

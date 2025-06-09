"""
Recipe repository.

This module contains the recipe repository implementation.
"""

from datetime import datetime
from typing import List, Optional

from ...domain.events.dispatcher import EventDispatcher
from ...domain.events.recipe import (
    RecipeCreated, 
    RecipeUpdated, 
    RecipeDeleted
)
from ...domain.recipe.models.recipe import Recipe
from ...domain.recipe.repositories.recipe_repository import RecipeRepository

class InMemoryRecipeRepository(RecipeRepository):
    """In - memory recipe repository.

    This repository stores recipes in memory.
    """

    def __init__(self, event_dispatcher: EventDispatcher):
        """Initialize the repository.

        Args:
            event_dispatcher: Event dispatcher
        """
        self.recipes: List[Recipe] = []
        self.event_dispatcher = event_dispatcher

    async def save(self, recipe: Recipe) -> None:
        """Save a recipe.

        Args:
            recipe: Recipe to save
        """
        # Check if recipe exists
        existing_recipe = await self.find_by_title(recipe.title)

        if existing_recipe:
            # Update existing recipe
            index = self.recipes.index(existing_recipe)
            self.recipes[index] = recipe

            # Create event
            event = RecipeUpdated(recipe, {})

            # Dispatch event
            await self.event_dispatcher.dispatch(event)
        else:
            # Add new recipe
            self.recipes.append(recipe)

            # Create event
            event = RecipeCreated(recipe)

            # Dispatch event
            await self.event_dispatcher.dispatch(event)

    async def delete(self, recipe: Recipe) -> None:
        """Delete a recipe.

        Args:
            recipe: Recipe to delete
        """
        # Remove recipe
        self.recipes = [r for r in self.recipes if r.title != recipe.title]

        # Create event
        event = RecipeDeleted(recipe.title)

        # Dispatch event
        await self.event_dispatcher.dispatch(event)

    async def find_by_title(self, title: str) -> Optional[Recipe]:
        """Find a recipe by title.

        Args:
            title: Recipe title

        Returns:
            Optional[Recipe]: Recipe if found, None otherwise
        """
        for recipe in self.recipes:
            if recipe.title == title:
                return recipe

        return None

    async def find_all(self) -> List[Recipe]:
        """Find all recipes.

        Returns:
            List[Recipe]: All recipes
        """
        return self.recipes.copy()

    async def search(self, query: str) -> List[Recipe]:
        """Search recipes.

        Args:
            query: Search query

        Returns:
            List[Recipe]: Matching recipes
        """
        query = query.lower()

        return [
            recipe for recipe in self.recipes
            if query in recipe.title.lower() or
            any(query in ingredient.name.lower() for ingredient in recipe.ingredients) or
            any(query in instruction.lower() for instruction in recipe.instructions) or
            any(query in tag.lower() for tag in recipe.metadata.tags)
        ]

    async def find_by_tag(self, tag: str) -> List[Recipe]:
        """Find recipes by tag.

        Args:
            tag: Tag to search for

        Returns:
            List[Recipe]: Recipes with the tag
        """
        return [
            recipe for recipe in self.recipes
            if tag in recipe.metadata.tags
        ]

    async def find_by_difficulty(self, difficulty: str) -> List[Recipe]:
        """Find recipes by difficulty.

        Args:
            difficulty: Difficulty level

        Returns:
            List[Recipe]: Recipes with the difficulty
        """
        return [
            recipe for recipe in self.recipes
            if recipe.metadata.dificultad == difficulty
        ]

    async def find_by_time_range(
        self, 
        min_time: int, 
        max_time: int
) -> List[Recipe]:
        """Find recipes by time range.

        Args:
            min_time: Minimum time in minutes
            max_time: Maximum time in minutes

        Returns:
            List[Recipe]: Recipes within the time range
        """
        return [
            recipe for recipe in self.recipes
            if min_time <= recipe.metadata.tiempo_preparacion + recipe.metadata.tiempo_coccion <= max_time
        ]

    async def find_by_calories_range(
        self, 
        min_calories: int, 
        max_calories: int
) -> List[Recipe]:
        """Find recipes by calories range.

        Args:
            min_calories: Minimum calories
            max_calories: Maximum calories

        Returns:
            List[Recipe]: Recipes within the calories range
        """
        return [
            recipe for recipe in self.recipes
            if min_calories <= recipe.metadata.calorias <= max_calories
        ]

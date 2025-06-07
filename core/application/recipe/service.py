"""
Recipe application service.

This module contains the recipe application service.
"""

import logging
from datetime import datetime
from typing import List, Optional, Dict, Any, Union

from core.domain.exceptions.recipe import (
    RecipeError, 
    RecipeValidationError, 
    RecipeGenerationError, 
    RecipeExtractionError, 
    RecipeNotFoundError, 
    RecipeDuplicateError
)
from core.domain.recipe.models.ingredient import Ingredient
from core.domain.recipe.models.metadata import RecipeMetadata
from core.domain.recipe.models.recipe import Recipe
from core.domain.recipe.services.recipe_service import RecipeService as DomainRecipeService
from core.domain.recipe.repositories.recipe_repository import RecipeRepository
from core.domain.events.dispatcher import EventDispatcher
from core.domain.events.handlers import RecipeEventHandler, EventLogger
from core.domain.events.recipe import (
    RecipeCreated, 
    RecipeUpdated, 
    RecipeDeleted, 
    RecipeScaled
)
from .processor import RecipeProcessor
from .notion_service import NotionRecipeService
from core.infrastructure.notion.client import NotionClient
from core.infrastructure.llm.client import LLMClient

logger = logging.getLogger(__name__)

class RecipeService:
    """Recipe application service.

    This service handles recipe - related use cases, combining domain
    operations with Notion integration.
    """

    def __init__(
        self, 
        notion_client: NotionClient, 
        llm_client: LLMClient, 
        recipe_repository: RecipeRepository, 
        processor: Optional[RecipeProcessor] = None
):
        """Initialize the service.

        Args:
            notion_client: Notion client
            llm_client: LLM client
            recipe_repository: Recipe repository
            processor: Recipe processor (optional)
        """
        # Create event dispatcher
        self.event_dispatcher = EventDispatcher()

        # Create event handlers
        self.event_logger = EventLogger()
        self.recipe_event_handler = RecipeEventHandler(self.event_logger)

        # Register event handlers
        self.event_dispatcher.register(
            RecipeCreated, 
            self.recipe_event_handler.handle_recipe_created
)
        self.event_dispatcher.register(
            RecipeUpdated, 
            self.recipe_event_handler.handle_recipe_updated
)
        self.event_dispatcher.register(
            RecipeDeleted, 
            self.recipe_event_handler.handle_recipe_deleted
)
        self.event_dispatcher.register(
            RecipeScaled, 
            self.recipe_event_handler.handle_recipe_scaled
)

        # Create domain service
        self.domain_service = DomainRecipeService(self.event_dispatcher)

        # Create Notion service
        self.notion_service = NotionRecipeService(
            notion_client = notion_client, 
            llm_client = llm_client, 
            processor = processor
)

        # Store repository
        self.recipe_repository = recipe_repository

    async def create_recipe(
        self, 
        title: str, 
        ingredients: List[Dict[str, Any]], 
        instructions: List[str], 
        metadata: Dict[str, Any]
) -> Recipe:
        """Create a recipe.

        Args:
            title: Recipe title
            ingredients: List of ingredients
            instructions: List of instructions
            metadata: Recipe metadata

        Returns:
            Recipe: Created recipe

        Raises:
            RecipeError: If creation fails
        """
        try:
            # Generate recipe
            recipe = await self.notion_service.generate_recipe(
                title = title, 
                ingredients = ingredients, 
                instructions = instructions, 
                metadata = metadata
)

            # Create recipe in domain
            created_recipe = await self.domain_service.create_recipe(recipe)

            # Save recipe
            await self.recipe_repository.save(created_recipe)

            # Save to Notion
            await self.notion_service.save_recipe(created_recipe)

            return created_recipe

        except RecipeError as e:
            logger.error(f"Recipe creation failed: {str(e)}")
            raise

        except Exception as e:
            logger.error(f"Unexpected error during recipe creation: {str(e)}")
            raise RecipeError(f"Unexpected error: {str(e)}")

    async def update_recipe(
        self, 
        page_id: str, 
        changes: Dict[str, Any]
) -> Recipe:
        """Update a recipe.

        Args:
            page_id: Notion page ID
            changes: Changes to apply

        Returns:
            Recipe: Updated recipe

        Raises:
            RecipeError: If update fails
        """
        try:
            # Get recipe from Notion
            recipe = await self.notion_service.get_recipe(page_id)

            # Update recipe in domain
            updated_recipe = await self.domain_service.update_recipe(recipe, changes)

            # Save recipe
            await self.recipe_repository.save(updated_recipe)

            # Update in Notion
            await self.notion_service.update_recipe(page_id, updated_recipe)

            return updated_recipe

        except RecipeError as e:
            logger.error(f"Recipe update failed: {str(e)}")
            raise

        except Exception as e:
            logger.error(f"Unexpected error during recipe update: {str(e)}")
            raise RecipeError(f"Unexpected error: {str(e)}")

    async def delete_recipe(self, page_id: str) -> None:
        """Delete a recipe.

        Args:
            page_id: Notion page ID

        Raises:
            RecipeError: If deletion fails
        """
        try:
            # Get recipe from Notion
            recipe = await self.notion_service.get_recipe(page_id)

            # Delete recipe in domain
            await self.domain_service.delete_recipe(recipe)

            # Delete from repository
            await self.recipe_repository.delete(recipe)

            # Delete from Notion
            await self.notion_service.delete_recipe(page_id)

        except RecipeError as e:
            logger.error(f"Recipe deletion failed: {str(e)}")
            raise

        except Exception as e:
            logger.error(f"Unexpected error during recipe deletion: {str(e)}")
            raise RecipeError(f"Unexpected error: {str(e)}")

    async def scale_recipe(self, page_id: str, factor: float) -> Recipe:
        """Scale recipe.

        Args:
            page_id: Notion page ID
            factor: Scaling factor

        Returns:
            Recipe: Scaled recipe

        Raises:
            RecipeError: If scaling fails
        """
        try:
            # Get recipe from Notion
            recipe = await self.notion_service.get_recipe(page_id)

            # Scale recipe in domain
            scaled_recipe = await self.domain_service.scale_recipe(recipe, factor)

            # Save recipe
            await self.recipe_repository.save(scaled_recipe)

            # Update in Notion
            await self.notion_service.update_recipe(page_id, scaled_recipe)

            return scaled_recipe

        except RecipeError as e:
            logger.error(f"Recipe scaling failed: {str(e)}")
            raise

        except Exception as e:
            logger.error(f"Unexpected error during recipe scaling: {str(e)}")
            raise RecipeError(f"Unexpected error: {str(e)}")

    async def merge_ingredients(self, page_id: str) -> Recipe:
        """Merge duplicate ingredients in recipe.

        Args:
            page_id: Notion page ID

        Returns:
            Recipe: Recipe with merged ingredients

        Raises:
            RecipeError: If merging fails
        """
        try:
            # Get recipe from Notion
            recipe = await self.notion_service.get_recipe(page_id)

            # Merge ingredients in domain
            merged_recipe = self.domain_service.merge_ingredients(recipe)

            # Save recipe
            await self.recipe_repository.save(merged_recipe)

            # Update in Notion
            await self.notion_service.update_recipe(page_id, merged_recipe)

            return merged_recipe

        except RecipeError as e:
            logger.error(f"Recipe merging failed: {str(e)}")
            raise

        except Exception as e:
            logger.error(f"Unexpected error during recipe merging: {str(e)}")
            raise RecipeError(f"Unexpected error: {str(e)}")

    async def suggest_tags(self, page_id: str) -> List[str]:
        """Suggest additional tags for recipe.

        Args:
            page_id: Notion page ID

        Returns:
            List[str]: Suggested tags

        Raises:
            RecipeError: If suggestion fails
        """
        try:
            # Get recipe from Notion
            recipe = await self.notion_service.get_recipe(page_id)

            # Suggest tags in domain
            return self.domain_service.suggest_tags(recipe)

        except RecipeError as e:
            logger.error(f"Tag suggestion failed: {str(e)}")
            raise

        except Exception as e:
            logger.error(f"Unexpected error during tag suggestion: {str(e)}")
            raise RecipeError(f"Unexpected error: {str(e)}")

    async def format_recipe(self, page_id: str) -> str:
        """Format recipe as text.

        Args:
            page_id: Notion page ID

        Returns:
            str: Formatted recipe

        Raises:
            RecipeError: If formatting fails
        """
        try:
            # Get recipe from Notion
            recipe = await self.notion_service.get_recipe(page_id)

            # Format recipe in domain
            return self.domain_service.format_recipe(recipe)

        except RecipeError as e:
            logger.error(f"Recipe formatting failed: {str(e)}")
            raise

        except Exception as e:
            logger.error(f"Unexpected error during recipe formatting: {str(e)}")
            raise RecipeError(f"Unexpected error: {str(e)}")

    async def get_recipe(self, page_id: str) -> Recipe:
        """Get a recipe.

        Args:
            page_id: Notion page ID

        Returns:
            Recipe: Retrieved recipe

        Raises:
            RecipeError: If retrieval fails
        """
        try:
            return await self.notion_service.get_recipe(page_id)

        except RecipeError as e:
            logger.error(f"Recipe retrieval failed: {str(e)}")
            raise

        except Exception as e:
            logger.error(f"Unexpected error during recipe retrieval: {str(e)}")
            raise RecipeError(f"Unexpected error: {str(e)}")

    async def list_recipes(self) -> List[Dict[str, Any]]:
        """List all recipes.

        Returns:
            List[Dict[str, Any]]: List of recipes

        Raises:
            RecipeError: If listing fails
        """
        try:
            return await self.notion_service.list_recipes()

        except RecipeError as e:
            logger.error(f"Recipe listing failed: {str(e)}")
            raise

        except Exception as e:
            logger.error(f"Unexpected error during recipe listing: {str(e)}")
            raise RecipeError(f"Unexpected error: {str(e)}")

    async def search_recipes(self, query: str) -> List[Dict[str, Any]]:
        """Search recipes.

        Args:
            query: Search query

        Returns:
            List[Dict[str, Any]]: Matching recipes

        Raises:
            RecipeError: If search fails
        """
        try:
            return await self.notion_service.search_recipes(query)

        except RecipeError as e:
            logger.error(f"Recipe search failed: {str(e)}")
            raise

        except Exception as e:
            logger.error(f"Unexpected error during recipe search: {str(e)}")
            raise RecipeError(f"Unexpected error: {str(e)}")

    async def get_recipes_by_tag(self, tag: str) -> List[Recipe]:
        """Get recipes by tag.

        Args:
            tag: Tag to search for

        Returns:
            List[Recipe]: Recipes with the tag

        Raises:
            RecipeError: If retrieval fails
        """
        try:
            return await self.recipe_repository.find_by_tag(tag)

        except RecipeError as e:
            logger.error(f"Recipe retrieval failed: {str(e)}")
            raise

        except Exception as e:
            logger.error(f"Unexpected error during recipe retrieval: {str(e)}")
            raise RecipeError(f"Unexpected error: {str(e)}")

    async def get_recipes_by_difficulty(self, difficulty: str) -> List[Recipe]:
        """Get recipes by difficulty.

        Args:
            difficulty: Difficulty level

        Returns:
            List[Recipe]: Recipes with the difficulty

        Raises:
            RecipeError: If retrieval fails
        """
        try:
            return await self.recipe_repository.find_by_difficulty(difficulty)

        except RecipeError as e:
            logger.error(f"Recipe retrieval failed: {str(e)}")
            raise

        except Exception as e:
            logger.error(f"Unexpected error during recipe retrieval: {str(e)}")
            raise RecipeError(f"Unexpected error: {str(e)}")

    async def get_recipes_by_time_range(
        self, 
        min_time: int, 
        max_time: int
) -> List[Recipe]:
        """Get recipes by time range.

        Args:
            min_time: Minimum time in minutes
            max_time: Maximum time in minutes

        Returns:
            List[Recipe]: Recipes within the time range

        Raises:
            RecipeError: If retrieval fails
        """
        try:
            return await self.recipe_repository.find_by_time_range(min_time, max_time)

        except RecipeError as e:
            logger.error(f"Recipe retrieval failed: {str(e)}")
            raise

        except Exception as e:
            logger.error(f"Unexpected error during recipe retrieval: {str(e)}")
            raise RecipeError(f"Unexpected error: {str(e)}")

    async def get_recipes_by_calories_range(
        self, 
        min_calories: int, 
        max_calories: int
) -> List[Recipe]:
        """Get recipes by calories range.

        Args:
            min_calories: Minimum calories
            max_calories: Maximum calories

        Returns:
            List[Recipe]: Recipes within the calories range

        Raises:
            RecipeError: If retrieval fails
        """
        try:
            return await self.recipe_repository.find_by_calories_range(
                min_calories, 
                max_calories
)

        except RecipeError as e:
            logger.error(f"Recipe retrieval failed: {str(e)}")
            raise

        except Exception as e:
            logger.error(f"Unexpected error during recipe retrieval: {str(e)}")
            raise RecipeError(f"Unexpected error: {str(e)}")

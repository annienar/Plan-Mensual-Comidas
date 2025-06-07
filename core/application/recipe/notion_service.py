"""
Recipe service.

This module contains the recipe service implementation.
"""
from core.domain.exceptions.recipe import RecipeError, RecipeValidationError, RecipeGenerationError, RecipeExtractionError, RecipeNotFoundError, RecipeDuplicateError
from core.domain.recipe.models.ingredient import Ingredient
from core.domain.recipe.models.metadata import RecipeMetadata
from core.domain.recipe.models.recipe import Recipe
from core.infrastructure.llm.client import LLMClient
from core.infrastructure.notion.client import NotionClient
from datetime import datetime
from typing import List, Optional, Dict, Any, Union

from .processor import RecipeProcessor
from pydantic import BaseModel, Field, validator
import logging
logger = logging.getLogger(__name__)

class NotionRecipeService:
    """Recipe service.

    This class handles recipe operations, including generation, 
    extraction, storage, and retrieval.
    """

    def __init__(self, notion_client: NotionClient, llm_client: LLMClient, 
                processor: Optional[RecipeProcessor] = None) -> None:
        """Initialize the service.

        Args:
            notion_client: Notion client
            llm_client: LLM client
            processor: Recipe processor (optional)
        """
        self.notion_client = notion_client
        self.llm_client = llm_client
        self.processor = processor or RecipeProcessor()

    async def generate_recipe(self, title: str, ingredients: List[Dict[str, 
        Any]], instructions: List[str], metadata: Dict[str, Any]) ->Recipe:
        """Generate a recipe.

        Args:
            title: Recipe title
            ingredients: List of ingredients
            instructions: List of instructions
            metadata: Recipe metadata

        Returns:
            Recipe: Generated recipe

        Raises:
            RecipeGenerationError: If generation fails
        """
        try:
            recipe = Recipe(title = title, ingredients=[Ingredient(nombre = ing[
                'nombre'], cantidad = ing.get('cantidad'), unidad = ing.get('unidad')) for
                ing in ingredients], instructions = instructions, metadata=
                RecipeMetadata(**metadata))
            self.processor.validate_recipe(recipe)
            return recipe
        except RecipeError as e:
            logger.error(f'Recipe generation failed: {str(e)}')
            raise
        except Exception as e:
            logger.error(f'Unexpected error during recipe generation: {str(e)}'
)
            raise RecipeGenerationError(f'Unexpected error: {str(e)}')

    async def extract_recipe(self, text: str) ->Recipe:
        """Extract a recipe from text.

        Args:
            text: Text to extract from

        Returns:
            Recipe: Extracted recipe

        Raises:
            RecipeExtractionError: If extraction fails
        """
        try:
            return self.processor.extract_recipe(text)
        except RecipeError as e:
            logger.error(f'Recipe extraction failed: {str(e)}')
            raise
        except Exception as e:
            logger.error(f'Unexpected error during recipe extraction: {str(e)}'
)
            raise RecipeExtractionError(f'Unexpected error: {str(e)}')

    async def process_recipe(self, recipe: Recipe) ->Dict[str, Any]:
        """Process a recipe.

        Args:
            recipe: Recipe to process

        Returns:
            Dict[str, Any]: Processed recipe in different formats

        Raises:
            RecipeError: If processing fails
        """
        try:
            return self.processor.process_recipe(recipe)
        except RecipeError as e:
            logger.error(f'Recipe processing failed: {str(e)}')
            raise
        except Exception as e:
            logger.error(f'Unexpected error during recipe processing: {str(e)}'
)
            raise RecipeError(f'Unexpected error: {str(e)}')

    async def process_text(self, text: str) ->Dict[str, Any]:
        """Process text into a recipe.

        Args:
            text: Text to process

        Returns:
            Dict[str, Any]: Processed recipe in different formats

        Raises:
            RecipeError: If processing fails
        """
        try:
            return self.processor.process_text(text)
        except RecipeError as e:
            logger.error(f'Text processing failed: {str(e)}')
            raise
        except Exception as e:
            logger.error(f'Unexpected error during text processing: {str(e)}')
            raise RecipeError(f'Unexpected error: {str(e)}')

    async def save_recipe(self, recipe: Recipe) ->str:
        """Save a recipe to Notion.

        Args:
            recipe: Recipe to save

        Returns:
            str: Notion page ID

        Raises:
            RecipeError: If saving fails
        """
        try:
            processed = await self.process_recipe(recipe)
            page_id = await self.notion_client.create_page(title = recipe.
                title, blocks = processed['notion_blocks'])
            return page_id
        except RecipeError as e:
            logger.error(f'Recipe saving failed: {str(e)}')
            raise
        except Exception as e:
            logger.error(f'Unexpected error during recipe saving: {str(e)}')
            raise RecipeError(f'Unexpected error: {str(e)}')

    async def get_recipe(self, page_id: str) ->Recipe:
        """Get a recipe from Notion.

        Args:
            page_id: Notion page ID

        Returns:
            Recipe: Retrieved recipe

        Raises:
            RecipeNotFoundError: If recipe not found
            RecipeError: If retrieval fails
        """
        try:
            page = await self.notion_client.get_page(page_id)
            if not page:
                raise RecipeNotFoundError(f'Recipe not found: {page_id}')
            return await self.extract_recipe(page['content'])
        except RecipeNotFoundError as e:
            logger.error(f'Recipe not found: {str(e)}')
            raise
        except RecipeError as e:
            logger.error(f'Recipe retrieval failed: {str(e)}')
            raise
        except Exception as e:
            logger.error(f'Unexpected error during recipe retrieval: {str(e)}')
            raise RecipeError(f'Unexpected error: {str(e)}')

    async def update_recipe(self, page_id: str, recipe: Recipe) ->None:
        """Update a recipe in Notion.

        Args:
            page_id: Notion page ID
            recipe: Updated recipe

        Raises:
            RecipeNotFoundError: If recipe not found
            RecipeError: If update fails
        """
        try:
            processed = await self.process_recipe(recipe)
            success = await self.notion_client.update_page(page_id = page_id, 
                title = recipe.title, blocks = processed['notion_blocks'])
            if not success:
                raise RecipeNotFoundError(f'Recipe not found: {page_id}')
        except RecipeNotFoundError as e:
            logger.error(f'Recipe not found: {str(e)}')
            raise
        except RecipeError as e:
            logger.error(f'Recipe update failed: {str(e)}')
            raise
        except Exception as e:
            logger.error(f'Unexpected error during recipe update: {str(e)}')
            raise RecipeError(f'Unexpected error: {str(e)}')

    async def delete_recipe(self, page_id: str) ->None:
        """Delete a recipe from Notion.

        Args:
            page_id: Notion page ID

        Raises:
            RecipeNotFoundError: If recipe not found
            RecipeError: If deletion fails
        """
        try:
            success = await self.notion_client.delete_page(page_id)
            if not success:
                raise RecipeNotFoundError(f'Recipe not found: {page_id}')
        except RecipeNotFoundError as e:
            logger.error(f'Recipe not found: {str(e)}')
            raise
        except RecipeError as e:
            logger.error(f'Recipe deletion failed: {str(e)}')
            raise
        except Exception as e:
            logger.error(f'Unexpected error during recipe deletion: {str(e)}')
            raise RecipeError(f'Unexpected error: {str(e)}')

    async def list_recipes(self) ->List[Dict[str, Any]]:
        """List all recipes from Notion.

        Returns:
            List[Dict[str, Any]]: List of recipes

        Raises:
            RecipeError: If listing fails
        """
        try:
            pages = await self.notion_client.list_pages()
            recipes = []
            for page in pages:
                try:
                    recipe = await self.extract_recipe(page['content'])
                    recipes.append({'id': page['id'], 'title': recipe.title, 
                        'metadata': recipe.metadata.dict()})
                except RecipeError:
                    logger.warning(
                        f"Failed to extract recipe from page: {page['id']}")
                    continue
            return recipes
        except RecipeError as e:
            logger.error(f'Recipe listing failed: {str(e)}')
            raise
        except Exception as e:
            logger.error(f'Unexpected error during recipe listing: {str(e)}')
            raise RecipeError(f'Unexpected error: {str(e)}')

    async def search_recipes(self, query: str) ->List[Dict[str, Any]]:
        """Search recipes in Notion.

        Args:
            query: Search query

        Returns:
            List[Dict[str, Any]]: List of matching recipes

        Raises:
            RecipeError: If search fails
        """
        try:
            pages = await self.notion_client.search_pages(query)
            recipes = []
            for page in pages:
                try:
                    recipe = await self.extract_recipe(page['content'])
                    recipes.append({'id': page['id'], 'title': recipe.title, 
                        'metadata': recipe.metadata.dict()})
                except RecipeError:
                    logger.warning(
                        f"Failed to extract recipe from page: {page['id']}")
                    continue
            return recipes
        except RecipeError as e:
            logger.error(f'Recipe search failed: {str(e)}')
            raise
        except Exception as e:
            logger.error(f'Unexpected error during recipe search: {str(e)}')
            raise RecipeError(f'Unexpected error: {str(e)}')

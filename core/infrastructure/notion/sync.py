"""
Notion synchronization module.

Handles synchronization of recipes with Notion.
"""
from core.domain.recipe.generators.notion_blocks import recipe_to_notion_blocks
from core.domain.recipe.models.recipe import Recipe
from core.infrastructure.notion.client import NotionClient
from core.infrastructure.notion.errors import NotionAPIError
from core.infrastructure.notion.models import NotionPantryItem, NotionIngredient, NotionRecipe
from core.utils.logger import get_logger
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from typing import Any, Dict, List, Optional, cast
logger = get_logger('notion.sync')

class NotionSync:
    """Sync recipes and ingredients with Notion."""

    def __init__(self: Any, client: NotionClient, recipes_db_id: str, 
        ingredients_db_id: str, pantry_db_id: str) -> None:
        """Initialize the Notion sync."""
        self.client = client
        self.db_ids = {'Recetas': recipes_db_id, 'Ingredientes':
            ingredients_db_id, 'Alacena': pantry_db_id}
        self._test_page_ids: List[str] = []

    def check_connection(self: Any) ->bool:
        """
        Verify connection to Notion API.

        Returns:
            bool: True if connection is successful
        """
        try:
            self.client.client.users.me
            return True
        except Exception as e:
            logger.error(f'Failed to connect to Notion API: {e}')
            return False

    def check_database(self: Any) ->bool:
        """
        Verify access to the database.

        Returns:
            bool: True if database is accessible
        """
        try:
            self.client.client.databases.retrieve(self.db_ids['Recetas'])
            return True
        except Exception as e:
            logger.error(f'Failed to access Notion database: {e}')
            return False

    def check_recipe_exists(self: Any, title: str) -> Optional[str]:
        """Check if a recipe exists in Notion by title."""
        try:
            results = self.client.query_database(self.db_ids['Recetas'], {
                'property': 'Nombre', 'title': {'equals': title}})
            return results['results'][0]['id'] if results['results'] else None
        except Exception as e:
            raise NotionAPIError(f'Failed to check if recipe exists: {e}')

    async def sync_recipe(self, recipe: Recipe) ->Dict[str, Any]:
        """Sync a recipe to Notion."""
        try:
            recipe_page = await self.client.create_page(self.db_ids[
                'Recetas'], {'Nombre': {'title': [{'text': {'content':
                recipe.name}}]}, 'Porciones': {'number': recipe.servings}, 
                'Tiempo Total': {'number': recipe.prep_time + recipe.
                cook_time}, 'Calorías': {'number': recipe.calories}, 
                'Proteínas': {'number': recipe.protein}, 'Carbohidratos': {
                'number': recipe.carbs}, 'Grasas': {'number': recipe.fat}})
            return recipe_page
        except Exception as e:
            logger.error(f'Error syncing recipe to Notion: {str(e)}')
            raise NotionAPIError(f'Failed to sync recipe: {e}')

    @retry(stop = stop_after_attempt(3), wait = wait_exponential(multiplier = 1, 
        min = 2, max = 10), retry = retry_if_exception_type((NotionAPIError, 
        ConnectionError)))
    async def sync_ingredient(self, ingredient: NotionIngredient) ->Dict[
        str, Any]:
        """Sync an ingredient to Notion."""
        try:
            properties = {'Nombre': {'title': [{'text': {'content':
                ingredient.name}}]}, 'Cantidad Usada': {'number':
                ingredient.quantity}, 'Unidad': {'rich_text': [{'text': {
                'content': ingredient.unit}}]}, 'Receta': {'relation': [{
                'id': ingredient.receta_id}]}}
            results = await self.client.query_database(self.db_ids[
                'Ingredientes'], {'property': 'Nombre', 'title': {'equals':
                ingredient.name}})
            if results['results']:
                return await self.client.update_page(results['results'][0][
                    'id'], properties)
            else:
                return await self.client.create_page(self.db_ids[
                    'Ingredientes'], properties)
        except Exception as e:
            logger.error(f'Error syncing ingredient to Notion: {str(e)}')
            raise NotionAPIError(f'Failed to sync ingredient: {e}')

    @retry(stop = stop_after_attempt(3), wait = wait_exponential(multiplier = 1, 
        min = 2, max = 10), retry = retry_if_exception_type((NotionAPIError, 
        ConnectionError)))
    async def sync_pantry_item(self, pantry_item: NotionPantryItem) ->Dict[
        str, Any]:
        """Sync a pantry item to Notion."""
        try:
            properties = {'Nombre': {'title': [{'text': {'content':
                pantry_item.name}}]}, 'Unidad': {'rich_text': [{'text': {
                'content': pantry_item.unit}}]}, 'Stock': {'number':
                pantry_item.stock}}
            results = await self.client.query_database(self.db_ids[
                'Alacena'], {'property': 'Nombre', 'title': {'equals':
                pantry_item.name}})
            if results['results']:
                return await self.client.update_page(results['results'][0][
                    'id'], properties)
            else:
                return await self.client.create_page(self.db_ids['Alacena'], 
                    properties)
        except Exception as e:
            logger.error(f'Error syncing pantry item to Notion: {str(e)}')
            raise NotionAPIError(f'Failed to sync pantry item: {e}')

    def get_recipe(self: Any, page_id: str) ->Dict[str, Any]:
        """
        Get a recipe from Notion.

        Args:
            page_id: ID of the Notion page

        Returns:
            Dict[str, Any]: Recipe data

        Raises:
            NotionAPIError: If retrieval fails
        """
        try:
            return cast(Dict[str, Any], self.client.client.pages.retrieve(
                page_id))
        except Exception as e:
            logger.error(f'Failed to get recipe {page_id}: {e}')
            raise NotionAPIError(f'Failed to get recipe {page_id}: {e}')

    def sync_all_recipes(self: Any, recipes: List[Recipe]) ->List[Dict[str, 
        Any]]:
        """
        Synchronize multiple recipes.

        Args:
            recipes: List of recipes to synchronize

        Returns:
            List[Dict[str, Any]]: List of synchronization results
        """
        results = []
        for recipe in recipes:
            try:
                page_id = self.sync_recipe(recipe)
                results.append({'success': True, 'page_id': page_id, 
                    'error': None})
            except Exception as e:
                results.append({'success': False, 'page_id': None, 'error':
                    str(e)})
        return results

    def delete_recipe(self: Any, page_id: str) ->None:
        """
        Delete a recipe from Notion.

        Args:
            page_id: ID of the page to delete

        Raises:
            NotionAPIError: If deletion fails
        """
        try:
            self.client.client.pages.update(page_id = page_id, archived = True)
        except Exception as e:
            logger.error(f'Failed to delete recipe {page_id}: {e}')
            raise NotionAPIError(f'Failed to delete recipe {page_id}: {e}')

    def update_ingredient_with_recipe(self: Any, ingredient_id: str, 
        recipe_id: str) ->None:
        """
        Update an ingredient page in Notion to set the Receta relation.
        """
        try:
            properties = {'📚 Recetas Completas': {'relation': [{'id':
                recipe_id}]}}
            self.client.client.pages.update(page_id = ingredient_id, 
                properties = properties)
        except Exception as e:
            logger.error(
                f'Failed to update ingredient {ingredient_id} with recipe {recipe_id}: {e}'
)
            raise NotionAPIError(
                f'Failed to update ingredient {ingredient_id} with recipe {recipe_id}: {e}'
)

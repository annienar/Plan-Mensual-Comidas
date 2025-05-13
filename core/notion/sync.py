"""
Notion synchronization module.

Handles synchronization of recipes with Notion.
"""

from typing import Any, Dict, List, Optional, cast

from notion_client import Client

from core.recipe.models.recipe import Recipe
from core.utils.logger import get_logger

logger = get_logger("notion.sync")


class NotionSync:
    """Handles recipe synchronization with Notion."""

    def __init__(self, token: str, database_id: str) -> None:
        """
        Initialize Notion client.

        Args:
            token: Notion integration token
            database_id: ID of the recipes database
        """
        self.token = token
        self.database_id = database_id
        self.client = Client(auth=token)
        self._test_page_ids: List[str] = []

    def check_connection(self) -> bool:
        """
        Verify connection to Notion API.

        Returns:
            bool: True if connection is successful
        """
        try:
            self.client.users.me
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Notion API: {e}")
            return False

    def check_database(self) -> bool:
        """
        Verify access to the database.

        Returns:
            bool: True if database is accessible
        """
        try:
            self.client.databases.retrieve(self.database_id)
            return True
        except Exception as e:
            logger.error(f"Failed to access Notion database: {e}")
            return False

    def _recipe_exists(self, recipe_name: str) -> Optional[str]:
        """
        Check if a recipe exists by name.

        Args:
            recipe_name: Name of the recipe to check

        Returns:
            Optional[str]: Page ID if exists, None otherwise
        """
        try:
            response = cast(
                Dict[str, Any],
                self.client.databases.query(
                    database_id=self.database_id,
                    filter={"property": "Nombre", "title": {"equals": recipe_name}},
                ),
            )

            if response["results"]:
                return cast(str, response["results"][0]["id"])
            return None
        except Exception as e:
            logger.error(f"Failed to check recipe existence: {e}")
            return None

    def sync_recipe(self, recipe: Recipe) -> str:
        """
        Synchronize a recipe with Notion.

        Args:
            recipe: Recipe to synchronize

        Returns:
            str: ID of the created/updated Notion page

        Raises:
            Exception: If synchronization fails
        """
        # Check if recipe exists
        existing_id = self._recipe_exists(recipe.name)

        # Prepare properties for Notion
        properties = {
            "Nombre": {"title": [{"text": {"content": recipe.name}}]},
            "Fuente": {
                "url": recipe.source_url if recipe.source_url != "Desconocido" else None
            },
            "Porciones": {
                "number": recipe.servings if isinstance(recipe.servings, int) else None
            },
            "Ingredientes": {
                "rich_text": [{"text": {"content": str(recipe.ingredients)}}]
            },
            "Preparación": {
                "rich_text": [{"text": {"content": str(recipe.preparation_steps)}}]
            },
        }

        if recipe.calories:
            properties["Calorías"] = {"number": recipe.calories}

        try:
            if existing_id:
                # Update existing page
                response = cast(
                    Dict[str, Any],
                    self.client.pages.update(page_id=existing_id, properties=properties),
                )
            else:
                # Create new page
                response = cast(
                    Dict[str, Any],
                    self.client.pages.create(
                        parent={"database_id": self.database_id}, properties=properties
                    ),
                )

            return cast(str, response["id"])
        except Exception as e:
            logger.error(f"Failed to sync recipe {recipe.name}: {e}")
            raise

    def get_recipe(self, page_id: str) -> Dict[str, Any]:
        """
        Get a recipe from Notion.

        Args:
            page_id: ID of the Notion page

        Returns:
            Dict[str, Any]: Recipe data

        Raises:
            Exception: If retrieval fails
        """
        try:
            return cast(Dict[str, Any], self.client.pages.retrieve(page_id))
        except Exception as e:
            logger.error(f"Failed to get recipe {page_id}: {e}")
            raise

    def sync_all_recipes(self, recipes: List[Recipe]) -> List[Dict[str, Any]]:
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
                results.append({"success": True, "page_id": page_id, "error": None})
            except Exception as e:
                results.append({"success": False, "page_id": None, "error": str(e)})
        return results

    def delete_recipe(self, page_id: str) -> None:
        """
        Delete a recipe from Notion.

        Args:
            page_id: ID of the page to delete

        Raises:
            Exception: If deletion fails
        """
        try:
            self.client.pages.update(page_id=page_id, archived=True)
        except Exception as e:
            logger.error(f"Failed to delete recipe {page_id}: {e}")
            raise 
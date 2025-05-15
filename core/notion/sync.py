"""
Notion synchronization module.

Handles synchronization of recipes with Notion.
"""

from typing import Any, Dict, List, Optional, cast
from core.notion.client import NotionClient
from core.notion.errors import NotionAPIError
from core.recipe.models.recipe import Recipe
from core.utils.logger import get_logger
from core.notion.models import NotionPantryItem, NotionIngredient, NotionRecipe
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from core.recipe.generators.notion_blocks import recipe_to_notion_blocks

logger = get_logger("notion.sync")


class NotionSync:
    """Handles recipe synchronization with Notion."""

    def __init__(self, client: NotionClient, db_ids: dict) -> None:
        """
        Initialize Notion client.

        Args:
            client: Notion client
            db_ids: Dictionary containing database IDs
        """
        self.client = client
        self.recipe_db = db_ids['Recetas']
        self.ingredient_db = db_ids['Ingredientes']
        self.pantry_db = db_ids['Alacena']
        self._test_page_ids: List[str] = []

    def check_connection(self) -> bool:
        """
        Verify connection to Notion API.

        Returns:
            bool: True if connection is successful
        """
        try:
            self.client.client.users.me
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
            self.client.client.databases.retrieve(self.recipe_db)
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
                self.client.client.databases.query(
                    database_id=self.recipe_db,
                    filter={"property": "Nombre", "title": {"equals": recipe_name}},
                ),
            )

            if response["results"]:
                return cast(str, response["results"][0]["id"])
            return None
        except Exception as e:
            logger.error(f"Failed to check recipe existence: {e}")
            return None

    def sync_recipe(self, recipe: NotionRecipe) -> str:
        """
        Synchronize a recipe with Notion.

        Args:
            recipe: Recipe to synchronize

        Returns:
            str: ID of the created/updated Notion page

        Raises:
            NotionAPIError: If synchronization fails
        """
        # Check if recipe exists
        existing_id = self._recipe_exists(recipe.title)

        # Prepare properties for Notion (Recetas Completas)
        properties = {
            "Nombre": {"title": [{"text": {"content": recipe.title}}]},
            "Porciones": {"number": recipe.portions} if recipe.portions is not None else None,
            "Calorías": {"number": recipe.calories} if recipe.calories is not None else None,
            "Tags": {"multi_select": [{"name": tag} for tag in recipe.tags]} if recipe.tags else None,
            "Tipo": {"select": {"name": recipe.tipo}} if recipe.tipo else None,
            "Hecho": {"checkbox": recipe.hecho} if recipe.hecho is not None else None,
            "Date": {"date": {"start": recipe.date}} if recipe.date else None,
            "Dificultad": {"select": {"name": recipe.dificultad}} if recipe.dificultad else None,
            "Notas": {"rich_text": [{"text": {"content": recipe.notas}}]} if recipe.notas else None,
            "Tiempo preparación": {"number": recipe.tiempo_preparacion} if recipe.tiempo_preparacion is not None else None,
            "Tiempo cocción": {"number": recipe.tiempo_coccion} if recipe.tiempo_coccion is not None else None,
            "Tiempo total": {"number": recipe.tiempo_total} if recipe.tiempo_total is not None else None,
            "URL": {"url": recipe.url} if recipe.url else None,
        }
        # Add ingredient relations (to Ingredientes DB rows)
        if recipe.ingredient_ids:
            print("Setting Ingredientes relation with IDs:", recipe.ingredient_ids)
            properties["Ingredientes"] = {
                "relation": [{"id": ing_id} for ing_id in recipe.ingredient_ids]
            }
        # Remove None values
        properties = {k: v for k, v in properties.items() if v is not None}

        # Log the properties being sent to Notion
        logger.info(f"Syncing recipe '{recipe.title}' with properties: {properties}")

        try:
            if existing_id:
                response = cast(
                    Dict[str, Any],
                    self.client.client.pages.update(page_id=existing_id, properties=properties),
                )
                page_id = existing_id
            else:
                response = cast(
                    Dict[str, Any],
                    self.client.client.pages.create(
                        parent={"database_id": self.recipe_db}, properties=properties
                    ),
                )
                page_id = cast(str, response["id"])

            # Add formatted content blocks to the recipe page
            blocks = recipe_to_notion_blocks(recipe)
            if blocks:
                self.client.client.blocks.children.append(page_id=page_id, children=blocks)

            return page_id
        except Exception as e:
            logger.error(f"Failed to sync recipe {recipe.title}: {e}")
            raise NotionAPIError(f"Failed to sync recipe {recipe.title}: {e}")

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10), retry=retry_if_exception_type((NotionAPIError, ConnectionError)))
    def sync_ingredient(self, ingredient: NotionIngredient) -> str:
        """
        Synchronize an ingredient with Notion (Ingredientes DB).

        Args:
            ingredient: Ingredient to synchronize

        Returns:
            str: ID of the created/updated Notion page

        Raises:
            NotionAPIError: If synchronization fails
        """
        try:
            # Log the ingredient data being synced
            logger.info(f"Syncing ingredient: {ingredient.name}")
            logger.info(f"  Quantity: {ingredient.quantity}")
            logger.info(f"  Unit: {ingredient.unit}")
            logger.info(f"  Pantry ID: {ingredient.pantry_id}")
            logger.info(f"  Recipe ID: {ingredient.receta_id}")

            # Set title to just the quantity
            properties = {
                "Cantidad Usada": {
                    "title": [{
                        "text": {
                            "content": (
                                str(int(ingredient.quantity)) if ingredient.quantity is not None and float(ingredient.quantity).is_integer()
                                else str(ingredient.quantity) if ingredient.quantity is not None
                                else ""
                            )
                        }
                    }]
                },
                "Ingrediente": {"relation": [{"id": ingredient.pantry_id}]} if ingredient.pantry_id else None,
                "Unidad": {"rich_text": [{"text": {"content": ingredient.unit or ''}}]},
                "Receta": {"relation": [{"id": ingredient.receta_id}]} if ingredient.receta_id else None,
            }
            # Remove None values
            properties = {k: v for k, v in properties.items() if v is not None}

            # Log the properties being sent to Notion
            logger.info(f"Sending properties to Notion: {properties}")

            response = cast(
                Dict[str, Any],
                self.client.client.pages.create(
                    parent={"database_id": self.ingredient_db}, properties=properties
                ),
            )
            page_id = cast(str, response["id"])
            logger.info(f"Created ingredient page with ID: {page_id}")
            return page_id
        except Exception as e:
            logger.error(f"Failed to sync ingredient {ingredient.name}: {e}")
            raise NotionAPIError(f"Failed to sync ingredient {ingredient.name}: {e}")

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10), retry=retry_if_exception_type((NotionAPIError, ConnectionError)))
    def sync_pantry_item(self, pantry_item: NotionPantryItem) -> str:
        """
        Synchronize a pantry item with Notion (Alacena DB).

        Args:
            pantry_item: Pantry item to synchronize

        Returns:
            str: ID of the created/updated Notion page

        Raises:
            NotionAPIError: If synchronization fails
        """
        try:
            # Prepare properties for Notion (Alacena)
            properties = {
                "Nombre": {"title": [{"text": {"content": pantry_item.name}}]},
                "Categoría": {"select": {"name": pantry_item.category}} if pantry_item.category else None,
                "Stock alacena": {"number": pantry_item.stock} if pantry_item.stock is not None else None,
                "Unidad": {"select": {"name": pantry_item.unit}} if pantry_item.unit else None,
            }
            # Remove None values
            properties = {k: v for k, v in properties.items() if v is not None}
            response = cast(
                Dict[str, Any],
                self.client.client.pages.create(
                    parent={"database_id": self.pantry_db}, properties=properties
                ),
            )
            return cast(str, response["id"])
        except Exception as e:
            logger.error(f"Failed to sync pantry item {pantry_item.name}: {e}")
            raise NotionAPIError(f"Failed to sync pantry item {pantry_item.name}: {e}")

    def get_recipe(self, page_id: str) -> Dict[str, Any]:
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
            return cast(Dict[str, Any], self.client.client.pages.retrieve(page_id))
        except Exception as e:
            logger.error(f"Failed to get recipe {page_id}: {e}")
            raise NotionAPIError(f"Failed to get recipe {page_id}: {e}")

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
            NotionAPIError: If deletion fails
        """
        try:
            self.client.client.pages.update(page_id=page_id, archived=True)
        except Exception as e:
            logger.error(f"Failed to delete recipe {page_id}: {e}")
            raise NotionAPIError(f"Failed to delete recipe {page_id}: {e}")

    def update_ingredient_with_recipe(self, ingredient_id: str, recipe_id: str) -> None:
        """
        Update an ingredient page in Notion to set the Receta relation.
        """
        try:
            properties = {
                "📚 Recetas Completas": {"relation": [{"id": recipe_id}]}
            }
            self.client.client.pages.update(page_id=ingredient_id, properties=properties)
        except Exception as e:
            logger.error(f"Failed to update ingredient {ingredient_id} with recipe {recipe_id}: {e}")
            raise NotionAPIError(f"Failed to update ingredient {ingredient_id} with recipe {recipe_id}: {e}") 
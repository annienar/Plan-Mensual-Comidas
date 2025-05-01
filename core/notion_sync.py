"""Módulo para sincronización con Notion."""

from typing import Any, Dict, List, Optional, cast

from notion_client import Client


class NotionSync:
    """Clase para manejar la sincronización de recetas con Notion."""

    def __init__(self, token: str, database_id: str) -> None:
        """Inicializa el cliente de Notion.

        Args:
            token: Token de integración de Notion
            database_id: ID de la base de datos de recetas
        """
        self.token = token
        self.database_id = database_id
        self.client = Client(auth=token)
        self._test_page_ids: List[str] = []

    def check_connection(self) -> bool:
        """Verifica conexión con Notion API.

        Returns:
            bool: True si la conexión es exitosa, False en caso contrario
        """
        try:
            # Intenta obtener el usuario bot para verificar conexión
            self.client.users.me
            return True
        except Exception:
            return False

    def check_database(self) -> bool:
        """Verifica acceso a la base de datos.

        Returns:
            bool: True si se puede acceder a la base de datos, False en caso contrario
        """
        try:
            # Intenta obtener la base de datos
            self.client.databases.retrieve(self.database_id)
            return True
        except Exception:
            return False

    def _recipe_exists(self, recipe_name: str) -> Optional[str]:
        """Busca si una receta ya existe por nombre.

        Args:
            recipe_name: Nombre de la receta a buscar

        Returns:
            Optional[str]: ID de la página si existe, None si no existe
        """
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

    def sync_recipe(self, recipe: Dict[str, Any]) -> str:
        """Sincroniza una receta con Notion.

        Args:
            recipe: Diccionario con los datos de la receta

        Returns:
            str: ID de la página creada/actualizada en Notion

        Raises:
            Exception: Si hay error al sincronizar
        """
        # Verificar si la receta ya existe
        existing_id = self._recipe_exists(recipe["nombre"])

        # Preparar propiedades para Notion
        properties = {
            "Nombre": {"title": [{"text": {"content": recipe["nombre"]}}]},
            "Fuente": {
                "url": (
                    recipe["url_origen"]
                    if recipe["url_origen"] != "Desconocido"
                    else None
                )
            },
            "Porciones": {
                "number": (
                    recipe["porciones"]
                    if isinstance(recipe["porciones"], int)
                    else None
                )
            },
            "Ingredientes": {
                "rich_text": [{"text": {"content": recipe["ingredientes"]}}]
            },
            "Preparación": {
                "rich_text": [{"text": {"content": recipe["preparacion"]}}]
            },
        }

        if "calorias" in recipe and recipe["calorias"]:
            properties["Calorías"] = {"number": recipe["calorias"]}

        if existing_id:
            # Actualizar página existente
            response = cast(
                Dict[str, Any],
                self.client.pages.update(page_id=existing_id, properties=properties),
            )
        else:
            # Crear nueva página
            response = cast(
                Dict[str, Any],
                self.client.pages.create(
                    parent={"database_id": self.database_id}, properties=properties
                ),
            )

        return cast(str, response["id"])

    def get_recipe(self, page_id: str) -> Dict[str, Any]:
        """Obtiene una receta de Notion.

        Args:
            page_id: ID de la página de Notion

        Returns:
            Dict[str, Any]: Datos de la receta

        Raises:
            Exception: Si hay error al obtener la receta
        """
        return cast(Dict[str, Any], self.client.pages.retrieve(page_id))

    def sync_all_recipes(self, recipes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Sincroniza múltiples recetas.

        Args:
            recipes: Lista de recetas a sincronizar

        Returns:
            List[Dict[str, Any]]: Lista de resultados de sincronización
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
        """Elimina una receta de Notion.

        Args:
            page_id: ID de la página a eliminar

        Raises:
            Exception: Si hay error al eliminar la receta
        """
        self.client.pages.update(page_id=page_id, archived=True)

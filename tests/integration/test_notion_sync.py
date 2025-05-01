"""
Tests de integración para la sincronización con Notion.

Este módulo contiene tests que verifican la correcta sincronización
de recetas con la base de datos de Notion. Los tests cubren:

1. Conexión y autenticación con Notion
2. Sincronización individual de recetas
3. Sincronización masiva de recetas
4. Manejo de duplicados y actualizaciones
5. Validación de datos sincronizados

Requisitos:
    - Credenciales válidas de Notion en variables de entorno:
        - NOTION_TOKEN: Token de integración de Notion
        - NOTION_DATABASE_ID: ID de la base de datos de recetas
    - Base de datos de Notion con la estructura correcta:
        - Nombre (title)
        - Fuente (url)
        - Porciones (number)
        - Ingredientes (rich_text)
        - Preparación (rich_text)
        - Calorías (number, opcional)
    - Archivos de receta en el directorio sin_procesar/

Uso:
    # Ejecutar todos los tests de Notion
    pytest tests/integration/test_notion_sync.py

    # Ejecutar tests específicos
    pytest tests/integration/test_notion_sync.py::test_notion_conexion
    pytest tests/integration/test_notion_sync.py::test_sync_receta_individual

    # Ejecutar con marcadores
    pytest -m notion
"""

import os
from typing import Generator

import pytest
from pytest import FixtureRequest

from core.config import DIR_SIN_PROCESAR
from core.gestor import GestorRecetas
from core.notion_sync import NotionSync

# Skip all tests if no Notion credentials
pytestmark = [
    pytest.mark.skipif(
        not os.getenv("NOTION_TOKEN") or not os.getenv("NOTION_DATABASE_ID"),
        reason="Notion credentials not found in environment",
    ),
    pytest.mark.notion,  # Marcar todos los tests como tests de Notion
    pytest.mark.integration,  # Marcar como tests de integración
]


@pytest.fixture
def notion_sync(request: FixtureRequest) -> Generator[NotionSync, None, None]:
    """
    Fixture para crear instancia de NotionSync con credenciales de test.

    Args:
        request: Objeto request de pytest para acceder al contexto del test

    Yields:
        NotionSync: Instancia configurada para tests

    Requires:
        Variables de entorno NOTION_TOKEN y NOTION_DATABASE_ID
    """
    token = os.environ["NOTION_TOKEN"]  # Will raise if not set
    database_id = os.environ["NOTION_DATABASE_ID"]  # Will raise if not set
    sync = NotionSync(token, database_id)

    # Guardar IDs de páginas creadas para limpiarlas después
    sync._test_page_ids = []
    yield sync

    # Limpiar páginas creadas durante los tests
    for page_id in sync._test_page_ids:
        try:
            sync.delete_recipe(page_id)
        except Exception:
            pass


@pytest.fixture
def gestor() -> GestorRecetas:
    """
    Fixture para crear instancia de GestorRecetas.

    Returns:
        GestorRecetas: Instancia limpia para cada test
    """
    return GestorRecetas()


def test_notion_conexion(notion_sync: NotionSync) -> None:
    """
    Verifica que podemos conectar con Notion API.

    Este test es fundamental y debe ejecutarse primero, ya que
    los demás tests dependen de una conexión exitosa.

    Args:
        notion_sync: Fixture de NotionSync

    Raises:
        AssertionError: Si no se puede establecer conexión
    """
    assert notion_sync.check_connection(), "No se pudo conectar con Notion API"


def test_notion_database_exists(notion_sync: NotionSync) -> None:
    """
    Verifica que la base de datos existe y es accesible.

    Confirma que:
    1. La base de datos existe
    2. Tenemos permisos para accederla
    3. Tiene la estructura correcta

    Args:
        notion_sync: Fixture de NotionSync

    Raises:
        AssertionError: Si no se puede acceder a la base de datos
    """
    assert (
        notion_sync.check_database()
    ), "No se pudo acceder a la base de datos de Notion"


def test_sync_receta_individual(notion_sync: NotionSync, gestor: GestorRecetas) -> None:
    """
    Verifica la sincronización de una receta individual.

    Proceso:
    1. Procesa una receta desde archivo
    2. La sincroniza con Notion
    3. Verifica que se creó correctamente
    4. Valida todos los campos sincronizados

    Args:
        notion_sync: Fixture de NotionSync
        gestor: Fixture de GestorRecetas

    Raises:
        AssertionError: Si la sincronización falla o los datos no coinciden
        FileNotFoundError: Si no hay archivos de receta disponibles
    """
    # Verificar que existen archivos de receta
    archivos = list(DIR_SIN_PROCESAR.glob("*.txt"))
    if not archivos:
        pytest.fail("No se encontraron archivos de receta para procesar")

    # Procesar y sincronizar la primera receta
    receta = gestor.procesar_receta(archivos[0])
    page_id = notion_sync.sync_recipe(receta)
    assert page_id, f"No se pudo sincronizar la receta {receta['nombre']}"
    notion_sync._test_page_ids.append(page_id)

    # Verificar que la receta existe en Notion
    page = notion_sync.get_recipe(page_id)
    assert page, f"No se pudo recuperar la receta {receta['nombre']} de Notion"

    # Verificar campos
    assert (
        page["properties"]["Nombre"]["title"][0]["text"]["content"] == receta["nombre"]
    )
    if receta["url_origen"] != "Desconocido":
        assert page["properties"]["Fuente"]["url"] == receta["url_origen"]
    if isinstance(receta["porciones"], int):
        assert page["properties"]["Porciones"]["number"] == receta["porciones"]


@pytest.mark.slow
def test_sync_todas_recetas(notion_sync: NotionSync, gestor: GestorRecetas) -> None:
    """
    Verifica la sincronización de todas las recetas.

    Este test puede ser lento ya que procesa y sincroniza
    todas las recetas encontradas. Usa el marcador 'slow'.

    Args:
        notion_sync: Fixture de NotionSync
        gestor: Fixture de GestorRecetas

    Raises:
        AssertionError: Si alguna receta falla al sincronizar
        FileNotFoundError: Si no hay archivos de receta disponibles
    """
    # Procesar todas las recetas
    recetas = gestor.procesar_todas_recetas()
    if not recetas:
        pytest.fail("No se encontraron recetas para procesar")

    # Sincronizar con Notion
    resultados = notion_sync.sync_all_recipes(recetas)
    assert len(resultados) == len(recetas), "No todas las recetas se sincronizaron"

    # Verificar que todas se sincronizaron correctamente
    for receta, resultado in zip(recetas, resultados):
        assert resultado[
            "success"
        ], f"Error sincronizando {receta['nombre']}: {resultado['error']}"
        assert resultado["page_id"], f"No se obtuvo page_id para {receta['nombre']}"
        notion_sync._test_page_ids.append(resultado["page_id"])


def test_manejo_duplicados(notion_sync: NotionSync, gestor: GestorRecetas) -> None:
    """
    Verifica el manejo de recetas duplicadas.

    Confirma que:
    1. No se crean duplicados al sincronizar la misma receta
    2. Se actualiza la existente en lugar de crear nueva

    Args:
        notion_sync: Fixture de NotionSync
        gestor: Fixture de GestorRecetas

    Raises:
        AssertionError: Si se crea un duplicado
        FileNotFoundError: Si no hay archivos de receta disponibles
    """
    # Verificar que existen archivos de receta
    archivos = list(DIR_SIN_PROCESAR.glob("*.txt"))
    if not archivos:
        pytest.fail("No se encontraron archivos de receta para procesar")

    # Procesar y sincronizar una receta
    receta = gestor.procesar_receta(archivos[0])

    # Intentar sincronizar la misma receta dos veces
    page_id1 = notion_sync.sync_recipe(receta)
    notion_sync._test_page_ids.append(page_id1)
    page_id2 = notion_sync.sync_recipe(receta)

    # Verificar que no se creó un duplicado
    assert page_id1 == page_id2, "Se creó un duplicado de la receta"


def test_actualizacion_receta(notion_sync: NotionSync, gestor: GestorRecetas) -> None:
    """
    Verifica la actualización de recetas existentes.

    Proceso:
    1. Sincroniza una receta
    2. Modifica algunos campos
    3. Vuelve a sincronizar
    4. Verifica que se actualizó la existente

    Args:
        notion_sync: Fixture de NotionSync
        gestor: Fixture de GestorRecetas

    Raises:
        AssertionError: Si la actualización falla o crea duplicado
        FileNotFoundError: Si no hay archivos de receta disponibles
    """
    # Verificar que existen archivos de receta
    archivos = list(DIR_SIN_PROCESAR.glob("*.txt"))
    if not archivos:
        pytest.fail("No se encontraron archivos de receta para procesar")

    # Procesar y sincronizar una receta
    receta = gestor.procesar_receta(archivos[0])
    page_id = notion_sync.sync_recipe(receta)
    notion_sync._test_page_ids.append(page_id)

    # Modificar la receta
    receta["porciones"] = 4 if receta["porciones"] != 4 else 6

    # Sincronizar la versión modificada
    new_page_id = notion_sync.sync_recipe(receta)

    # Verificar que se actualizó la existente
    assert new_page_id == page_id, "Se creó una nueva receta en lugar de actualizar"
    page = notion_sync.get_recipe(page_id)
    assert page["properties"]["Porciones"]["number"] == receta["porciones"]

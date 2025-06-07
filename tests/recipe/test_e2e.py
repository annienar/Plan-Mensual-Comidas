"""
End - to - end tests for recipe processing pipeline.
"""

from core.domain.recipe.models import Recipe, Ingredient
from core.application.recipe.processor import RecipeProcessor
from core.infrastructure.llm.client import LLMClient, InvalidResponseError
from core.infrastructure.notion.client import NotionClient
from core.infrastructure.notion.errors import NotionAPIError
from core.infrastructure.notion.sync import NotionSync
from core.utils.logger import get_logger
from datetime import datetime
import os

import asyncio
import pytest
import pytest_asyncio
import time
os.environ["NOTION_API_KEY"] = "test_notion_api_key"
os.environ["NOTION_DATABASE_ID"] = "test_database_id"
os.environ["NOTION_RECIPES_DB_ID"] = "test_recipes_db_id"
os.environ["NOTION_INGREDIENTS_DB_ID"] = "test_ingredients_db_id"
os.environ["NOTION_PANTRY_DB_ID"] = "test_pantry_db_id"

logger = get_logger("test_e2e")

# Test constants
TEST_TIMEOUT = 30  # seconds
PERFORMANCE_THRESHOLD = 10.0  # seconds

@pytest_asyncio.fixture
async def llm_client():
    """Create a test LLM client."""
    client = LLMClient()
    return client

@pytest_asyncio.fixture
async def recipe_processor(llm_client):
    """Create a test recipe processor."""
    processor = RecipeProcessor(llm_client)
    return processor

@pytest_asyncio.fixture
async def notion_sync():
    """Create a test Notion sync instance."""
    client = NotionClient()
    return NotionSync(
        client = client, 
        recipes_db_id = os.getenv("NOTION_RECIPES_DB_ID"), 
        ingredients_db_id = os.getenv("NOTION_INGREDIENTS_DB_ID"), 
        pantry_db_id = os.getenv("NOTION_PANTRY_DB_ID")
)

@pytest.mark.asyncio
async def test_full_recipe_processing(recipe_processor, notion_sync):
    """Test the complete recipe processing pipeline."""
    try:
        async with asyncio.timeout(TEST_TIMEOUT):
            # Test recipe
            recipe_text = """
            Receta: Pollo al Curry
            Porciones: 4
            Tiempo Total: 45 minutos

            Ingredientes:
            - 500g de pollo
            - 2 cebollas
            - 2 dientes de ajo
            - 2 cucharadas de curry en polvo
            - 400ml de leche de coco
            - Sal y pimienta al gusto

            Instrucciones:
            1. Cortar el pollo en trozos
            2. Picar la cebolla y el ajo
            3. Dorar el pollo en una sartén
            4. Añadir la cebolla y el ajo
            5. Agregar el curry y la leche de coco
            6. Cocinar a fuego lento por 20 minutos
            7. Ajustar la sazón
            """

            # Process recipe
            recipe = await recipe_processor.process_recipe(recipe_text)

            # Verify recipe structure
            assert recipe is not None
            assert recipe.title == "Pollo al Curry"
            assert recipe.metadata.porciones == 4
            assert recipe.metadata.tiempo_total == 45
            assert len(recipe.ingredients) > 0
            assert len(recipe.instructions) > 0

            # Verify ingredients (using Spanish field names)
            for ingredient in recipe.ingredients:
                assert ingredient.nombre
                assert ingredient.cantidad > 0
                assert ingredient.unidad

            # Verify instructions
            for instruction in recipe.instructions:
                assert instruction

            # Sync to Notion
            recipe_page = await notion_sync.sync_recipe(recipe)

            # Verify Notion page
            assert recipe_page is not None
            assert recipe_page["properties"]["Nombre"]["title"][0]["text"]["content"] == recipe.title
            assert recipe_page["properties"]["Porciones"]["number"] == recipe.metadata.porciones
            assert recipe_page["properties"]["Tiempo Total"]["number"] == recipe.metadata.tiempo_total

    except asyncio.TimeoutError:
        pytest.fail("Test timed out after 30 seconds")

@pytest.mark.asyncio
async def test_recipe_processing_with_errors(recipe_processor):
    """Test recipe processing with error handling."""
    # Test with invalid input
    with pytest.raises(InvalidResponseError):
        await recipe_processor.process_recipe("Invalid recipe text")

    # Test with missing required fields
    with pytest.raises(InvalidResponseError):
        await recipe_processor.process_recipe("Receta: Test\nPorciones: 4")

    # Test with invalid numeric fields
    with pytest.raises(InvalidResponseError):
        await recipe_processor.process_recipe("Receta: Test\nPorciones: invalid")

@pytest.mark.asyncio
async def test_recipe_processing_performance(recipe_processor):
    """Test recipe processing performance."""
    try:
        async with asyncio.timeout(TEST_TIMEOUT):
            start_time = time.time()

            # Test recipe
            recipe_text = """
            Receta: Pollo al Curry
            Porciones: 4
            Tiempo Total: 45 minutos

            Ingredientes:
            - 500g de pollo
            - 2 cebollas
            - 2 dientes de ajo
            - 2 cucharadas de curry en polvo
            - 400ml de leche de coco
            - Sal y pimienta al gusto

            Instrucciones:
            1. Cortar el pollo en trozos
            2. Picar la cebolla y el ajo
            3. Dorar el pollo en una sartén
            4. Añadir la cebolla y el ajo
            5. Agregar el curry y la leche de coco
            6. Cocinar a fuego lento por 20 minutos
            7. Ajustar la sazón
            """

            # Process recipe
            recipe = await recipe_processor.process_recipe(recipe_text)

            # Verify performance
            processing_time = time.time() - start_time
            assert processing_time < PERFORMANCE_THRESHOLD, f"Recipe processing took {processing_time:.2f} seconds, exceeding {PERFORMANCE_THRESHOLD} second threshold"

            # Verify recipe structure
            assert recipe is not None
            assert recipe.title == "Pollo al Curry"
            assert recipe.metadata.porciones == 4
            assert recipe.metadata.tiempo_total == 45
            assert len(recipe.ingredients) > 0
            assert len(recipe.instructions) > 0

    except asyncio.TimeoutError:
        pytest.fail("Test timed out after 30 seconds")

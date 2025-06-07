"""
Integration tests using real LLM service and Notion API for recipe processing.
These tests should be run separately from the main test suite due to:
1. API costs
2. Network dependencies
3. Longer execution time
"""

from core.domain.recipe.models.ingredient import Ingredient
from core.domain.recipe.models.metadata import RecipeMetadata
from core.domain.recipe.models.recipe import Recipe
from core.application.recipe.processor import RecipeProcessor
from core.infrastructure.llm.client import LLMClient, InvalidResponseError
from core.infrastructure.notion.client import NotionClient
from core.infrastructure.notion.models import NotionRecipe, NotionIngredient, NotionPantryItem
from core.infrastructure.notion.sync import NotionSync
from core.utils.logger import get_logger, log_test_result
from datetime import datetime
from pathlib import Path
import os

from unittest.mock import patch, MagicMock
import asyncio
import pytest
import pytest_asyncio
import time
import json
import tempfile

logger = get_logger("test_integration")

# Mark all tests in this module as integration tests
pytestmark = pytest.mark.asyncio

# Test configuration
TEST_TIMEOUT = 120  # 2 minutes timeout for tests
PERFORMANCE_THRESHOLD = 120  # 2 minutes threshold for performance tests

# Test environment setup
os.environ["NOTION_API_KEY"] = "test_notion_api_key"
os.environ["NOTION_DATABASE_ID"] = "test_database_id"
os.environ["NOTION_RECIPES_DB_ID"] = "test_recipes_db_id"
os.environ["NOTION_INGREDIENTS_DB_ID"] = "test_ingredients_db_id"
os.environ["NOTION_PANTRY_DB_ID"] = "test_pantry_db_id"

@pytest_asyncio.fixture
async def event_loop():
    """Create an event loop for the test."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="function")
async def llm_client():
    """Create a test LLM client."""
    client = LLMClient()
    return client

@pytest_asyncio.fixture(scope="function")
async def recipe_processor(llm_client):
    """Create a test recipe processor."""
    processor = RecipeProcessor(llm_client)
    return processor

@pytest_asyncio.fixture(scope="function")
async def notion_sync():
    """Create a test Notion sync instance."""
    client = NotionClient()
    return NotionSync(
        client = client, 
        recipes_db_id = os.getenv("NOTION_RECIPES_DB_ID"), 
        ingredients_db_id = os.getenv("NOTION_INGREDIENTS_DB_ID"), 
        pantry_db_id = os.getenv("NOTION_PANTRY_DB_ID")
)

@pytest.fixture
def cleanup_notion():
    """Create a list to track Notion pages for cleanup."""
    return []

# Sample recipes that can be reused
SAMPLE_RECIPES = [
    """Receta: Pollo al Curry
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
    7. Ajustar la sazón"""
]

@pytest_asyncio.fixture(scope="session")
def sample_recipes():
    """Provide sample recipes for testing."""
    return SAMPLE_RECIPES

@pytest.mark.asyncio
async def test_llm_recipe_extraction(recipe_processor, sample_recipes):
    """Test recipe extraction using LLM."""
    try:
        async with asyncio.timeout(TEST_TIMEOUT):
            # Process recipe
            recipe = await recipe_processor.process_recipe(sample_recipes[0])

            # Verify recipe structure
            assert recipe is not None
            assert recipe.title == "Pollo al Curry"
            assert recipe.servings == 4
            assert recipe.prep_time + recipe.cook_time == 45
            assert len(recipe.ingredients) > 0
            assert len(recipe.instructions) > 0

            # Verify ingredients
            for ingredient in recipe.ingredients:
                assert ingredient.nombre
                assert ingredient.cantidad > 0
                assert ingredient.unidad

            # Verify instructions
            for instruction in recipe.instructions:
                assert instruction
    except asyncio.TimeoutError:
        pytest.fail("Test timed out after 30 seconds")

@pytest.mark.asyncio
async def test_llm_error_handling(recipe_processor):
    """Test LLM error handling."""
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
async def test_llm_performance(recipe_processor, sample_recipes):
    """Test LLM performance."""
    try:
        async with asyncio.timeout(TEST_TIMEOUT):
            start_time = time.time()

            # Process recipe
            recipe = await recipe_processor.process_recipe(sample_recipes[0])

            # Verify performance
            processing_time = time.time() - start_time
            assert processing_time < 10.0  # Should process within 10 seconds

            # Verify recipe structure
            assert recipe is not None
            assert recipe.title == "Pollo al Curry"
            assert recipe.servings == 4
            assert len(recipe.ingredients) > 0
            assert len(recipe.instructions) > 0
    except asyncio.TimeoutError:
        pytest.fail("Test timed out after 30 seconds")

# Notion Integration Tests
@pytest.mark.asyncio
async def test_notion_recipe_sync(recipe_processor, notion_sync, sample_recipes, cleanup_notion):
    """Test syncing recipes to Notion."""
    try:
        async with asyncio.timeout(TEST_TIMEOUT):
            # Process recipe
            recipe = await recipe_processor.process_recipe(sample_recipes[0])
            assert recipe is not None

            # Sync recipe
            recipe_page = await notion_sync.sync_recipe(recipe)
            cleanup_notion.append(recipe_page)

            # Verify recipe page
            assert recipe_page is not None
            assert recipe_page["properties"]["Nombre"]["title"][0]["text"]["content"] == recipe.title
            assert recipe_page["properties"]["Porciones"]["number"] == recipe.servings
            assert recipe_page["properties"]["Tiempo Total"]["number"] == recipe.prep_time + recipe.cook_time
    except asyncio.TimeoutError:
        pytest.fail("Test timed out after 30 seconds")

@pytest.mark.asyncio
async def test_notion_ingredients_sync(recipe_processor, notion_sync, sample_recipes, cleanup_notion):
    """Test syncing ingredients to Notion."""
    try:
        async with asyncio.timeout(TEST_TIMEOUT):
            # Process recipe
            recipe = await recipe_processor.process_recipe(sample_recipes[0])
            assert recipe is not None

            # Sync recipe first to get recipe_id
            recipe_page = await notion_sync.sync_recipe(recipe)
            cleanup_notion.append(recipe_page)

            # Sync ingredients
            ingredient_pages = []
            for ing_data in recipe.ingredients:
                ingredient = NotionIngredient(
                    name = ing_data.nombre, 
                    cantidad = ing_data.cantidad, 
                    unit = ing_data.unidad, 
                    receta_id = recipe_page["id"]
)
                ingredient_page = await notion_sync.sync_ingredient(ingredient)
                ingredient_pages.append(ingredient_page)
                cleanup_notion.append(ingredient_page)

            # Verify ingredient pages
            assert len(ingredient_pages) == len(recipe.ingredients)
            for page, ing in zip(ingredient_pages, recipe.ingredients):
                assert page["properties"]["Nombre"]["title"][0]["text"]["content"] == ing.nombre
                assert page["properties"]["Cantidad Usada"]["number"] == ing.cantidad
                assert page["properties"]["Unidad"]["rich_text"][0]["text"]["content"] == ing.unidad
    except asyncio.TimeoutError:
        pytest.fail("Test timed out after 30 seconds")

@pytest.mark.asyncio
async def test_notion_pantry_sync(recipe_processor, notion_sync, sample_recipes, cleanup_notion):
    """Test syncing pantry items to Notion."""
    try:
        async with asyncio.timeout(TEST_TIMEOUT):
            # Process recipe
            recipe = await recipe_processor.process_recipe(sample_recipes[0])
            assert recipe is not None

            # Sync recipe first to get recipe_id
            recipe_page = await notion_sync.sync_recipe(recipe)
            cleanup_notion.append(recipe_page)

            # Sync pantry items
            pantry_pages = []
            for ing_data in recipe.ingredients:
                pantry_item = NotionPantryItem(
                    name = ing_data.nombre, 
                    unit = ing_data.unidad, 
                    stock = 0.0  # Initialize with 0 stock
)
                pantry_page = await notion_sync.sync_pantry_item(pantry_item)
                pantry_pages.append(pantry_page)
                cleanup_notion.append(pantry_page)

            # Verify pantry pages
            assert len(pantry_pages) == len(recipe.ingredients)
            for page, ing in zip(pantry_pages, recipe.ingredients):
                assert page["properties"]["Nombre"]["title"][0]["text"]["content"] == ing.nombre
                assert page["properties"]["Unidad"]["rich_text"][0]["text"]["content"] == ing.unidad
                assert page["properties"]["Stock"]["number"] == 0.0
    except asyncio.TimeoutError:
        pytest.fail("Test timed out after 30 seconds")

@pytest.mark.asyncio
async def test_notion_error_handling(notion_sync):
    """Test Notion error handling."""
    # Test with invalid data
    invalid_recipe = Recipe(
        name="Invalid Recipe", 
        servings=-1, 
        prep_time=-1, 
        cook_time=-1, 
        calories=-1, 
        protein=-1, 
        carbs=-1, 
        fat=-1, 
        ingredients=[], 
        instructions=[]
)

    with pytest.raises(NotionAPIError) as exc_info:
        await notion_sync.sync_recipe(invalid_recipe)
    assert "Failed to sync recipe" in str(exc_info.value)

def teardown_module(module):
    """Clean up after all tests."""
    # Close the event loop
    loop = asyncio.get_event_loop()
    if loop.is_running():
        loop.stop()
    if not loop.is_closed():
        loop.close()

    # Close the HTTP client
    if hasattr(module, 'http_client'):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(module.http_client.close())
        loop.close()

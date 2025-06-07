"""
Tests for CLI functionality.
"""

import pytest
from commands.cli import validate_env_vars, process_single_recipe, cli
from pathlib import Path
from unittest.mock import patch, MagicMock
from core.application.recipe.processor import RecipeProcessor
from core.domain.recipe.models.ingredient import Ingredient
from core.domain.recipe.models.metadata import RecipeMetadata
from core.domain.recipe.models.recipe import Recipe
from core.infrastructure.notion.sync import NotionSync
import os

from unittest.mock import patch, MagicMock, AsyncMock

@pytest.fixture(autouse = True)

def setup_env():
    """Set up test environment variables."""
    os.environ["NOTION_TOKEN"] = "test_token"
    os.environ["NOTION_RECETAS_DB"] = "test_recipes_db"
    os.environ["NOTION_INGREDIENTES_DB"] = "test_ingredients_db"
    os.environ["NOTION_ALACENA_DB"] = "test_pantry_db"
    yield
    # Cleanup
    for var in ["NOTION_TOKEN", "NOTION_RECETAS_DB", "NOTION_INGREDIENTES_DB", "NOTION_ALACENA_DB"]:
        os.environ.pop(var, None)

@pytest.fixture

def test_recipe():
    """Create a test recipe."""
    return Recipe(
        title="Test Recipe",
        metadata = RecipeMetadata(
            title="Test Recipe", 
            porciones = 4, 
            calorias = 500, 
            tags=["test", "dinner"], 
            tipo="main", 
            hecho = False, 
            date="2024-03-20", 
            dificultad="medium", 
            tiempo_preparacion = 30, 
            tiempo_coccion = 45, 
            tiempo_total = 75, 
            notas="Test notes", 
            url="https://example.com/recipe"
), 
        ingredients=[
            Ingredient(nombre="flour", cantidad = 2, unidad="cups"), 
            Ingredient(nombre="sugar", cantidad = 1, unidad="cup")
        ], 
        instructions=[
            "Mix ingredients thoroughly", 
            "Bake at 350F for 25 minutes"
        ]
)

def test_validate_env_vars():
    """Test environment variable validation."""
    # Test with all variables set
    result = validate_env_vars()
    assert result["Recetas"] == "test_recipes_db"
    assert result["Ingredientes"] == "test_ingredients_db"
    assert result["Alacena"] == "test_pantry_db"

    # Test with missing variables
    os.environ.pop("NOTION_TOKEN")
    with pytest.raises(Exception) as exc_info:
        validate_env_vars()
    assert "Missing required environment variables" in str(exc_info.value)

@pytest.mark.asyncio
async def test_process_single_recipe(test_recipe):
    """Test processing a single recipe."""
    # Mock dependencies
    mock_notion_sync = AsyncMock(spec = NotionSync)
    mock_processor = AsyncMock(spec = RecipeProcessor)
    mock_progress_bar = MagicMock()

    # Mock recipe processing (async method)
    mock_processor.process_recipe = AsyncMock(return_value=test_recipe)

    # Mock Notion sync operations
    mock_notion_sync.sync_pantry_item.return_value = "test_pantry_id"
    mock_notion_sync.sync_ingredient.return_value = "test_ingredient_id"
    mock_notion_sync.sync_recipe.return_value = "test_recipe_id"

    # Create test file
    test_file = Path("test_recipe.txt")
    test_file.write_text("Test recipe content")

    try:
        # Process recipe
        result = await process_single_recipe(
            test_file, 
            mock_notion_sync, 
            mock_processor, 
            mock_progress_bar
)

        # Verify result
        assert result is True

        # Verify calls
        mock_processor.process_recipe.assert_called_once()
        assert mock_notion_sync.sync_pantry_item.call_count == 2  # One for each ingredient
        assert mock_notion_sync.sync_ingredient.call_count == 2
        mock_notion_sync.sync_recipe.assert_called_once()
        assert mock_notion_sync.update_ingredient_with_recipe.call_count == 2

    finally:
        # Cleanup
        if test_file.exists():
            test_file.unlink()

@pytest.mark.asyncio
async def test_process_single_recipe_error(test_recipe):
    """Test error handling in recipe processing."""
    # Mock dependencies
    mock_notion_sync = AsyncMock(spec = NotionSync)
    mock_processor = AsyncMock(spec = RecipeProcessor)
    mock_progress_bar = MagicMock()

    # Mock error
    mock_processor.process_recipe.side_effect = Exception("Test error")

    # Create test file
    test_file = Path("test_recipe.txt")
    test_file.write_text("Test recipe content")

    try:
        # Process recipe
        result = await process_single_recipe(
            test_file, 
            mock_notion_sync, 
            mock_processor, 
            mock_progress_bar
)

        # Verify result
        assert result is False

        # Verify error handling
        mock_progress_bar.update.assert_called_with(1, "ERROR: test_recipe.txt failed: Test error")

    finally:
        # Cleanup
        if test_file.exists():
            test_file.unlink()

def test_cli_commands():
    """Test CLI commands."""
    # Test list_recipes command
    with patch('click.echo') as mock_echo:
        with patch('pathlib.Path.glob') as mock_glob:
            mock_glob.return_value = [Path("test1.txt"), Path("test2.txt")]
            cli.commands['list_recipes'].callback()
            assert mock_echo.call_count > 0

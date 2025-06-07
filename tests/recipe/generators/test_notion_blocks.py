"""
Tests for the Notion blocks generator module.
"""

from core.domain.recipe.generators.notion_blocks import recipe_to_notion_blocks
from core.domain.recipe.models.ingredient import Ingredient
from core.domain.recipe.models.metadata import RecipeMetadata
from core.domain.recipe.models.recipe import Recipe

import pytest
@pytest.fixture

def test_recipe():
    """Create a test recipe."""
    return Recipe(
        metadata = RecipeMetadata(
            title="Test Recipe", 
            porciones = 4, 
            calorias = 500, 
            tags=["test", "dinner"], 
            tipo="main", 
            hecho = False, 
            date="2024 - 03 - 20", 
            dificultad="medium", 
            tiempo_preparacion = 30, 
            tiempo_coccion = 45, 
            tiempo_total = 75, 
            notas="Test note 1\nTest note 2"
), 
        ingredients=[
            Ingredient(nombre="flour", cantidad = 2, unidad="cups"), 
            Ingredient(nombre="sugar", cantidad = 1, unidad="cup"), 
            Ingredient(nombre="salt", cantidad = 0.5, unidad="teaspoon", notes="optional")
        ], 
        instructions=[
            "Mix dry ingredients", 
            "Add wet ingredients", 
            "Bake at 350F"
        ]
)

def test_recipe_to_notion_blocks_basic(test_recipe):
    """Test basic Notion blocks generation."""
    blocks = recipe_to_notion_blocks(test_recipe)

    # Verify title block
    assert blocks[0]["type"] == "heading_1"
    assert blocks[0]["heading_1"]["rich_text"][0]["text"]["content"] == test_recipe.title

    # Verify metadata block
    assert blocks[1]["type"] == "paragraph"
    metadata_text = blocks[1]["paragraph"]["rich_text"][0]["text"]["content"]
    assert "🍽 Porciones: 4" in metadata_text
    assert "⏱ Prep: 30" in metadata_text
    assert "🔥 Cocción: 45" in metadata_text
    assert "⏰ Total: 75" in metadata_text
    assert "📊 Dificultad: medium" in metadata_text
    assert "⚡ Calorías: 500" in metadata_text

    # Verify ingredients section
    assert blocks[2]["type"] == "heading_2"
    assert blocks[2]["heading_2"]["rich_text"][0]["text"]["content"] == "🧾 Ingredientes"

    # Verify ingredients list
    assert blocks[3]["type"] == "bulleted_list_item"
    assert "2 cups flour" in blocks[3]["bulleted_list_item"]["rich_text"][0]["text"]["content"]
    assert blocks[4]["type"] == "bulleted_list_item"
    assert "1 cup sugar" in blocks[4]["bulleted_list_item"]["rich_text"][0]["text"]["content"]
    assert blocks[5]["type"] == "bulleted_list_item"
    assert "0.5 teaspoon salt" in blocks[5]["bulleted_list_item"]["rich_text"][0]["text"]["content"]

    # Verify instructions section
    assert blocks[6]["type"] == "heading_2"
    assert blocks[6]["heading_2"]["rich_text"][0]["text"]["content"] == "🔪 Preparación"

    # Verify instructions list
    assert blocks[7]["type"] == "numbered_list_item"
    assert blocks[7]["numbered_list_item"]["rich_text"][0]["text"]["content"] == "Mix dry ingredients"
    assert blocks[8]["type"] == "numbered_list_item"
    assert blocks[8]["numbered_list_item"]["rich_text"][0]["text"]["content"] == "Add wet ingredients"
    assert blocks[9]["type"] == "numbered_list_item"
    assert blocks[9]["numbered_list_item"]["rich_text"][0]["text"]["content"] == "Bake at 350F"

    # Verify notes section
    assert blocks[10]["type"] == "heading_2"
    assert blocks[10]["heading_2"]["rich_text"][0]["text"]["content"] == "📝 Notas"
    assert blocks[11]["type"] == "paragraph"
    assert blocks[11]["paragraph"]["rich_text"][0]["text"]["content"] == "Test note 1"
    assert blocks[12]["type"] == "paragraph"
    assert blocks[12]["paragraph"]["rich_text"][0]["text"]["content"] == "Test note 2"

def test_recipe_to_notion_blocks_minimal():
    """Test Notion blocks generation with minimal recipe."""
    recipe = Recipe(
        metadata = RecipeMetadata(
            title="Minimal Recipe"
), 
        ingredients=[], 
        instructions=[]
)

    blocks = recipe_to_notion_blocks(recipe)

    # Verify only title block is present
    assert len(blocks) == 1
    assert blocks[0]["type"] == "heading_1"
    assert blocks[0]["heading_1"]["rich_text"][0]["text"]["content"] == "Minimal Recipe"

def test_recipe_to_notion_blocks_no_metadata():
    """Test Notion blocks generation without metadata."""
    recipe = Recipe(
        metadata = RecipeMetadata(
            title="No Metadata Recipe"
), 
        ingredients=[
            Ingredient(nombre="flour", cantidad = 1, unidad="cup")
        ], 
        instructions=["Test step"]
)

    blocks = recipe_to_notion_blocks(recipe)

    # Verify no metadata block
    assert blocks[0]["type"] == "heading_1"
    assert blocks[1]["type"] == "heading_2"  # Ingredients section
    assert " | " not in blocks[1]["heading_2"]["rich_text"][0]["text"]["content"]

def test_recipe_to_notion_blocks_no_notes():
    """Test Notion blocks generation without notes."""
    recipe = Recipe(
        metadata = RecipeMetadata(
            title="No Notes Recipe"
), 
        ingredients=[
            Ingredient(nombre="flour", cantidad = 1, unidad="cup")
        ], 
        instructions=["Test step"]
)

    blocks = recipe_to_notion_blocks(recipe)

    # Verify no notes section
    assert blocks[-1]["type"] == "numbered_list_item"  # Last block should be an instruction
    assert "📝 Notas" not in [block["heading_2"]["rich_text"][0]["text"]["content"]
                            for block in blocks
                            if block["type"] == "heading_2"]

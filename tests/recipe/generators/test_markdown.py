"""
Tests for the markdown generator module.
"""

from core.domain.recipe.generators.markdown import format_ingredient, generate_markdown, generate_all_markdown
from core.domain.recipe.models.ingredient import Ingredient
from core.domain.recipe.models.metadata import RecipeMetadata
from core.domain.recipe.models.recipe import Recipe
from pathlib import Path

import pytest
@pytest.fixture

def test_recipe():
    """Create a test recipe."""
    return Recipe(
        metadata = RecipeMetadata(
            title="Test Recipe", 
            url="https://example.com / recipe", 
            porciones = 4, 
            calorias = 500, 
            tipo="main", 
            tags=["test", "dinner"], 
            hecho = False, 
            date="2024 - 03 - 20", 
            dificultad="medium", 
            tiempo_preparacion = 30, 
            tiempo_coccion = 45, 
            tiempo_total = 75, 
            notas="Test notes"
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

def test_format_ingredient():
    """Test ingredient formatting."""
    # Test with quantity and unit
    ingredient = {"cantidad": 2, "unidad": "tazas", "nombre": "flour"}
    assert format_ingredient(ingredient) == "- 2 tazas de flour"

    # Test with singular unit
    ingredient = {"cantidad": 1, "unidad": "tazas", "nombre": "flour"}
    assert format_ingredient(ingredient) == "- 1 taza de flour"

    # Test with fraction
    ingredient = {"cantidad": 0.5, "unidad": "cucharadas", "nombre": "salt"}
    assert format_ingredient(ingredient) == "- 1 / 2 cucharada de salt"

    # Test with mixed fraction
    ingredient = {"cantidad": 1.5, "unidad": "tazas", "nombre": "sugar"}
    assert format_ingredient(ingredient) == "- 1 1 / 2 tazas de sugar"

    # Test without quantity
    ingredient = {"cantidad": 0, "unidad": "", "nombre": "salt to taste"}
    assert format_ingredient(ingredient) == "- salt to taste"

    # Test without unit
    ingredient = {"cantidad": 2, "unidad": "", "nombre": "eggs"}
    assert format_ingredient(ingredient) == "- 2 eggs"

def test_generate_markdown(test_recipe, tmp_path):
    """Test markdown file generation."""
    output_path = tmp_path / "test_recipe.md"
    assert generate_markdown(test_recipe, output_path)

    content = output_path.read_text()
    assert "# Test Recipe" in content
    assert "## Ingredientes" in content
    assert "## Preparación" in content
    assert "- 2 cups flour" in content
    assert "- 1 cup sugar" in content
    assert "- 0.5 teaspoon salt" in content
    assert "1. Mix dry ingredients" in content
    assert "2. Add wet ingredients" in content
    assert "3. Bake at 350F" in content

def test_generate_markdown_minimal(tmp_path):
    """Test markdown generation with minimal recipe."""
    recipe = Recipe(
        metadata = RecipeMetadata(title="Minimal Recipe"), 
        ingredients=[], 
        instructions=[]
)

    output_path = tmp_path / "minimal_recipe.md"
    assert generate_markdown(recipe, output_path)

    content = output_path.read_text()
    assert "# Minimal Recipe" in content
    assert "## Ingredientes" in content
    assert "## Preparación" in content
    assert "- 0" not in content  # No ingredients
    assert "1." not in content  # No instructions

def test_generate_all_markdown(tmp_path):
    """Test generating markdown for multiple recipes."""
    # Create test JSON files
    json_dir = tmp_path / "json"
    json_dir.mkdir()

    recipe1 = Recipe(
        metadata = RecipeMetadata(title="Recipe 1"), 
        ingredients=[Ingredient(nombre="flour", cantidad = 1, unidad="cup")], 
        instructions=["Step 1"]
)

    recipe2 = Recipe(
        metadata = RecipeMetadata(title="Recipe 2"), 
        ingredients=[Ingredient(nombre="sugar", cantidad = 1, unidad="cup")], 
        instructions=["Step 1"]
)

    # Save recipes as JSON
    with open(json_dir / "recipe1.json", "w") as f:
        f.write(recipe1.to_dict())
    with open(json_dir / "recipe2.json", "w") as f:
        f.write(recipe2.to_dict())

    # Generate markdown files
    md_dir = tmp_path / "markdown"
    assert generate_all_markdown(json_dir, md_dir)

    # Verify files were created
    assert (md_dir / "recipe1.md").exists()
    assert (md_dir / "recipe2.md").exists()

def test_generate_all_markdown_empty_dir(tmp_path):
    """Test generating markdown with empty directory."""
    json_dir = tmp_path / "empty"
    md_dir = tmp_path / "markdown"

    assert generate_all_markdown(json_dir, md_dir)
    assert not md_dir.exists()  # Directory should not be created

def test_generate_all_markdown_invalid_json(tmp_path):
    """Test generating markdown with invalid JSON files."""
    json_dir = tmp_path / "invalid"
    json_dir.mkdir()

    # Create invalid JSON file
    with open(json_dir / "invalid.json", "w") as f:
        f.write("invalid json")

    md_dir = tmp_path / "markdown"
    assert not generate_all_markdown(json_dir, md_dir)

"""
Tests for the recipe model module.
"""

from core.domain.recipe.models.ingredient import Ingredient
from core.domain.recipe.models.metadata import RecipeMetadata
from core.domain.recipe.models.recipe import Recipe
from datetime import datetime, timezone

import pytest
@pytest.fixture

def test_metadata():
    """Create test metadata."""
    return RecipeMetadata(
        title="Test Recipe", 
        url="https://example.com/recipe", 
        porciones = 4, 
        calorias = 500, 
        tipo="main", 
        tags=["test", "dinner"], 
        hecho = False, 
        date="2024-03-20", 
        dificultad="medium", 
        tiempo_preparacion = 30, 
        tiempo_coccion = 45, 
        tiempo_total = 75, 
        notas="Test notes"
)

@pytest.fixture

def test_ingredients():
    """Create test ingredients."""
    return [
        Ingredient(nombre="flour", cantidad = 2, unidad="cups"), 
        Ingredient(nombre="sugar", cantidad = 1, unidad="cup"), 
        Ingredient(nombre="salt", cantidad = 0.5, unidad="teaspoon", notas="optional")
    ]

@pytest.fixture

def test_instructions():
    """Create test instructions."""
    return [
        "Mix dry ingredients", 
        "Add wet ingredients", 
        "Bake at 350F"
    ]

@pytest.fixture

def test_recipe(test_metadata, test_ingredients, test_instructions):
    """Create a test recipe."""
    return Recipe(
        title=test_metadata.title,
        metadata = test_metadata, 
        ingredients = test_ingredients, 
        instructions = test_instructions
)

def test_recipe_creation(test_recipe, test_metadata, test_ingredients, test_instructions):
    """Test recipe creation with all components."""
    assert test_recipe.metadata == test_metadata
    assert test_recipe.ingredients == test_ingredients
    assert test_recipe.instructions == test_instructions
    assert isinstance(test_recipe.created_at, datetime)
    assert isinstance(test_recipe.updated_at, datetime)

def test_recipe_properties(test_recipe):
    """Test recipe property accessors."""
    assert test_recipe.title == "Test Recipe"
    assert test_recipe.tipo == "main"
    assert test_recipe.porciones == 4
    assert test_recipe.calorias == 500
    assert test_recipe.tags == ["dinner", "test"]  # Tags are sorted alphabetically
    assert test_recipe.hecho is False
    assert test_recipe.date == "2024-03-20"
    assert test_recipe.source_url == "https://example.com/recipe"

def test_recipe_from_dict():
    """Test recipe creation from dictionary."""
    data = {
        'metadata': {
            'title': 'Test Recipe', 
            'url': 'https://example.com/recipe', 
            'porciones': 4, 
            'calorias': 500, 
            'tipo': 'main', 
            'tags': ['test', 'dinner'], 
            'hecho': False, 
            'date': '2024-03-20', 
            'dificultad': 'medium', 
            'tiempo_preparacion': 30, 
            'tiempo_coccion': 45, 
            'tiempo_total': 75, 
            'notas': 'Test notes'
        }, 
        'ingredients': [
            {'nombre': 'flour', 'cantidad': 2, 'unidad': 'cups'}, 
            {'nombre': 'sugar', 'cantidad': 1, 'unidad': 'cup'}, 
            {'nombre': 'salt', 'cantidad': 0.5, 'unidad': 'teaspoon', 'notas': 'optional'}
        ], 
        'instructions': [
            'Mix dry ingredients', 
            'Add wet ingredients', 
            'Bake at 350F'
        ]
    }

    recipe = Recipe.from_dict(data)
    assert recipe.title == "Test Recipe"
    assert recipe.tipo == "main"
    assert recipe.porciones == 4
    assert len(recipe.ingredients) == 3
    assert len(recipe.instructions) == 3

def test_recipe_to_dict(test_recipe):
    """Test recipe conversion to dictionary."""
    data = test_recipe.to_dict()

    assert data['metadata']['title'] == "Test Recipe"
    assert data['metadata']['tipo'] == "main"
    assert data['metadata']['porciones'] == 4
    assert len(data['ingredients']) == 3
    assert len(data['instructions']) == 3
    assert 'created_at' in data
    assert 'updated_at' in data

def test_recipe_minimal():
    """Test recipe creation with minimal data."""
    metadata = RecipeMetadata(title="Minimal Recipe", tags=[])
    test_ingredient = Ingredient(nombre="test", cantidad=1, unidad="piece")
    recipe = Recipe(title=metadata.title, metadata = metadata, ingredients=[test_ingredient], instructions=["Test instruction"])

    assert recipe.title == "Minimal Recipe"
    assert len(recipe.ingredients) == 1
    assert len(recipe.instructions) == 1
    assert recipe.tipo is None
    assert recipe.porciones is None
    assert recipe.calorias is None
    assert recipe.tags == ["general"]
    assert recipe.hecho is False
    assert len(recipe.date) == 10  # YYYY-MM-DD format
    assert recipe.source_url == "Desconocido"

def test_recipe_optional_fields():
    """Test recipe with optional fields."""
    metadata = RecipeMetadata(
        title="Optional Fields Recipe", 
        tipo = None, 
        porciones = None, 
        calorias = None
)
    test_ingredient = Ingredient(nombre="test", cantidad=1, unidad="piece")
    recipe = Recipe(title=metadata.title, metadata = metadata, ingredients=[test_ingredient], instructions=["Test instruction"])

    assert recipe.tipo is None
    assert recipe.porciones is None
    assert recipe.calorias is None
    assert recipe.source_url == "Desconocido"

def test_recipe_instruction_validation():
    """Test recipe instruction validation."""
    metadata = RecipeMetadata(title="Test Recipe")
    test_ingredient = Ingredient(nombre="test", cantidad=1, unidad="piece")

    # Test empty instructions
    with pytest.raises(ValueError, match="at least 1 item"):
        Recipe(title=metadata.title, metadata = metadata, ingredients=[test_ingredient], instructions=[])

    # Test instruction length limits
    short_instruction = "Too short"
    with pytest.raises(ValueError, match="instruction 1 is too short"):
        Recipe(title=metadata.title, metadata = metadata, ingredients=[test_ingredient], instructions=[short_instruction])

    long_instruction = "x" * 1001
    with pytest.raises(ValueError, match="instruction 1 is too long"):
        Recipe(title=metadata.title, metadata = metadata, ingredients=[test_ingredient], instructions=[long_instruction])

    # Test whitespace handling
    recipe = Recipe(
        title=metadata.title,
        metadata = metadata, 
        ingredients=[test_ingredient],
        instructions=["  Valid instruction  ", "  ", "Another valid instruction"]
)
    assert len(recipe.instructions) == 2
    assert recipe.instructions[0] == "Valid instruction"
    assert recipe.instructions[1] == "Another valid instruction"

def test_recipe_empty_data():
    """Test recipe with empty data."""
    metadata = RecipeMetadata(title="Test Recipe")

    # Test empty ingredients
    with pytest.raises(ValueError, match="at least 1 item"):
        Recipe(title=metadata.title, metadata = metadata, ingredients=[], instructions=["Valid instruction"])

    # Test empty title
    with pytest.raises(ValueError, match="String should have at least 3 characters"):
        Recipe(title="", metadata = RecipeMetadata(title=""))

def test_recipe_invalid_data():
    """Test recipe with invalid data."""
    metadata = RecipeMetadata(title="Test Recipe")
    test_ingredient = Ingredient(nombre="test", cantidad=1, unidad="piece")

    # Test invalid metadata type
    with pytest.raises(ValueError, match="metadata must be a RecipeMetadata instance"):
        Recipe(title="Test Recipe", metadata="invalid")

    # Test invalid ingredients type
    with pytest.raises(ValueError, match="ingredients must be a list"):
        Recipe(title=metadata.title, metadata = metadata, ingredients="invalid", instructions=["Valid instruction"])

    # Test invalid ingredient type
    with pytest.raises(ValueError, match="all ingredients must be Ingredient instances"):
        Recipe(title=metadata.title, metadata = metadata, ingredients=["invalid"], instructions=["Valid instruction"])

    # Test invalid instructions type
    with pytest.raises(ValueError, match="instructions must be a list"):
        Recipe(title=metadata.title, metadata = metadata, ingredients=[test_ingredient], instructions="invalid")

    # Test invalid instruction type
    with pytest.raises(ValueError, match="all instructions must be strings"):
        Recipe(title=metadata.title, metadata = metadata, ingredients=[test_ingredient], instructions=[123])

def test_recipe_datetime_handling():
    """Test recipe datetime handling."""
    # Test creation timestamps
    test_ingredient = Ingredient(nombre="test", cantidad=1, unidad="piece")
    recipe = Recipe(title="Test Recipe", metadata = RecipeMetadata(title="Test Recipe"), ingredients=[test_ingredient], instructions=["Test instruction"])
    assert isinstance(recipe.created_at, datetime)
    assert isinstance(recipe.updated_at, datetime)
    assert abs((recipe.created_at - recipe.updated_at).total_seconds()) < 0.1  # Within 100ms

    # Test update timestamp
    old_updated_at = recipe.updated_at
    recipe.metadata.title = "Updated Recipe"
    assert recipe.updated_at > old_updated_at

    # Test from_dict with timestamps
    data = {
        'metadata': {'title': 'Test Recipe'}, 
        'created_at': '2024-03-20T12:00:00Z', 
        'updated_at': '2024-03-20T12:00:00Z'
    }
    recipe = Recipe.from_dict(data)
    assert recipe.created_at == datetime(2024, 3, 20, 12, 0, 0, tzinfo = timezone.utc)
    assert recipe.updated_at == datetime(2024, 3, 20, 12, 0, 0, tzinfo = timezone.utc)

    # Test to_dict with timestamps
    data = recipe.to_dict()
    assert 'created_at' in data
    assert 'updated_at' in data
    assert isinstance(data['created_at'], str)
    assert isinstance(data['updated_at'], str)

def test_recipe_validation():
    """Test recipe validation."""
    metadata = RecipeMetadata(title="Test Recipe")

    # Test valid recipe
    recipe = Recipe(
        title=metadata.title,
        metadata = metadata, 
        ingredients=[Ingredient(nombre="test", cantidad = 1, unidad="piece")], 
        instructions=["Valid instruction"]
)
    assert recipe.is_valid()

    # Test invalid recipe - no ingredients
    recipe = Recipe(title=metadata.title, metadata = metadata, instructions=["Valid instruction"])
    assert not recipe.is_valid()

    # Test invalid recipe - no instructions
    recipe = Recipe(
        title=metadata.title,
        metadata = metadata, 
        ingredients=[Ingredient(nombre="test", cantidad = 1, unidad="piece")]
)
    assert not recipe.is_valid()

    # Test invalid recipe - invalid metadata
    recipe = Recipe(
        title="",
        metadata = RecipeMetadata(title=""), 
        ingredients=[Ingredient(nombre="test", cantidad = 1, unidad="piece")], 
        instructions=["Valid instruction"]
)
    assert not recipe.is_valid()

def test_recipe_updates():
    """Test recipe updates."""
    recipe = Recipe(
        title="Test Recipe",
        metadata = RecipeMetadata(title="Test Recipe"), 
        ingredients=[Ingredient(nombre="test", cantidad = 1, unidad="piece")], 
        instructions=["Valid instruction"]
)

    # Test metadata update
    old_updated_at = recipe.updated_at
    recipe.metadata.title = "Updated Recipe"
    assert recipe.title == "Updated Recipe"
    assert recipe.updated_at > old_updated_at

    # Test ingredients update
    old_updated_at = recipe.updated_at
    recipe.ingredients.append(Ingredient(nombre="new", cantidad = 1, unidad="piece"))
    assert len(recipe.ingredients) == 2
    assert recipe.updated_at > old_updated_at

    # Test instructions update
    old_updated_at = recipe.updated_at
    recipe.instructions.append("New instruction")
    assert len(recipe.instructions) == 2
    assert recipe.updated_at > old_updated_at

def test_recipe_comparison():
    """Test recipe comparison."""
    recipe1 = Recipe(
        title="Recipe 1",
        metadata = RecipeMetadata(title="Recipe 1"), 
        ingredients=[Ingredient(nombre="test", cantidad = 1, unidad="piece")], 
        instructions=["Valid instruction"]
)

    recipe2 = Recipe(
        title="Recipe 2",
        metadata = RecipeMetadata(title="Recipe 2"), 
        ingredients=[Ingredient(nombre="test", cantidad = 1, unidad="piece")], 
        instructions=["Valid instruction"]
)

    # Test equality
    assert recipe1 != recipe2

    # Test same recipe
    recipe3 = Recipe(
        title="Recipe 1",
        metadata = RecipeMetadata(title="Recipe 1"), 
        ingredients=[Ingredient(nombre="test", cantidad = 1, unidad="piece")], 
        instructions=["Valid instruction"]
)
    assert recipe1 != recipe3  # Different timestamps

    # Test copy
    recipe4 = recipe1.copy()
    assert recipe4 != recipe1  # Different timestamps
    assert recipe4.title == recipe1.title
    assert recipe4.ingredients == recipe1.ingredients
    assert recipe4.instructions == recipe1.instructions

def test_recipe_serialization():
    """Test recipe serialization."""
    recipe = Recipe(
        title="Test Recipe",
        metadata = RecipeMetadata(title="Test Recipe"), 
        ingredients=[Ingredient(nombre="test", cantidad = 1, unidad="piece")], 
        instructions=["Valid instruction"]
)

    # Test to_dict
    data = recipe.to_dict()
    assert isinstance(data, dict)
    assert 'metadata' in data
    assert 'ingredients' in data
    assert 'instructions' in data
    assert 'created_at' in data
    assert 'updated_at' in data

    # Test from_dict
    new_recipe = Recipe.from_dict(data)
    assert new_recipe.title == recipe.title
    assert new_recipe.ingredients == recipe.ingredients
    assert new_recipe.instructions == recipe.instructions

    # Test to_json
    json_data = recipe.to_json()
    assert isinstance(json_data, str)

    # Test from_json
    new_recipe = Recipe.from_json(json_data)
    assert new_recipe.title == recipe.title
    assert new_recipe.ingredients == recipe.ingredients
    assert new_recipe.instructions == recipe.instructions

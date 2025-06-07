"""
Tests for PHI (Microsoft) LLM integration with recipe processing.
"""

import asyncio
import json
import pytest
from pathlib import Path
from core.application.recipe.processor import RecipeProcessor
from core.domain.recipe.models.ingredient import Ingredient
from core.domain.recipe.models.metadata import RecipeMetadata
from core.domain.recipe.models.recipe import Recipe
from core.exceptions import InvalidResponseError
from core.infrastructure.llm.client import LLMClient
from core.utils.logger import get_logger, log_test_result

import pytest_asyncio
import time
logger = get_logger("test_phi")

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

@pytest.mark.asyncio
async def test_phi_recipe_extraction(recipe_processor):
    """Test recipe extraction using Phi model."""
    # Test recipe text
    recipe_text = """
    Classic Chocolate Chip Cookies

    Prep Time: 15 minutes
    Cook Time: 10 minutes
    Servings: 24 cookies

    Ingredients:
    - 2 1 / 4 cups all - purpose flour
    - 1 tsp baking soda
    - 1 tsp salt
    - 1 cup (2 sticks) butter, softened
    - 3 / 4 cup granulated sugar
    - 3 / 4 cup packed brown sugar
    - 2 large eggs
    - 2 tsp vanilla extract
    - 2 cups chocolate chips

    Instructions:
    1. Preheat oven to 375°F (190°C).
    2. Mix flour, baking soda and salt in small bowl.
    3. Beat butter, granulated sugar, brown sugar and vanilla in large mixer bowl.
    4. Add eggs one at a time, beating well after each addition.
    5. Gradually beat in flour mixture.
    6. Stir in chocolate chips.
    7. Drop by rounded tablespoon onto ungreased baking sheets.
    8. Bake for 9 to 11 minutes or until golden brown.
    9. Cool on baking sheets for 2 minutes; remove to wire racks to cool completely.
    """

    # Process recipe
    recipe = await recipe_processor.process_recipe(recipe_text)

    # Verify recipe
    assert isinstance(recipe, Recipe)
    assert recipe.title == "Classic Chocolate Chip Cookies"
    assert recipe.metadata.porciones == 24
    assert recipe.metadata.prep_time == 15
    assert recipe.metadata.cook_time == 10
    assert len(recipe.ingredients) == 9
    assert len(recipe.instructions) == 9

    # Verify ingredients
    flour = next(i for i in recipe.ingredients if i.nombre == "all - purpose flour")
    assert flour.amount == 2.25
    assert flour.unidad == "cups"

    # Verify instructions
    assert "Preheat oven" in recipe.instructions[0]
    assert "Bake for 9 to 11 minutes" in recipe.instructions[7]

@pytest.mark.asyncio
async def test_phi_invalid_recipe(recipe_processor):
    """Test handling of invalid recipe text."""
    # Test with empty text
    with pytest.raises(ValueError):
        await recipe_processor.process_recipe("")

    # Test with invalid format
    with pytest.raises(ValueError):
        await recipe_processor.process_recipe("This is not a recipe")

@pytest.mark.asyncio
async def test_phi_minimal_recipe(recipe_processor):
    """Test extraction of minimal recipe."""
    recipe_text = """
    Simple Toast

    Ingredients:
    - 2 slices bread

    Instructions:
    1. Toast bread
    2. Serve
    """

    recipe = await recipe_processor.process_recipe(recipe_text)

    assert isinstance(recipe, Recipe)
    assert recipe.title == "Simple Toast"
    assert len(recipe.ingredients) == 1
    assert len(recipe.instructions) == 2

@pytest.mark.asyncio
async def test_phi_recipe_with_special_chars(recipe_processor):
    """Test extraction of recipe with special characters."""
    recipe_text = """
    Spicy Thai Curry

    Ingredients:
    - 2 tbsp coconut oil
    - 1 onion, diced
    - 3 cloves garlic, minced
    - 2 tbsp curry paste
    - 1 can (400ml) coconut milk
    - 1 lb chicken, cubed
    - 2 cups vegetables
    - 1 tbsp fish sauce
    - 1 tbsp palm sugar
    - 1 lime, juiced

    Instructions:
    1. Heat oil in large pan
    2. Sauté onion and garlic
    3. Add curry paste and cook 1 minute
    4. Add coconut milk and bring to simmer
    5. Add chicken and cook 15 minutes
    6. Add vegetables and cook 5 minutes
    7. Season with fish sauce, palm sugar, and lime juice
    8. Serve hot with rice
    """

    recipe = await recipe_processor.process_recipe(recipe_text)

    assert isinstance(recipe, Recipe)
    assert recipe.title == "Spicy Thai Curry"
    assert len(recipe.ingredients) == 10
    assert len(recipe.instructions) == 8

    # Verify special characters
    coconut_milk = next(i for i in recipe.ingredients if i.nombre == "coconut milk")
    assert coconut_milk.amount == 1
    assert coconut_milk.unidad == "can"
    assert "400ml" in coconut_milk.notes

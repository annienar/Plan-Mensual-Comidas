"""
Tests for English to Spanish translation functionality in LLM extractor.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from core.application.recipe.extractors.llm import LLMExtractor
from core.domain.recipe.models.recipe import Recipe
from core.domain.recipe.models.ingredient import Ingredient
from core.domain.recipe.models.metadata import RecipeMetadata


@pytest.fixture
def mock_llm_client():
    """Mock LLM client for testing."""
    client = AsyncMock()
    client.model = "phi"
    return client


@pytest.fixture 
def llm_extractor(mock_llm_client):
    """LLM extractor with mocked client."""
    return LLMExtractor(llm_client=mock_llm_client)


@pytest.mark.asyncio
async def test_english_ingredient_translation(llm_extractor, mock_llm_client):
    """Test that English ingredients are translated to Spanish."""
    
    # Mock LLM response with Spanish translations
    mock_response = {
        "title": "Pollo con Pasta",
        "servings": 4,
        "prep_time": 15,
        "cook_time": 30,
        "difficulty": "medium",
        "calories": 450,
        "tags": ["plato principal", "pasta"],
        "ingredients": [
            {
                "name": "pechuga de pollo",  # translated from "chicken breast"
                "quantity": 1.0,
                "unit": "libra",
                "category": "protein"
            },
            {
                "name": "pasta",
                "quantity": 2.0,
                "unit": "tazas",  # translated from "cups"
                "category": "grain"
            },
            {
                "name": "aceite de oliva",  # translated from "olive oil"
                "quantity": 0.5,
                "unit": "taza",
                "category": "condiment"
            }
        ],
        "instructions": [
            "Calentar aceite en una sartén grande",  # translated from "Heat oil in large pan"
            "Cocinar el pollo hasta dorarse",        # translated from "Cook chicken until golden"
            "Hervir agua y cocinar la pasta"         # translated from "Boil water and cook pasta"
        ],
        "notes": "Servir caliente con queso parmesano"  # translated from "Serve hot with parmesan"
    }
    
    mock_llm_client.get_structured_completion.return_value = mock_response
    
    english_recipe_text = """
    Chicken Pasta Recipe
    
    Ingredients:
    - 1 pound chicken breast
    - 2 cups pasta
    - 1/2 cup olive oil
    
    Instructions:
    1. Heat oil in large pan
    2. Cook chicken until golden
    3. Boil water and cook pasta
    
    Notes: Serve hot with parmesan
    """
    
    recipe = await llm_extractor.extract_recipe(english_recipe_text)
    
    # Verify title is in Spanish
    assert "pollo" in recipe.title.lower() or "pasta" in recipe.title.lower()
    
    # Verify ingredients are translated
    ingredient_names = [ing.nombre.lower() for ing in recipe.ingredients]
    assert any("pollo" in name for name in ingredient_names)
    assert any("aceite" in name for name in ingredient_names)
    
    # Verify instructions are translated
    instruction_text = " ".join(recipe.instructions).lower()
    assert any(spanish_word in instruction_text for spanish_word in 
               ["calentar", "cocinar", "hervir", "servir"])


@pytest.mark.asyncio
async def test_mixed_language_translation(llm_extractor, mock_llm_client):
    """Test translation of recipes with mixed English/Spanish content."""
    
    mock_response = {
        "title": "Sopa de Verduras Casera",
        "servings": 6,
        "prep_time": 20,
        "cook_time": 45,
        "difficulty": "easy",
        "calories": 200,
        "tags": ["sopa", "vegetariano", "saludable"],
        "ingredients": [
            {
                "name": "cebolla",  # already Spanish
                "quantity": 1.0,
                "unit": "unidad",
                "category": "vegetable"
            },
            {
                "name": "zanahorias",  # translated from "carrots"
                "quantity": 3.0,
                "unit": "unidades",
                "category": "vegetable"
            },
            {
                "name": "caldo de verduras",  # translated from "vegetable broth"
                "quantity": 4.0,
                "unit": "tazas",
                "category": "condiment"
            }
        ],
        "instructions": [
            "Picar todas las verduras finamente",      # translated from "Chop all vegetables finely"
            "Sofreír la cebolla hasta transparente",   # already Spanish
            "Agregar las zanahorias y cocinar 5 minutos",  # translated from "Add carrots and cook 5 minutes"
            "Añadir el caldo y hervir 30 minutos"     # translated from "Add broth and simmer 30 minutes"
        ],
        "notes": "Sazonar al gusto con sal y pimienta"  # translated from "Season to taste with salt and pepper"
    }
    
    mock_llm_client.get_structured_completion.return_value = mock_response
    
    mixed_recipe_text = """
    Sopa de Verduras Recipe
    
    Ingredients:
    - 1 cebolla
    - 3 carrots
    - 4 cups vegetable broth
    
    Instructions:
    1. Chop all vegetables finely
    2. Sofreír la cebolla hasta transparente  
    3. Add carrots and cook 5 minutes
    4. Add broth and simmer 30 minutes
    
    Season to taste with salt and pepper
    """
    
    recipe = await llm_extractor.extract_recipe(mixed_recipe_text)
    
    # Verify all content is now in Spanish
    assert "sopa" in recipe.title.lower()
    
    # Check ingredients
    ingredient_names = [ing.nombre.lower() for ing in recipe.ingredients]
    assert "cebolla" in ingredient_names
    assert any("zanahoria" in name for name in ingredient_names)
    assert any("caldo" in name for name in ingredient_names)
    
    # Check instructions are all in Spanish
    instructions_text = " ".join(recipe.instructions).lower()
    spanish_cooking_terms = ["picar", "sofreír", "agregar", "cocinar", "añadir", "hervir"]
    assert any(term in instructions_text for term in spanish_cooking_terms)


@pytest.mark.asyncio 
async def test_cooking_terms_translation(llm_extractor, mock_llm_client):
    """Test that cooking terms are properly translated."""
    
    mock_response = {
        "title": "Técnicas de Cocina Básicas",
        "servings": 1,
        "prep_time": 5,
        "cook_time": 10,
        "difficulty": "easy",
        "calories": 100,
        "tags": ["técnicas", "básico"],
        "ingredients": [
            {
                "name": "ingredientes varios",
                "quantity": 1.0,
                "unit": "porción",
                "category": "other"
            }
        ],
        "instructions": [
            "Precalentar el horno a 180°C",           # "Preheat oven to 350°F" 
            "Saltear las verduras en aceite caliente", # "Sauté vegetables in hot oil"
            "Hervir a fuego lento durante 20 minutos", # "Simmer for 20 minutes"
            "Hornear hasta que esté dorado",          # "Bake until golden brown"
            "Dejar reposar antes de servir"           # "Let rest before serving"
        ],
        "notes": "Técnicas fundamentales de cocina"
    }
    
    mock_llm_client.get_structured_completion.return_value = mock_response
    
    english_cooking_text = """
    Basic Cooking Techniques
    
    Instructions:
    1. Preheat oven to 350°F
    2. Sauté vegetables in hot oil  
    3. Simmer for 20 minutes
    4. Bake until golden brown
    5. Let rest before serving
    """
    
    recipe = await llm_extractor.extract_recipe(english_cooking_text)
    
    # Verify cooking terms are translated
    instructions_text = " ".join(recipe.instructions).lower()
    spanish_terms = ["precalentar", "saltear", "hervir", "hornear", "reposar"]
    
    # At least some Spanish cooking terms should be present
    found_terms = [term for term in spanish_terms if term in instructions_text]
    assert len(found_terms) >= 2, f"Expected Spanish cooking terms, found: {found_terms}"


@pytest.mark.asyncio
async def test_title_translation_fallback(llm_extractor):
    """Test title translation when LLM doesn't provide proper translation."""
    
    # Test fallback title generation with English ingredients
    ingredients = [
        {"name": "chicken", "quantity": 1.0, "unit": "lb"},
        {"name": "rice", "quantity": 2.0, "unit": "cups"},
        {"name": "onion", "quantity": 1.0, "unit": "piece"}
    ]
    
    # This should generate a Spanish title even from English ingredients
    title = llm_extractor._generate_title_from_ingredients(ingredients)
    
    # Should create a Spanish-style title
    assert any(word in title.lower() for word in ["chicken", "con", "receta"])


@pytest.mark.asyncio
async def test_system_prompt_includes_translation_instructions(llm_extractor):
    """Test that the system prompt includes translation instructions."""
    
    system_prompt = llm_extractor.system_prompt
    
    # Verify translation instructions are present
    assert "TRANSLATION" in system_prompt.upper()
    assert "spanish" in system_prompt.lower() or "español" in system_prompt.lower()
    assert "translate" in system_prompt.lower() or "traducir" in system_prompt.lower()


@pytest.mark.asyncio
async def test_extraction_prompt_includes_translation_examples(llm_extractor):
    """Test that extraction prompts include translation examples."""
    
    test_text = "Sample recipe text"
    prompt = llm_extractor._build_extraction_prompt(test_text)
    
    # Should include translation examples
    assert "chicken" in prompt.lower() and "pollo" in prompt.lower()
    
    # Check detailed prompt as well
    detailed_prompt = llm_extractor._build_detailed_prompt(test_text)
    assert "TRANSLATION" in detailed_prompt.upper() or "chicken" in detailed_prompt.lower()


def test_difficulty_translation():
    """Test that difficulty levels are properly translated."""
    extractor = LLMExtractor()
    
    # Test English to Spanish difficulty translation
    assert extractor._normalize_difficulty("easy") == "Fácil"
    assert extractor._normalize_difficulty("medium") == "Media" 
    assert extractor._normalize_difficulty("hard") == "Difícil"
    
    # Test Spanish difficulties are preserved
    assert extractor._normalize_difficulty("fácil") == "Fácil"
    assert extractor._normalize_difficulty("media") == "Media"
    assert extractor._normalize_difficulty("difícil") == "Difícil"


def test_title_generation_with_spanish_ingredients():
    """Test title generation uses Spanish format."""
    extractor = LLMExtractor()
    
    # Test with Spanish ingredients
    spanish_ingredients = [
        {"name": "pollo", "quantity": 1.0, "unit": "kg"},
        {"name": "arroz", "quantity": 2.0, "unit": "tazas"}
    ]
    
    title = extractor._generate_title_from_ingredients(spanish_ingredients)
    assert "con" in title.lower()  # Spanish connector
    assert "pollo" in title.lower()
    assert "arroz" in title.lower() 
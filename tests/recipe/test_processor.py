"""
Tests for recipe processor functionality.
"""
import pytest
from pathlib import Path
from typing import Dict, Any

from core.application.recipe.processor import RecipeProcessor

from core.domain.recipe.models.metadata import RecipeMetadata
from core.domain.recipe.models.recipe import Recipe

from unittest.mock import AsyncMock, MagicMock, patch

@pytest.fixture

def sample_recipe():
    """Sample recipe text for testing."""
    return """
    Título: Pollo al Curry
    Porciones: 4
    Tiempo total: 45 minutos

    Ingredientes:
    - 500g de pollo
    - 2 cucharadas de curry
    - 1 cebolla
    - 2 dientes de ajo
    - 200ml de leche de coco

    Instrucciones:
    1. Cortar el pollo en cubos
    2. Picar la cebolla y el ajo
    3. Dorar el pollo
    4. Agregar las verduras
    5. Añadir el curry y la leche de coco
    6. Cocinar por 20 minutos
    """

@pytest.fixture

def high_confidence_llm_response():
    """Sample high confidence LLM response."""
    return {
        "metadata": {
            "title": "Pollo al Curry", 
            "porciones": 4, 
            "tiempo_total": 45, 
            "confidence": 0.9
        }, 
        "ingredients": [
            {"name": "pollo", "quantity": 500, "unit": "g"}, 
            {"name": "curry", "quantity": 2, "unit": "cucharadas"}, 
            {"name": "cebolla", "quantity": 1, "unit": "unidad"}, 
            {"name": "ajo", "quantity": 2, "unit": "dientes"}, 
            {"name": "leche de coco", "quantity": 200, "unit": "ml"}
        ], 
        "instructions": [
            "Cortar el pollo en cubos", 
            "Picar la cebolla y el ajo", 
            "Doran el pollo", 
            "Agregar las verduras", 
            "Añadir el curry y la leche de coco", 
            "Cocinar por 20 minutos"
        ], 
        "confidence": 0.9
    }

@pytest.fixture

def low_confidence_llm_response():
    """Sample low confidence LLM response."""
    return {
        "metadata": {
            "title": "Pollo al Curry", 
            "porciones": 4, 
            "tiempo_total": 45, 
            "confidence": 0.5
        }, 
        "ingredients": [
            {"name": "pollo", "quantity": 500, "unit": "g"}, 
            {"name": "curry", "quantity": 2, "unit": "cucharadas"}
        ], 
        "instructions": [
            "Cortar el pollo", 
            "Cocinar"
        ], 
        "confidence": 0.5
    }

@pytest.mark.asyncio
async def test_process_recipe_high_confidence(sample_recipe, high_confidence_llm_response):
    """Test recipe processing with high confidence LLM response."""
    # Setup
    with patch('core.recipe.extractors.llm.LLMExtractor.extract_with_confidence') as mock_extract:
        mock_extract.return_value = high_confidence_llm_response
        processor = RecipeProcessor()

        # Execute
        result = await processor.process_recipe(sample_recipe)

        # Assert
        assert isinstance(result, Recipe)
        assert result.metadata.title == "Pollo al Curry"
        assert result.metadata.porciones == 4
        assert len(result.ingredients) == 5
        assert len(result.instructions) == 6

@pytest.mark.asyncio
async def test_process_recipe_low_confidence(sample_recipe, low_confidence_llm_response):
    """Test recipe processing with low confidence LLM response."""
    # Setup
    with patch('core.recipe.extractors.llm.LLMExtractor.extract_with_confidence') as mock_extract:
        mock_extract.return_value = low_confidence_llm_response
        processor = RecipeProcessor()

        # Execute
        result = await processor.process_recipe(sample_recipe)

        # Assert
        assert isinstance(result, Recipe)
        # Should use rule - based extraction due to low confidence
        assert result.metadata.title == "Pollo al Curry"
        assert len(result.ingredients) > 2  # Should have more ingredients from rule - based extraction

@pytest.mark.asyncio
async def test_process_recipe_llm_error(sample_recipe):
    """Test recipe processing when LLM extraction fails."""
    # Setup
    with patch('core.recipe.extractors.llm.LLMExtractor.extract_with_confidence') as mock_extract:
        mock_extract.side_effect = Exception("LLM error")
        processor = RecipeProcessor()

        # Execute
        result = await processor.process_recipe(sample_recipe)

        # Assert
        assert isinstance(result, Recipe)
        # Should use rule - based extraction due to error
        assert result.metadata.title == "Pollo al Curry"
        assert len(result.ingredients) > 0

@pytest.mark.asyncio
async def test_process_recipe_validation(sample_recipe, high_confidence_llm_response):
    """Test recipe processing validation."""
    # Setup
    with patch('core.recipe.extractors.llm.LLMExtractor.extract_with_confidence') as mock_extract:
        mock_extract.return_value = high_confidence_llm_response
        processor = RecipeProcessor()

        # Execute
        result = await processor.process_recipe(sample_recipe)

        # Assert
        assert isinstance(result, Recipe)
        assert isinstance(result.metadata, RecipeMetadata)
        assert all(hasattr(ing, 'name') for ing in result.ingredients)
        assert all(hasattr(ing, 'quantity') for ing in result.ingredients)
        assert all(hasattr(ing, 'unit') for ing in result.ingredients)
        assert all(isinstance(step, str) for step in result.instructions)

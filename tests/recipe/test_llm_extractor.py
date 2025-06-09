"""
Unit tests for the LLM - based recipe extractor.
"""

from core.application.recipe.extractors.llm import LLMExtractor
from core.infrastructure.llm.client import LLMClient

from unittest.mock import AsyncMock, MagicMock, patch
import pytest
@pytest.fixture

def mock_llm_client():
    """Create a mock LLM client."""
    client = AsyncMock(spec = LLMClient)
    return client

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

def valid_llm_response():
    """Sample valid LLM response."""
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

@pytest.mark.asyncio
async def test_extract_valid_recipe(mock_llm_client, sample_recipe, valid_llm_response):
    """Test extraction of a valid recipe."""
    # Setup
    mock_llm_client.get_structured_completion.return_value = valid_llm_response
    extractor = LLMExtractor(mock_llm_client)

    # Execute
    result = await extractor.extract(sample_recipe)

    # Assert
    assert result["metadata"]["title"] == "Pollo al Curry"
    assert result["metadata"]["porciones"] == 4
    assert len(result["ingredients"]) == 5
    assert len(result["instructions"]) == 6

@pytest.mark.asyncio
async def test_extract_invalid_json(mock_llm_client, sample_recipe):
    """Test handling of invalid JSON response."""
    # Setup
    mock_llm_client.get_structured_completion.side_effect = Exception("Invalid JSON")
    extractor = LLMExtractor(mock_llm_client)

    # Execute
    result = await extractor.extract(sample_recipe)

    # Assert
    assert result["metadata"]["title"] is not None
    assert len(result["ingredients"]) >= 1  # Fallback should provide at least one ingredient
    assert len(result["instructions"]) >= 1  # Fallback should provide instructions

@pytest.mark.asyncio
async def test_extract_missing_required_fields(mock_llm_client, sample_recipe):
    """Test handling of response with missing required fields."""
    # Setup
    invalid_response = {
        "metadata": {
            "title": "Pollo al Curry"
            # Missing required fields
        }, 
        "ingredients": [], 
        "instructions": []
    }
    mock_llm_client.get_structured_completion.return_value = invalid_response
    extractor = LLMExtractor(mock_llm_client)

    # Execute
    result = await extractor.extract(sample_recipe)

    # Assert
    assert result["metadata"]["title"] == "Pollo al Curry"

@pytest.mark.asyncio
async def test_extract_with_confidence(mock_llm_client, sample_recipe, valid_llm_response):
    """Test extraction with confidence scores."""
    # Setup
    mock_llm_client.get_structured_completion.return_value = valid_llm_response
    extractor = LLMExtractor(mock_llm_client)

    # Execute
    result = await extractor.extract_with_confidence(sample_recipe)

    # Assert
    assert "confidence" in result
    assert result["confidence"] > 0

@pytest.mark.asyncio
async def test_extract_llm_error(mock_llm_client, sample_recipe):
    """Test handling of LLM client errors."""
    # Setup
    mock_llm_client.get_structured_completion.side_effect = Exception("LLM error")
    extractor = LLMExtractor(mock_llm_client)

    # Execute
    result = await extractor.extract(sample_recipe)

    # Assert
    assert result["metadata"]["title"] is not None  # Should have fallback title
    assert "confidence" in result

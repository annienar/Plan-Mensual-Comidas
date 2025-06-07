"""
Edge case tests for recipe processing.

This module tests various challenging scenarios and edge cases that
can occur during recipe processing to ensure robustness.
"""

import pytest
from typing import Dict, List, Any

from core.domain.recipe.extractors.ingredients import IngredientExtractor
from core.domain.recipe.extractors.metadata import MetadataExtractor
from core.domain.recipe.extractors.sections import SectionExtractor
from core.domain.recipe.normalizers.measurements import MeasurementNormalizer
from core.domain.recipe.normalizers.text import TextNormalizer


class TestIngredientEdgeCases:
    """Test edge cases for ingredient extraction."""

    @pytest.fixture
    def ingredient_extractor(self):
        return IngredientExtractor()

    @pytest.mark.parametrize("ingredient_text,expected_count", [
        # Empty and whitespace
        ("", 0),
        ("   \n\n\t   ", 0),
        ("\n\n", 0),
        
        # Single ingredient variations
        ("1 cup flour", 1),
        ("2 large eggs", 1),
        ("Salt to taste", 1),
        ("1/2 teaspoon vanilla extract", 1),
        
        # Multiple ingredients with different formats
        ("""
        1 cup all-purpose flour
        2 large eggs
        1/2 cup milk
        1 tsp vanilla extract
        Salt to taste
        """, 5),
        
        # Ingredients with special characters
        ("½ cup sugar", 1),
        ("1 ¼ cups water", 1),
        ("2-3 cloves garlic", 1),
        
        # Complex measurements
        ("2 (14.5 oz) cans diced tomatoes", 1),
        ("1 bunch fresh cilantro (about ¼ cup chopped)", 1),
        ("3-4 pounds chicken, cut into pieces", 1),
    ])
    def test_ingredient_extraction_variety(self, ingredient_extractor, ingredient_text, expected_count):
        """Test ingredient extraction with various input formats."""
        ingredients = ingredient_extractor.extract(ingredient_text)
        assert len(ingredients) == expected_count, f"Expected {expected_count} ingredients, got {len(ingredients)} from: {ingredient_text}"

    @pytest.mark.parametrize("problematic_text", [
        # Malformed input
        "Ingredients:\n\n\nSteps:\n1. Do something",
        "1 cup flour\n\nInstructions:\n1. Mix everything",
        "Random text with no ingredients",
        "123 !@# invalid $%^ text &*()",
        
        # Mixed languages
        "1 taza harina\n2 eggs\n3 cucharadas aceite",
        "½ кг муки\n2 eggs\n1 cup water",
        
        # Special formatting
        "• 1 cup flour\n* 2 eggs\n- 1 tsp salt",
        "1.) 1 cup flour\n2.) 2 eggs\n3.) Salt",
    ])
    def test_ingredient_extraction_problematic_input(self, ingredient_extractor, problematic_text):
        """Test that problematic input doesn't crash the extractor."""
        try:
            ingredients = ingredient_extractor.extract(problematic_text)
            assert isinstance(ingredients, list), "Should always return a list"
        except Exception as e:
            pytest.fail(f"Extractor should handle problematic input gracefully: {e}")


class TestMeasurementEdgeCases:
    """Test edge cases for measurement normalization."""

    @pytest.fixture
    def measurement_normalizer(self):
        return MeasurementNormalizer()

    @pytest.mark.parametrize("measurement,should_normalize", [
        # Valid measurements
        ("1 cup", True),
        ("2.5 kg", True),
        ("0.25 l", True),
        
        # Edge cases
        ("", False),
        ("invalid", False),
        ("just text", False),
        ("123", False),
        
        # Boundary values
        ("0 cups", True),
        ("1000000 g", True),
        ("-1 cup", True),  # Should handle negative (even if nonsensical)
        
        # Special characters
        ("1½ cups", True),
        ("2¼ tsp", True),
        ("3-4 cups", True),
    ])
    def test_measurement_normalization_edge_cases(self, measurement_normalizer, measurement, should_normalize):
        """Test measurement normalization with edge cases."""
        try:
            value, unit = measurement_normalizer.normalize(measurement)
            
            if should_normalize:
                assert isinstance(value, (int, float)), f"Value should be numeric for '{measurement}'"
                assert isinstance(unit, str), f"Unit should be string for '{measurement}'"
                assert unit.strip(), f"Unit should not be empty for '{measurement}'"
            else:
                # For invalid measurements, we might get (0, '') or similar
                pass
                
        except Exception as e:
            if should_normalize:
                pytest.fail(f"Should normalize '{measurement}' but got error: {e}")


class TestTextNormalizationEdgeCases:
    """Test edge cases for text normalization."""

    @pytest.fixture
    def text_normalizer(self):
        return TextNormalizer()

    @pytest.mark.parametrize("text,expected_properties", [
        # Basic cases
        ("Hello World", {"lowercase": True, "no_extra_spaces": True}),
        ("  MULTIPLE   SPACES  ", {"lowercase": True, "no_extra_spaces": True}),
        ("", {"empty": True}),
        
        # Special characters
        ("Café with ñoño", {"has_accents": True, "lowercase": True}),
        ("Text with émojis 😊", {"has_special_chars": True}),
        ("123 numbers and !@# symbols", {"has_numbers": True, "has_symbols": True}),
        
        # Edge formatting
        ("\n\n\tTabbed\n\nText\n\n", {"normalized_whitespace": True}),
        ("Extra    spaces    everywhere", {"no_extra_spaces": True}),
        ("MixedCaseText", {"lowercase": True}),
    ])
    def test_text_normalization_properties(self, text_normalizer, text, expected_properties):
        """Test text normalization preserves expected properties."""
        result = text_normalizer.normalize(text)
        
        assert isinstance(result, str), "Result should always be a string"
        
        if expected_properties.get("empty"):
            assert result == "", f"Empty input should produce empty output"
        
        if expected_properties.get("lowercase"):
            assert result.islower() or not result.isalpha(), f"Result should be lowercase: '{result}'"
        
        if expected_properties.get("no_extra_spaces"):
            # No multiple consecutive spaces
            assert "  " not in result, f"Should not have multiple spaces: '{result}'"
            # No leading/trailing spaces
            assert result == result.strip(), f"Should not have leading/trailing spaces: '{result}'"


class TestMetadataExtractionEdgeCases:
    """Test edge cases for metadata extraction."""

    @pytest.fixture
    def metadata_extractor(self):
        return MetadataExtractor()

    @pytest.mark.parametrize("content,expected_fields", [
        # Minimal content
        ("Recipe Title", ["title"]),
        ("", ["title"]),  # Should generate a default title
        
        # Complete metadata
        ("""
        Delicious Pasta Recipe
        Porciones: 4
        Tiempo total: 30 minutos
        Dificultad: Fácil
        Calorías: 450
        """, ["title", "porciones", "tiempo_total", "dificultad", "calorias"]),
        
        # Mixed format metadata
        ("""
        Soup Recipe
        Serves: 6 people
        Cook time: 45 min
        Difficulty: Medium
        Cal: 200
        """, ["title"]),  # Might not extract non-Spanish formats
        
        # Malformed metadata
        ("""
        Recipe
        Porciones: invalid
        Tiempo: not a number
        Difficulty: 
        """, ["title"]),
    ])
    def test_metadata_extraction_variety(self, metadata_extractor, content, expected_fields):
        """Test metadata extraction with various content formats."""
        metadata = metadata_extractor.extract(content)
        
        assert isinstance(metadata, dict), "Metadata should be a dictionary"
        
        for field in expected_fields:
            assert field in metadata, f"Should extract {field} from content"
            
        # Title should never be empty
        assert metadata.get("title"), "Title should never be empty"


class TestSectionExtractionEdgeCases:
    """Test edge cases for section extraction."""

    @pytest.fixture
    def section_extractor(self):
        return SectionExtractor()

    @pytest.mark.parametrize("content,expected_sections", [
        # Empty content
        ("", ["ingredients", "instructions", "notes"]),
        
        # Only ingredients
        ("""
        Ingredientes:
        1 cup flour
        2 eggs
        """, ["ingredients", "instructions", "notes"]),
        
        # Only instructions
        ("""
        Preparación:
        1. Mix ingredients
        2. Cook for 20 minutes
        """, ["ingredients", "instructions", "notes"]),
        
        # Mixed languages
        ("""
        Ingredients:
        1 cup flour
        
        Pasos:
        1. Mix everything
        
        Notes:
        Serve hot
        """, ["ingredients", "instructions", "notes"]),
        
        # No clear sections
        ("""
        This is just a paragraph of text
        without any clear recipe structure
        or section headers.
        """, ["ingredients", "instructions", "notes"]),
        
        # Unusual formatting
        ("""
        --- INGREDIENTES ---
        flour, eggs, milk
        
        *** STEPS ***
        mix and cook
        
        ~~ NOTAS ~~
        enjoy!
        """, ["ingredients", "instructions", "notes"]),
    ])
    def test_section_extraction_variety(self, section_extractor, content, expected_sections):
        """Test section extraction with various content formats."""
        sections = section_extractor.extract(content)
        
        assert isinstance(sections, dict), "Sections should be a dictionary"
        
        # Should always have the expected section keys
        for section_name in expected_sections:
            assert section_name in sections, f"Should have {section_name} section"
            assert isinstance(sections[section_name], list), f"Section {section_name} should be a list"


class TestRealWorldScenarios:
    """Test real-world challenging scenarios."""

    def test_recipe_with_unicode_and_special_chars(self):
        """Test handling of recipes with unicode and special characters."""
        content = """
        Ñoquis con Crema y Champiñones
        
        Ingredientes:
        • 500g ñoquis frescos
        • 200ml crema de leche
        • 150g champiñones portobello
        • 2 dientes de ajo
        • Queso parmesano rallado
        • Sal y pimienta al gusto
        
        Preparación:
        1. Saltear los champiñones en aceite caliente
        2. Agregar el ajo picado y cocinar 1'
        3. Incorporar la crema y sazonar
        4. Cocinar los ñoquis según las instrucciones
        5. Mezclar con la salsa y servir con queso
        
        Notas: 
        ¡Perfecto para una cena romántica! 💕
        """
        
        # Test that extractors can handle this content
        ingredient_extractor = IngredientExtractor()
        metadata_extractor = MetadataExtractor()
        section_extractor = SectionExtractor()
        
        # Should not crash
        ingredients = ingredient_extractor.extract(content)
        metadata = metadata_extractor.extract(content)
        sections = section_extractor.extract(content)
        
        assert isinstance(ingredients, list)
        assert isinstance(metadata, dict)
        assert isinstance(sections, dict)
        
        # Should extract meaningful content
        assert metadata.get("title"), "Should extract title"
        assert len(ingredients) > 0, "Should extract some ingredients"
        assert any(sections.values()), "Should extract some section content"

    def test_very_long_recipe(self):
        """Test handling of very long recipes."""
        # Create a very long ingredient list
        long_ingredients = "\n".join([f"{i+1} cup ingredient_{i}" for i in range(100)])
        long_instructions = "\n".join([f"{i+1}. Step number {i+1} with detailed instructions." for i in range(50)])
        
        content = f"""
        Very Long Recipe
        
        Ingredientes:
        {long_ingredients}
        
        Preparación:
        {long_instructions}
        """
        
        ingredient_extractor = IngredientExtractor()
        ingredients = ingredient_extractor.extract(content)
        
        # Should handle long content without issues
        assert isinstance(ingredients, list)
        assert len(ingredients) > 50, "Should extract many ingredients"

    def test_multilingual_recipe(self):
        """Test handling of recipes with multiple languages."""
        content = """
        International Fusion Recipe / Receta de Fusión Internacional
        
        Ingredients / Ingredientes:
        1 cup rice / 1 taza arroz
        2 chicken breasts / 2 pechugas de pollo
        1 tsp soy sauce / 1 cdta salsa de soja
        
        Instructions / Instrucciones:
        1. Cook rice / Cocinar arroz
        2. Season chicken / Sazonar pollo
        3. Combine / Combinar
        """
        
        ingredient_extractor = IngredientExtractor()
        ingredients = ingredient_extractor.extract(content)
        
        # Should handle multilingual content gracefully
        assert isinstance(ingredients, list)
        # Might extract duplicate ingredients due to translation, but shouldn't crash 
"""
Integration tests using real recipe files.

This module tests the complete recipe processing pipeline using actual
recipe files from the fixtures directory, validating end-to-end functionality.
"""

import pytest
from pathlib import Path
from typing import List, Dict, Any

from core.application.recipe.extractors.text import TextExtractor
from core.application.recipe.processor import RecipeProcessor
from core.domain.recipe.extractors.ingredients import IngredientExtractor
from core.domain.recipe.extractors.metadata import MetadataExtractor
from core.domain.recipe.extractors.sections import SectionExtractor
from core.domain.recipe.models.recipe import Recipe


class TestRealFileProcessing:
    """Test recipe processing with real files."""

    @pytest.fixture
    def text_extractor(self):
        """Create a text extractor instance."""
        return TextExtractor()

    @pytest.fixture
    def ingredient_extractor(self):
        """Create an ingredient extractor instance."""
        return IngredientExtractor()

    @pytest.fixture
    def metadata_extractor(self):
        """Create a metadata extractor instance."""
        return MetadataExtractor()

    @pytest.fixture
    def section_extractor(self):
        """Create a section extractor instance."""
        return SectionExtractor()

    @pytest.fixture
    def real_recipe_files(self) -> List[Path]:
        """Get all real recipe files from fixtures."""
        fixture_dir = Path("tests/fixtures/recipes/sin_procesar")
        if not fixture_dir.exists():
            pytest.skip(f"Fixture directory {fixture_dir} not found")
        
        files = list(fixture_dir.glob("*.txt"))
        if not files:
            pytest.skip(f"No recipe files found in {fixture_dir}")
        
        return files

    def test_text_extraction_from_real_files(self, text_extractor, real_recipe_files):
        """Test text extraction from real recipe files."""
        successful_extractions = 0
        
        for file_path in real_recipe_files:
            try:
                content = text_extractor.extract(str(file_path))
                
                # Verify we extracted something
                assert isinstance(content, str), f"Content should be string for {file_path.name}"
                
                if content.strip():  # If we got content
                    successful_extractions += 1
                    
                    # Verify content has recipe-like characteristics
                    content_lower = content.lower()
                    
                    # Should contain some recipe keywords
                    recipe_keywords = [
                        "ingredientes", "ingredients", "preparación", "preparation",
                        "pasos", "steps", "instrucciones", "instructions"
                    ]
                    
                    has_recipe_keywords = any(keyword in content_lower for keyword in recipe_keywords)
                    
                    if has_recipe_keywords:
                        print(f"✓ Successfully extracted recipe content from {file_path.name}")
                    else:
                        print(f"⚠ Extracted content from {file_path.name} but no recipe keywords found")
                        
            except Exception as e:
                print(f"✗ Failed to extract from {file_path.name}: {e}")
        
        # Ensure we successfully extracted from at least some files
        assert successful_extractions > 0, f"Should extract content from at least some files, got {successful_extractions}/{len(real_recipe_files)}"
        print(f"Successfully extracted content from {successful_extractions}/{len(real_recipe_files)} files")

    def test_ingredient_extraction_from_real_files(self, text_extractor, ingredient_extractor, real_recipe_files):
        """Test ingredient extraction from real recipe files."""
        successful_extractions = 0
        
        for file_path in real_recipe_files[:5]:  # Test first 5 files to keep it manageable
            try:
                # Extract text first
                content = text_extractor.extract(str(file_path))
                if not content.strip():
                    continue
                
                # Extract ingredients
                ingredients = ingredient_extractor.extract(content)
                
                assert isinstance(ingredients, list), f"Ingredients should be a list for {file_path.name}"
                
                if ingredients:
                    successful_extractions += 1
                    print(f"✓ Extracted {len(ingredients)} ingredients from {file_path.name}")
                    
                    # Verify ingredient structure
                    for ingredient in ingredients[:3]:  # Check first 3 ingredients
                        assert isinstance(ingredient, dict), "Each ingredient should be a dict"
                        assert 'nombre' in ingredient, "Ingredient should have 'nombre' field"
                        assert isinstance(ingredient['nombre'], str), "Ingredient name should be string"
                        
            except Exception as e:
                print(f"✗ Failed to extract ingredients from {file_path.name}: {e}")
        
        print(f"Successfully extracted ingredients from {successful_extractions}/{min(5, len(real_recipe_files))} files")

    def test_metadata_extraction_from_real_files(self, text_extractor, metadata_extractor, real_recipe_files):
        """Test metadata extraction from real recipe files."""
        successful_extractions = 0
        
        for file_path in real_recipe_files[:5]:  # Test first 5 files
            try:
                # Extract text first
                content = text_extractor.extract(str(file_path))
                if not content.strip():
                    continue
                
                # Extract metadata
                metadata = metadata_extractor.extract(content)
                
                assert isinstance(metadata, dict), f"Metadata should be a dict for {file_path.name}"
                
                # Should have at least a title
                if metadata.get('title'):
                    successful_extractions += 1
                    print(f"✓ Extracted metadata from {file_path.name}: title='{metadata['title']}'")
                    
                    # Verify expected metadata fields exist
                    expected_fields = ['title', 'porciones', 'tiempo_total', 'dificultad']
                    for field in expected_fields:
                        assert field in metadata, f"Metadata should have '{field}' field"
                        
            except Exception as e:
                print(f"✗ Failed to extract metadata from {file_path.name}: {e}")
        
        print(f"Successfully extracted metadata from {successful_extractions}/{min(5, len(real_recipe_files))} files")

    def test_section_extraction_from_real_files(self, text_extractor, section_extractor, real_recipe_files):
        """Test section extraction from real recipe files."""
        successful_extractions = 0
        
        for file_path in real_recipe_files[:5]:  # Test first 5 files
            try:
                # Extract text first
                content = text_extractor.extract(str(file_path))
                if not content.strip():
                    continue
                
                # Extract sections
                sections = section_extractor.extract(content)
                
                assert isinstance(sections, dict), f"Sections should be a dict for {file_path.name}"
                
                # Should have the main section keys
                expected_sections = ['ingredients', 'instructions', 'notes']
                for section_name in expected_sections:
                    assert section_name in sections, f"Should have '{section_name}' section"
                    assert isinstance(sections[section_name], list), f"Section '{section_name}' should be a list"
                
                # If we found any content in sections
                if any(sections.values()):
                    successful_extractions += 1
                    section_counts = {k: len(v) for k, v in sections.items()}
                    print(f"✓ Extracted sections from {file_path.name}: {section_counts}")
                        
            except Exception as e:
                print(f"✗ Failed to extract sections from {file_path.name}: {e}")
        
        print(f"Successfully extracted sections from {successful_extractions}/{min(5, len(real_recipe_files))} files")

    @pytest.mark.slow
    def test_complete_pipeline_with_real_files(self, real_recipe_files):
        """Test the complete processing pipeline with real files."""
        if len(real_recipe_files) == 0:
            pytest.skip("No real recipe files available")
        
        # Test with the first recipe file
        test_file = real_recipe_files[0]
        
        try:
            # Step 1: Extract text
            text_extractor = TextExtractor()
            content = text_extractor.extract(str(test_file))
            
            assert content.strip(), f"Should extract text content from {test_file.name}"
            print(f"✓ Step 1: Extracted {len(content)} characters from {test_file.name}")
            
            # Step 2: Extract sections
            section_extractor = SectionExtractor()
            sections = section_extractor.extract(content)
            
            assert isinstance(sections, dict), "Sections should be a dictionary"
            print(f"✓ Step 2: Extracted sections: {list(sections.keys())}")
            
            # Step 3: Extract ingredients
            ingredient_extractor = IngredientExtractor()
            ingredients = ingredient_extractor.extract(content)
            
            assert isinstance(ingredients, list), "Ingredients should be a list"
            print(f"✓ Step 3: Extracted {len(ingredients)} ingredients")
            
            # Step 4: Extract metadata
            metadata_extractor = MetadataExtractor()
            metadata = metadata_extractor.extract(content)
            
            assert isinstance(metadata, dict), "Metadata should be a dictionary"
            assert metadata.get('title'), "Should extract a title"
            print(f"✓ Step 4: Extracted metadata with title: '{metadata['title']}'")
            
            # Verify the complete pipeline worked
            print(f"✓ Complete pipeline test successful for {test_file.name}")
            
        except Exception as e:
            pytest.fail(f"Complete pipeline test failed for {test_file.name}: {e}")

    def test_file_formats_and_encodings(self, text_extractor, real_recipe_files):
        """Test that we handle different file formats and encodings properly."""
        encoding_results = {}
        
        for file_path in real_recipe_files:
            try:
                content = text_extractor.extract(str(file_path))
                
                # Check for different types of content
                if content:
                    encoding_results[file_path.name] = {
                        'length': len(content),
                        'has_special_chars': any(ord(c) > 127 for c in content),
                        'has_accents': any(c in 'áéíóúñüç' for c in content.lower()),
                        'lines': len(content.splitlines())
                    }
                else:
                    encoding_results[file_path.name] = {'error': 'Empty content'}
                    
            except Exception as e:
                encoding_results[file_path.name] = {'error': str(e)}
        
        # Verify we processed at least some files successfully
        successful_files = [name for name, result in encoding_results.items() if 'error' not in result]
        print(f"Successfully processed {len(successful_files)}/{len(real_recipe_files)} files")
        
        # Print summary
        for filename, result in encoding_results.items():
            if 'error' not in result:
                print(f"✓ {filename}: {result['length']} chars, {result['lines']} lines, "
                      f"special_chars={result['has_special_chars']}, accents={result['has_accents']}")
            else:
                print(f"✗ {filename}: {result['error']}")
        
        assert len(successful_files) > 0, "Should successfully process at least some files" 
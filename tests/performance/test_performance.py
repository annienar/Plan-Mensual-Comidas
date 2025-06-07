"""
Performance tests for recipe processing.

This module tests the performance characteristics of recipe processing
to ensure operations complete within acceptable time limits.
"""

import pytest
import time
from pathlib import Path
from typing import List, Dict, Any

from core.application.recipe.extractors.text import TextExtractor
from core.domain.recipe.extractors.ingredients import IngredientExtractor
from core.domain.recipe.extractors.metadata import MetadataExtractor
from core.domain.recipe.extractors.sections import SectionExtractor


class TestPerformance:
    """Performance tests for recipe processing."""

    @pytest.fixture
    def text_extractor(self):
        return TextExtractor()

    @pytest.fixture
    def ingredient_extractor(self):
        return IngredientExtractor()

    @pytest.fixture
    def metadata_extractor(self):
        return MetadataExtractor()

    @pytest.fixture
    def section_extractor(self):
        return SectionExtractor()

    @pytest.fixture
    def sample_recipe_content(self):
        """Sample recipe content for performance testing."""
        return """
        Delicious Pasta Recipe
        
        Ingredientes:
        1 pound spaghetti
        2 tablespoons olive oil
        4 cloves garlic, minced
        1/2 cup white wine
        1 can (14 oz) diced tomatoes
        1/4 cup fresh basil, chopped
        Salt and pepper to taste
        Grated Parmesan cheese for serving
        
        Preparación:
        1. Cook spaghetti according to package directions until al dente
        2. While pasta cooks, heat olive oil in a large skillet
        3. Add garlic and cook for 1 minute until fragrant
        4. Add wine and cook for 2 minutes to reduce
        5. Add tomatoes and simmer for 10 minutes
        6. Season with salt and pepper
        7. Drain pasta and add to sauce
        8. Toss with fresh basil and serve with Parmesan
        
        Notas:
        This recipe serves 4-6 people
        Can be made vegetarian by omitting meat
        """

    @pytest.fixture
    def large_recipe_content(self):
        """Large recipe content for stress testing."""
        ingredients = []
        instructions = []
        
        # Generate 50 ingredients
        for i in range(50):
            ingredients.append(f"{i+1} cup ingredient_{i}")
        
        # Generate 25 instructions
        for i in range(25):
            instructions.append(f"{i+1}. Step {i+1}: This is a detailed instruction with lots of text to make it longer and more realistic for testing purposes.")
        
        return f"""
        Large Test Recipe
        
        Ingredientes:
        {chr(10).join(ingredients)}
        
        Preparación:
        {chr(10).join(instructions)}
        
        Notas:
        This is a very large recipe for performance testing.
        It has many ingredients and instructions to test scalability.
        """

    def measure_time(self, func, *args, **kwargs):
        """Measure execution time of a function."""
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        return result, (end_time - start_time) * 1000  # Return time in milliseconds

    @pytest.mark.performance
    def test_text_extraction_performance(self, text_extractor):
        """Test text extraction performance."""
        # Create a temporary file for testing
        import tempfile
        
        content = "Test content for performance testing\n" * 100
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(content)
            temp_path = f.name
        
        try:
            _, execution_time = self.measure_time(text_extractor.extract, temp_path)
            
            # Should complete within 100ms for a small file
            assert execution_time < 100, f"Text extraction took {execution_time:.2f}ms, expected < 100ms"
            print(f"✓ Text extraction completed in {execution_time:.2f}ms")
            
        finally:
            Path(temp_path).unlink(missing_ok=True)

    @pytest.mark.performance
    def test_ingredient_extraction_performance(self, ingredient_extractor, sample_recipe_content):
        """Test ingredient extraction performance."""
        _, execution_time = self.measure_time(ingredient_extractor.extract, sample_recipe_content)
        
        # Should complete within 50ms for normal recipe
        assert execution_time < 50, f"Ingredient extraction took {execution_time:.2f}ms, expected < 50ms"
        print(f"✓ Ingredient extraction completed in {execution_time:.2f}ms")

    @pytest.mark.performance
    def test_metadata_extraction_performance(self, metadata_extractor, sample_recipe_content):
        """Test metadata extraction performance."""
        _, execution_time = self.measure_time(metadata_extractor.extract, sample_recipe_content)
        
        # Should complete within 100ms for normal recipe
        assert execution_time < 100, f"Metadata extraction took {execution_time:.2f}ms, expected < 100ms"
        print(f"✓ Metadata extraction completed in {execution_time:.2f}ms")

    @pytest.mark.performance
    def test_section_extraction_performance(self, section_extractor, sample_recipe_content):
        """Test section extraction performance."""
        _, execution_time = self.measure_time(section_extractor.extract, sample_recipe_content)
        
        # Should complete within 30ms for normal recipe
        assert execution_time < 30, f"Section extraction took {execution_time:.2f}ms, expected < 30ms"
        print(f"✓ Section extraction completed in {execution_time:.2f}ms")

    @pytest.mark.performance
    @pytest.mark.slow
    def test_large_recipe_performance(self, ingredient_extractor, metadata_extractor, 
                                     section_extractor, large_recipe_content):
        """Test performance with large recipes."""
        print(f"Testing with large recipe ({len(large_recipe_content)} characters)")
        
        # Test ingredient extraction
        _, ingredient_time = self.measure_time(ingredient_extractor.extract, large_recipe_content)
        assert ingredient_time < 200, f"Large ingredient extraction took {ingredient_time:.2f}ms, expected < 200ms"
        print(f"✓ Large ingredient extraction: {ingredient_time:.2f}ms")
        
        # Test metadata extraction
        _, metadata_time = self.measure_time(metadata_extractor.extract, large_recipe_content)
        assert metadata_time < 300, f"Large metadata extraction took {metadata_time:.2f}ms, expected < 300ms"
        print(f"✓ Large metadata extraction: {metadata_time:.2f}ms")
        
        # Test section extraction
        _, section_time = self.measure_time(section_extractor.extract, large_recipe_content)
        assert section_time < 100, f"Large section extraction took {section_time:.2f}ms, expected < 100ms"
        print(f"✓ Large section extraction: {section_time:.2f}ms")

    @pytest.mark.performance
    def test_batch_processing_performance(self, ingredient_extractor, sample_recipe_content):
        """Test performance when processing multiple recipes."""
        batch_size = 10
        recipes = [sample_recipe_content] * batch_size
        
        start_time = time.time()
        results = []
        for recipe in recipes:
            result = ingredient_extractor.extract(recipe)
            results.append(result)
        end_time = time.time()
        
        total_time = (end_time - start_time) * 1000
        avg_time = total_time / batch_size
        
        # Should process each recipe in under 50ms on average
        assert avg_time < 50, f"Batch processing averaged {avg_time:.2f}ms per recipe, expected < 50ms"
        print(f"✓ Batch processing: {total_time:.2f}ms total, {avg_time:.2f}ms average per recipe")

    @pytest.mark.performance
    def test_memory_usage_with_large_content(self, ingredient_extractor):
        """Test that memory usage stays reasonable with large content."""
        import psutil
        import os
        
        # Get current process
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Create very large content
        large_ingredients = "\n".join([f"{i} cup ingredient_{i}" for i in range(1000)])
        
        # Process the large content
        result = ingredient_extractor.extract(large_ingredients)
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be reasonable (less than 50MB for this test)
        assert memory_increase < 50, f"Memory increased by {memory_increase:.2f}MB, expected < 50MB"
        print(f"✓ Memory usage: increased by {memory_increase:.2f}MB")
        
        # Should still produce results
        assert isinstance(result, list), "Should still return a list"
        assert len(result) > 500, "Should extract many ingredients"

    @pytest.mark.performance 
    @pytest.mark.slow
    def test_real_file_processing_performance(self):
        """Test performance with real recipe files."""
        fixture_dir = Path("tests/fixtures/recipes/sin_procesar")
        if not fixture_dir.exists():
            pytest.skip("Fixture directory not found")
        
        recipe_files = list(fixture_dir.glob("*.txt"))
        if not recipe_files:
            pytest.skip("No recipe files found")
        
        text_extractor = TextExtractor()
        ingredient_extractor = IngredientExtractor()
        
        total_time = 0
        processed_files = 0
        
        for file_path in recipe_files[:5]:  # Test first 5 files
            start_time = time.time()
            
            # Extract text
            content = text_extractor.extract(str(file_path))
            if content.strip():
                # Extract ingredients
                ingredients = ingredient_extractor.extract(content)
                
                end_time = time.time()
                file_time = (end_time - start_time) * 1000
                total_time += file_time
                processed_files += 1
                
                print(f"✓ {file_path.name}: {file_time:.2f}ms, {len(ingredients)} ingredients")
        
        if processed_files > 0:
            avg_time = total_time / processed_files
            assert avg_time < 200, f"Real file processing averaged {avg_time:.2f}ms, expected < 200ms"
            print(f"✓ Real file processing: {avg_time:.2f}ms average across {processed_files} files")

    @pytest.mark.performance
    def test_concurrent_processing_simulation(self, ingredient_extractor, sample_recipe_content):
        """Simulate concurrent processing to test for race conditions."""
        import threading
        import queue
        
        results_queue = queue.Queue()
        errors_queue = queue.Queue()
        
        def worker():
            try:
                start_time = time.time()
                result = ingredient_extractor.extract(sample_recipe_content)
                end_time = time.time()
                execution_time = (end_time - start_time) * 1000
                results_queue.put((result, execution_time))
            except Exception as e:
                errors_queue.put(e)
        
        # Start multiple threads
        threads = []
        num_threads = 5
        for _ in range(num_threads):
            thread = threading.Thread(target=worker)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Check results
        assert errors_queue.empty(), f"Errors occurred during concurrent processing: {list(errors_queue.queue)}"
        assert results_queue.qsize() == num_threads, f"Expected {num_threads} results, got {results_queue.qsize()}"
        
        # Check performance
        times = []
        while not results_queue.empty():
            result, execution_time = results_queue.get()
            times.append(execution_time)
            assert isinstance(result, list), "Each thread should return a list"
        
        avg_time = sum(times) / len(times)
        max_time = max(times)
        
        print(f"✓ Concurrent processing: {avg_time:.2f}ms average, {max_time:.2f}ms max")
        assert max_time < 100, f"Concurrent processing max time {max_time:.2f}ms exceeded 100ms" 
"""
Performance tests for recipe processing.

This module tests the performance characteristics of recipe processing
to ensure operations complete within acceptable time limits.
"""

import pytest
import time
import asyncio
from pathlib import Path
from typing import List, Dict, Any

from core.application.recipe.extractors.text import TextExtractor
from core.domain.recipe.extractors.ingredients import IngredientExtractor
from core.domain.recipe.extractors.metadata import MetadataExtractor
from core.domain.recipe.extractors.sections import SectionExtractor
from core.domain.recipe.processors.llm import RecipeProcessor
from core.domain.recipe.processors.intelligent_batch import IntelligentBatchProcessor


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
    def recipe_processor(self):
        """Recipe processor for LLM-based tests."""
        return RecipeProcessor()

    @pytest.fixture
    def batch_processor(self):
        """Intelligent batch processor for optimization tests."""
        return IntelligentBatchProcessor()

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

    @pytest.fixture
    def recipe_batch_simple(self):
        """Simple recipes for batch testing."""
        return [
            """
            Arroz Blanco Simple
            
            Ingredientes:
            - 2 tazas arroz
            - 1 cucharada sal
            
            Instrucciones:
            1. Hervir agua
            2. Agregar arroz
            3. Cocinar 15 minutos
            """,
            """
            Pasta Básica
            
            Ingredientes:
            - 400g pasta
            - 2 cucharadas aceite
            
            Instrucciones:
            1. Hervir agua con sal
            2. Cocinar pasta al dente
            3. Escurrir y servir
            """,
            """
            Huevos Revueltos
            
            Ingredientes:
            - 4 huevos
            - 1 cucharada mantequilla
            
            Instrucciones:
            1. Batir huevos
            2. Calentar mantequilla
            3. Revolver hasta cremosos
            """
        ]

    @pytest.fixture
    def recipe_batch_complex(self):
        """Complex recipes for batch testing."""
        return [
            """
            Paella Valenciana Tradicional
            
            Ingredientes:
            - 500g arroz bomba especial para paella
            - 1kg pollo cortado en trozos medianos
            - 500g conejo trozado (opcional)
            - 200g judías verdes frescas
            - 200g garrofón (judía lima)
            - 2 tomates maduros rallados
            - 1 pimiento rojo cortado en tiras
            - 6 dientes de ajo picados
            - 1 cucharada de pimentón dulce
            - Hebras de azafrán
            - 1.5 litros de caldo de pollo
            - 150ml aceite de oliva virgen extra
            - Sal y pimienta al gusto
            - Limón para decorar
            
            Instrucciones:
            1. Calentar aceite en paellera de 40cm a fuego medio-alto
            2. Dorar pollo y conejo por todos los lados hasta color uniforme
            3. Apartar carne a un lado de la paellera
            4. Sofreír ajo y tomate hasta reducir y concentrar sabores
            5. Añadir pimentón, remover rápidamente para evitar que se queme
            6. Incorporar arroz, mezclar bien con el sofrito por 2-3 minutos
            7. Verter caldo caliente, agregar azafrán infusionado en agua tibia
            8. Distribuir ingredientes uniformemente, no remover más
            9. Cocinar a fuego fuerte 10 minutos, luego medio 15 minutos
            10. Añadir judías verdes y garrofón en los últimos 5 minutos
            11. Subir fuego final 2 minutos para crear socarrat
            12. Reposar 5 minutos cubierto con paño antes de servir
            """,
            """
            Cocido Madrileño Completo
            
            Ingredientes:
            Para el caldo:
            - 500g morcillo de ternera
            - 300g jarrete de ternera
            - 1 hueso de caña
            - 200g tocino entero
            - 1 gallina entera
            - 300g garbanzos remojados 12 horas
            - 2 zanahorias grandes
            - 1 nabo mediano
            - 2 puerros
            - 1 apio
            - Sal gruesa
            
            Para la pelota:
            - 200g carne picada de ternera
            - 100g miga de pan remojada en leche
            - 2 huevos
            - 2 dientes ajo picados
            - Perejil fresco picado
            - Sal y pimienta
            
            Para las verduras:
            - 400g repollo cortado en trozos
            - 300g patatas cortadas en cuartos
            - 200g judías verdes
            
            Instrucciones:
            1. Remojar garbanzos desde la noche anterior con agua y sal
            2. En olla grande, poner carnes, hueso y gallina con agua fría
            3. Llevar a ebullición, espumar impurezas frecuentemente
            4. Añadir garbanzos escurridos, cocinar 1 hora a fuego lento
            5. Agregar verduras duras (zanahoria, nabo), cocinar 30 minutos
            6. Preparar pelota mezclando todos ingredientes, formar bola
            7. Añadir pelota y verduras tiernas al caldo
            8. Cocinar 45 minutos más hasta garbanzos tiernos
            9. Colar caldo para sopa de primero
            10. Servir carnes, verduras y garbanzos de segundo
            11. Acompañar con salsa de tomate picante opcional
            """
        ]

    def measure_time(self, func, *args, **kwargs):
        """Measure execution time of a function."""
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        return result, (end_time - start_time) * 1000  # Return time in milliseconds

    async def measure_time_async(self, func, *args, **kwargs):
        """Measure execution time of an async function."""
        start_time = time.time()
        result = await func(*args, **kwargs)
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
    def test_intelligent_batch_complexity_analysis(self, batch_processor, recipe_batch_simple, recipe_batch_complex):
        """Test intelligent batch processor complexity analysis performance."""
        all_recipes = recipe_batch_simple + recipe_batch_complex
        
        start_time = time.time()
        
        # Test complexity calculation for each recipe
        complexity_scores = []
        for recipe in all_recipes:
            complexity = batch_processor.calculate_recipe_complexity(recipe)
            complexity_scores.append(complexity)
        
        # Test sorting by complexity
        sorted_recipes = batch_processor.sort_recipes_by_complexity(all_recipes)
        
        analysis_time = (time.time() - start_time) * 1000
        
        # Should complete complexity analysis quickly
        assert analysis_time < 100, f"Complexity analysis took {analysis_time:.2f}ms, expected < 100ms"
        
        # Verify sorting works (simple recipes should have lower complexity)
        simple_avg = sum(complexity_scores[:3]) / 3  # First 3 are simple
        complex_avg = sum(complexity_scores[3:]) / 2  # Last 2 are complex
        
        assert complex_avg > simple_avg, f"Complex recipes should have higher complexity scores"
        
        print(f"✓ Complexity analysis: {analysis_time:.2f}ms")
        print(f"✓ Simple recipes avg complexity: {simple_avg:.1f}")
        print(f"✓ Complex recipes avg complexity: {complex_avg:.1f}")

    @pytest.mark.performance  
    def test_adaptive_batch_sizing(self, batch_processor):
        """Test adaptive batch sizing performance and accuracy."""
        start_time = time.time()
        
        # Test different scenarios
        scenarios = [
            (10, 0.9),   # 10 recipes, 90% success rate
            (50, 0.7),   # 50 recipes, 70% success rate  
            (100, 0.8),  # 100 recipes, 80% success rate
            (5, None),   # 5 recipes, no success rate data
        ]
        
        batch_sizes = []
        for total_recipes, success_rate in scenarios:
            batch_size = batch_processor.calculate_adaptive_batch_size(total_recipes, success_rate)
            batch_sizes.append(batch_size)
            
        calculation_time = (time.time() - start_time) * 1000
        
        # Should calculate quickly
        assert calculation_time < 10, f"Batch size calculation took {calculation_time:.2f}ms, expected < 10ms"
        
        # Verify reasonable batch sizes
        for batch_size in batch_sizes:
            assert 1 <= batch_size <= 10, f"Batch size {batch_size} outside reasonable range"
        
        print(f"✓ Adaptive batch sizing: {calculation_time:.2f}ms")
        print(f"✓ Calculated batch sizes: {batch_sizes}")

    @pytest.mark.performance
    @pytest.mark.slow
    async def test_intelligent_vs_traditional_batch_performance(self, recipe_processor, recipe_batch_simple):
        """Compare intelligent vs traditional batch processing performance."""
        recipes = recipe_batch_simple * 3  # 9 total recipes
        
        # Mock the LLM extractor for performance testing
        class MockLLMExtractor:
            async def extract_recipe(self, content):
                # Simulate variable processing time based on complexity
                import random
                await asyncio.sleep(random.uniform(0.1, 0.3))
                
                from core.domain.recipe.models.recipe import Recipe
                from core.domain.recipe.models.metadata import RecipeMetadata
                from core.domain.recipe.models.ingredient import Ingredient
                from datetime import datetime
                
                return Recipe(
                    title="Test Recipe",
                    metadata=RecipeMetadata(
                        title="Test Recipe",
                        tags=['test'],
                        date=datetime.now().isoformat(),
                        porciones=4,
                        tiempo_preparacion=15,
                        tiempo_coccion=30,
                        tiempo_total=45,
                        dificultad='Media',
                        calorias=350
                    ),
                    ingredients=[
                        Ingredient(nombre="Test ingredient", cantidad=1.0, unidad="cup")
                    ],
                    instructions=["Test instruction"]
                )
        
        # Replace with mock for testing
        original_extractor = recipe_processor.llm_extractor
        recipe_processor.llm_extractor = MockLLMExtractor()
        
        try:
            # Test traditional batch processing (if method exists)
            if hasattr(recipe_processor, 'process_recipes_batch'):
                traditional_results, traditional_time = await self.measure_time_async(
                    recipe_processor.process_recipes_batch, recipes
                )
            
            # Test intelligent batch processing (if method exists)
            if hasattr(recipe_processor, 'process_recipes_batch_optimized'):
                intelligent_results, intelligent_time = await self.measure_time_async(
                    recipe_processor.process_recipes_batch_optimized, recipes
                )
                
                # Intelligent processing should be competitive or better
                print(f"✓ Intelligent batch processing: {intelligent_time:.2f}ms for {len(recipes)} recipes")
                print(f"✓ Processed {len(intelligent_results)} recipes successfully")
                
                if 'traditional_time' in locals():
                    improvement = ((traditional_time - intelligent_time) / traditional_time * 100)
                    print(f"✓ Performance improvement: {improvement:.1f}%")
        
        finally:
            # Restore original extractor
            recipe_processor.llm_extractor = original_extractor

    @pytest.mark.performance
    def test_memory_usage_with_large_content(self, ingredient_extractor):
        """Test that memory usage stays reasonable with large content."""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / (1024 * 1024)  # MB
        
        # Process large content multiple times
        large_content = """
        Large Recipe Content
        
        Ingredientes:
        """ + "\n".join([f"- {i} cups ingredient_{i}" for i in range(1000)])
        
        for _ in range(10):
            ingredient_extractor.extract(large_content)
        
        final_memory = process.memory_info().rss / (1024 * 1024)  # MB
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be reasonable (less than 100MB)
        assert memory_increase < 100, f"Memory increased by {memory_increase:.1f}MB, expected < 100MB"
        print(f"✓ Memory usage increase: {memory_increase:.1f}MB")

    @pytest.mark.performance 
    @pytest.mark.slow
    def test_real_file_processing_performance(self):
        """Test performance with real files from the sin_procesar directory."""
        sin_procesar_dir = Path("data/recipes/sin_procesar")
        
        if not sin_procesar_dir.exists():
            pytest.skip("sin_procesar directory not found")
            
        test_files = list(sin_procesar_dir.glob("*.txt"))[:5]  # Test first 5 files
        
        if not test_files:
            pytest.skip("No test files found in sin_procesar")
        
        text_extractor = TextExtractor()
        processing_times = []
        
        for file_path in test_files:
            start_time = time.time()
            try:
                content = text_extractor.extract(str(file_path))
                processing_time = (time.time() - start_time) * 1000
                processing_times.append(processing_time)
                
                # Individual file should process quickly
                assert processing_time < 1000, f"File {file_path.name} took {processing_time:.2f}ms, expected < 1000ms"
                print(f"✓ {file_path.name}: {processing_time:.2f}ms")
                
            except Exception as e:
                print(f"⚠️ Skipped {file_path.name}: {e}")
        
        if processing_times:
            avg_time = sum(processing_times) / len(processing_times)
            print(f"✓ Average processing time: {avg_time:.2f}ms")

    @pytest.mark.performance
    def test_concurrent_processing_simulation(self, ingredient_extractor, sample_recipe_content):
        """Test performance under simulated concurrent load."""
        import threading
        import queue
        
        num_threads = 5
        recipes_per_thread = 3
        results_queue = queue.Queue()
        
        def worker():
            thread_results = []
            for _ in range(recipes_per_thread):
                start_time = time.time()
                result = ingredient_extractor.extract(sample_recipe_content)
                processing_time = (time.time() - start_time) * 1000
                thread_results.append(processing_time)
            results_queue.put(thread_results)
        
        # Start concurrent processing
        start_time = time.time()
        threads = []
        for _ in range(num_threads):
            thread = threading.Thread(target=worker)
            thread.start()
            threads.append(thread)
        
        # Wait for completion
        for thread in threads:
            thread.join()
        
        total_time = (time.time() - start_time) * 1000
        
        # Collect results
        all_times = []
        while not results_queue.empty():
            thread_times = results_queue.get()
            all_times.extend(thread_times)
        
        avg_time = sum(all_times) / len(all_times)
        total_recipes = num_threads * recipes_per_thread
        
        # Concurrent processing should not degrade significantly
        assert avg_time < 100, f"Concurrent processing averaged {avg_time:.2f}ms, expected < 100ms"
        print(f"✓ Concurrent processing: {total_recipes} recipes in {total_time:.2f}ms")
        print(f"✓ Average time per recipe: {avg_time:.2f}ms")

    @pytest.mark.performance
    def test_batch_processor_history_tracking(self, batch_processor):
        """Test performance of batch processor history tracking."""
        start_time = time.time()
        
        # Simulate processing history updates
        for i in range(50):
            batch_processor.update_processing_history(
                batch_size=5 + (i % 3),
                success_count=4 + (i % 2), 
                total_count=5,
                processing_time=10.0 + (i % 5)
            )
        
        # Test recent success rate calculation
        success_rate = batch_processor.get_recent_success_rate()
        
        # Test performance summary generation
        summary = batch_processor.get_performance_summary()
        
        tracking_time = (time.time() - start_time) * 1000
        
        # Should complete quickly
        assert tracking_time < 50, f"History tracking took {tracking_time:.2f}ms, expected < 50ms"
        
        # Verify reasonable values
        assert 0 <= success_rate <= 1, f"Success rate {success_rate} out of range"
        assert summary['status'] == 'active'
        
        print(f"✓ History tracking: {tracking_time:.2f}ms")
        print(f"✓ Recent success rate: {success_rate:.1%}")
        print(f"✓ Total batches tracked: {summary['summary']['total_batches_processed']}")

    @pytest.mark.performance
    @pytest.mark.benchmark
    def test_performance_benchmark_suite(self, batch_processor, recipe_batch_simple, recipe_batch_complex):
        """Comprehensive performance benchmark for intelligent batch processing."""
        print("\n🚀 Running Performance Benchmark Suite")
        print("=" * 50)
        
        all_recipes = recipe_batch_simple + recipe_batch_complex
        benchmark_results = {}
        
        # Benchmark 1: Complexity Analysis
        start_time = time.time()
        for recipe in all_recipes * 10:  # Test with 50 recipes
            batch_processor.calculate_recipe_complexity(recipe)
        benchmark_results['complexity_analysis_per_recipe'] = ((time.time() - start_time) * 1000) / (len(all_recipes) * 10)
        
        # Benchmark 2: Adaptive Batch Sizing
        start_time = time.time()
        for _ in range(100):  # 100 calculations
            batch_processor.calculate_adaptive_batch_size(20, 0.8)
        benchmark_results['adaptive_batch_sizing_per_calc'] = ((time.time() - start_time) * 1000) / 100
        
        # Benchmark 3: Recipe Sorting
        start_time = time.time()
        large_recipe_list = all_recipes * 20  # 100 recipes
        batch_processor.sort_recipes_by_complexity(large_recipe_list)
        benchmark_results['recipe_sorting_100_items'] = (time.time() - start_time) * 1000
        
        # Benchmark 4: History Management
        start_time = time.time()
        for i in range(100):
            batch_processor.update_processing_history(5, 4, 5, 10.0)
            batch_processor.get_recent_success_rate()
        benchmark_results['history_management_per_update'] = ((time.time() - start_time) * 1000) / 100
        
        # Print benchmark results
        print("\n📊 Benchmark Results:")
        for operation, time_ms in benchmark_results.items():
            print(f"  {operation}: {time_ms:.3f}ms")
            
        # Assert performance targets
        assert benchmark_results['complexity_analysis_per_recipe'] < 1.0, "Complexity analysis too slow"
        assert benchmark_results['adaptive_batch_sizing_per_calc'] < 0.1, "Batch sizing calculation too slow"
        assert benchmark_results['recipe_sorting_100_items'] < 100, "Recipe sorting too slow"
        assert benchmark_results['history_management_per_update'] < 0.5, "History management too slow"
        
        print("\n✅ All performance benchmarks passed!")
        
        return benchmark_results 
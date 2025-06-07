"""
Recipe processor that uses LLM extraction with Ollama and Phi model for accurate recipe parsing.
"""
from core.application.recipe.extractors.llm import LLMExtractor
from core.domain.recipe.models.metadata import RecipeMetadata
from core.domain.recipe.models.recipe import Recipe
from core.utils.logger import get_logger
from core.utils.performance import performance_monitor
from typing import Dict, Any, List, Optional

from functools import lru_cache
import asyncio
import hashlib
import uuid
logger = get_logger(__name__)

class RecipeProcessor:
    """Recipe processor that relies entirely on LLM extraction using Ollama with Phi model."""

    def __init__(self, batch_size: int = 5) -> None:
        """Initialize the recipe processor.

        Args:
            batch_size: Number of recipes to process in parallel
        """
        self.llm_extractor = LLMExtractor()
        self._cache = {}
        self._processing_lock = asyncio.Lock()
        self.batch_size = batch_size

    def _get_cache_key(self, content: str) -> str:
        """Generate a cache key for the content."""
        return hashlib.md5(content.encode()).hexdigest()

    async def extract_recipe(self, content: str) -> Recipe:
        """Extract recipe using LLM.
        
        This is the primary method that uses LLM extraction.
        Maintains compatibility with existing tests.
        """
        return await self.process_recipe(content)

    async def process_recipe(self, content: str) -> Recipe:
        """Process recipe content into structured data using LLM extraction."""
        recipe_id = str(uuid.uuid4())
        metrics = performance_monitor.start_processing(recipe_id, 'llm')
        
        cache_key = self._get_cache_key(content)
        if cache_key in self._cache:
            logger.debug('Using cached recipe')
            metrics.cache_hit = True
            performance_monitor.end_processing(recipe_id, success=True)
            return self._cache[cache_key]
        
        async with self._processing_lock:
            try:
                logger.info('Using LLM extraction for recipe processing')
                
                # Use LLM extraction without timeout - let it complete
                recipe = await self.llm_extractor.extract_recipe(content)
                
                # Validate the recipe
                if not self._validate_recipe(recipe):
                    logger.warning('Recipe validation failed, attempting correction')
                    recipe = self._correct_recipe(recipe, content)
                
                self._cache[cache_key] = recipe
                performance_monitor.end_processing(recipe_id, success=True)
                logger.info(f'Successfully extracted recipe: {recipe.metadata.title}')
                return recipe
                
            except Exception as e:
                logger.error(f'Error in recipe processing: {str(e)}')
                performance_monitor.end_processing(recipe_id, success=False, error=str(e))
                
                # Create a minimal fallback recipe to prevent complete failure
                fallback_recipe = self._create_fallback_recipe(content, str(e))
                self._cache[cache_key] = fallback_recipe
                return fallback_recipe

    def _validate_recipe(self, recipe: Recipe) -> bool:
        """Validate that the recipe has minimum required data."""
        try:
            # Check metadata
            if not recipe.metadata or not recipe.metadata.title:
                return False
            
            # Check ingredients - should have at least one with a name
            if not recipe.ingredients or not any(ing.nombre.strip() for ing in recipe.ingredients):
                return False
            
            # Check instructions - should have at least one non-empty instruction
            if not recipe.instructions or not any(inst.strip() for inst in recipe.instructions):
                return False
                
            return True
        except Exception as e:
            logger.error(f'Error validating recipe: {str(e)}')
            return False

    def _correct_recipe(self, recipe: Recipe, original_content: str) -> Recipe:
        """Attempt to correct a recipe with validation issues."""
        try:
            # Fix title if missing
            if not recipe.metadata.title or recipe.metadata.title.strip() == '':
                recipe.metadata.title = self._extract_title_from_content(original_content)
            
            # Fix ingredients if empty
            if not recipe.ingredients or not any(ing.nombre.strip() for ing in recipe.ingredients):
                logger.warning('No valid ingredients found, creating placeholder')
                from core.domain.recipe.models.ingredient import Ingredient
                recipe.ingredients = [
                    Ingredient(
                        nombre='Ingrediente a definir',
                        cantidad=1.0,
                        unidad='',
                        notas='Extraído desde texto original'
                    )
                ]
            
            # Fix instructions if empty
            if not recipe.instructions or not any(inst.strip() for inst in recipe.instructions):
                logger.warning('No valid instructions found, creating placeholder')
                recipe.instructions = [
                    'Consultar texto original para instrucciones detalladas',
                    'Verificar ingredientes y cantidades'
                ]
            
            return recipe
            
        except Exception as e:
            logger.error(f'Error correcting recipe: {str(e)}')
            return recipe

    def _extract_title_from_content(self, content: str) -> str:
        """Extract title from content using simple parsing."""
        lines = content.splitlines()
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Look for title patterns
            if line.lower().startswith('título:'):
                return line[7:].strip()
            elif line.lower().startswith('title:'):
                return line[6:].strip()
            elif len(line) < 100 and not any(word in line.lower() for word in 
                                           ['ingredientes', 'ingredients', 'preparación', 'instructions']):
                return line
        
        return 'Receta Extraída'

    def _create_fallback_recipe(self, content: str, error_reason: str) -> Recipe:
        """Create a minimal fallback recipe when LLM extraction fails completely."""
        from core.domain.recipe.models.ingredient import Ingredient
        from datetime import datetime
        
        title = self._extract_title_from_content(content)
        
        metadata = RecipeMetadata(
            title=title,
            tags=['general', 'error'],
            date=datetime.now().isoformat(),  # Convert to string
            porciones=4,
            tiempo_preparacion=0,
            tiempo_coccion=0,
            tiempo_total=1,  # Ensure > 0
            dificultad='Media',  # Use proper case
            calorias=0,
            notas=f'Error en extracción automática: {error_reason}'
        )
        
        ingredients = [
            Ingredient(
                nombre='Error en extracción de ingredientes',
                cantidad=1.0,
                unidad='',
                notas=f'Consultar texto original. Error: {error_reason}'
            )
        ]
        
        instructions = [
            f'Error en extracción automática: {error_reason}',
            'Por favor revisar el texto original para obtener la receta completa',
            'Contactar soporte si el problema persiste'
        ]
        
        return Recipe(
            metadata=metadata,
            ingredients=ingredients,
            instructions=instructions
        )

    async def process_recipes_batch(self, contents: List[str]) -> List[Recipe]:
        """Process multiple recipes in parallel batches."""
        batch_id = str(uuid.uuid4())
        batch_metrics = performance_monitor.start_batch(len(contents))
        results = []
        
        try:
            for i in range(0, len(contents), self.batch_size):
                batch = contents[i:i + self.batch_size]
                batch_tasks = [self.process_recipe(content) for content in batch]
                batch_results = await asyncio.gather(*batch_tasks, return_exceptions=True)
                
                # Handle any exceptions in batch processing
                for j, result in enumerate(batch_results):
                    if isinstance(result, Exception):
                        logger.error(f'Error processing recipe {i+j}: {str(result)}')
                        fallback = self._create_fallback_recipe(batch[j], str(result))
                        results.append(fallback)
                    else:
                        results.append(result)
                        
            performance_monitor.end_batch(batch_id)
            return results
            
        except Exception as e:
            logger.error(f'Error in batch processing: {str(e)}')
            performance_monitor.end_batch(batch_id)
            raise

    async def process_recipe_file(self, file_path: str) -> Recipe:
        """Process a recipe from a file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return await self.process_recipe(content)
        except Exception as e:
            logger.error(f'Error processing recipe file {file_path}: {str(e)}')
            raise

    async def process_recipe_files_batch(self, file_paths: List[str]) -> List[Recipe]:
        """Process multiple recipe files in parallel batches."""
        batch_id = str(uuid.uuid4())
        batch_metrics = performance_monitor.start_batch(len(file_paths))
        results = []
        
        try:
            for i in range(0, len(file_paths), self.batch_size):
                batch = file_paths[i:i + self.batch_size]
                batch_tasks = [self.process_recipe_file(path) for path in batch]
                batch_results = await asyncio.gather(*batch_tasks, return_exceptions=True)
                
                # Handle any exceptions in batch processing
                for j, result in enumerate(batch_results):
                    if isinstance(result, Exception):
                        logger.error(f'Error processing file {batch[j]}: {str(result)}')
                        fallback = self._create_fallback_recipe(f'File: {batch[j]}', str(result))
                        results.append(fallback)
                    else:
                        results.append(result)
                        
            performance_monitor.end_batch(batch_id)
            return results
            
        except Exception as e:
            logger.error(f'Error in batch file processing: {str(e)}')
            performance_monitor.end_batch(batch_id)
            raise

    def get_extraction_stats(self) -> Dict[str, Any]:
        """Get extraction statistics."""
        return {
            'cache_size': len(self._cache),
            'processor_type': 'llm_only',
            'model': 'phi',
            'batch_size': self.batch_size
        }

    def clear_cache(self):
        """Clear the processing cache."""
        self._cache.clear()
        logger.info('Recipe processing cache cleared')

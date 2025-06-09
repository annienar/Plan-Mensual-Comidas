"""
Recipe processor using LLM integration with Ollama and Phi model.

This module contains the recipe processor implementation that uses
LLM-based extraction for accurate recipe parsing.
"""

import logging
from datetime import datetime
from typing import List, Optional, Dict, Any, Union
import asyncio

from pydantic import BaseModel, Field, field_validator

from core.domain.exceptions.recipe import (
    RecipeError, 
    RecipeValidationError, 
    RecipeGenerationError, 
    RecipeExtractionError
)
from core.domain.recipe.models.ingredient import Ingredient
from core.domain.recipe.models.metadata import RecipeMetadata
from core.domain.recipe.models.recipe import Recipe
from core.domain.recipe.processors.llm import RecipeProcessor as LLMRecipeProcessor
from .generators.recipe_generator import RecipeGenerator

logger = logging.getLogger(__name__)

class RecipeProcessor:
    """Recipe processor using LLM integration.

    This class handles recipe processing using LLM-based extraction
    with Ollama and the Phi model for accurate recipe parsing.
    """

    def __init__(self, llm_client=None):
        """Initialize the processor.
        
        Args:
            llm_client: Optional LLM client (for backward compatibility)
        """
        self.generator = RecipeGenerator()
        self.llm_processor = LLMRecipeProcessor(batch_size=5)

    def validate_recipe(self, recipe: Recipe) -> bool:
        """Validate a recipe.

        Args:
            recipe: Recipe to validate

        Returns:
            bool: True if valid, False otherwise

        Raises:
            RecipeValidationError: If validation fails
        """
        try:
            # Validate title
            if not recipe.metadata.title:
                raise RecipeValidationError("Title is required")

            # Validate ingredients
            if not recipe.ingredients:
                raise RecipeValidationError("At least one ingredient is required")

            for ingredient in recipe.ingredients:
                if not ingredient.nombre:
                    raise RecipeValidationError("Ingredient name is required")
                if ingredient.cantidad <= 0:
                    raise RecipeValidationError("Ingredient quantity must be positive")

            # Validate instructions
            if not recipe.instructions:
                raise RecipeValidationError("At least one instruction is required")

            for instruction in recipe.instructions:
                if not instruction:
                    raise RecipeValidationError("Instruction cannot be empty")

            # Validate metadata
            if recipe.metadata.porciones is not None and recipe.metadata.porciones <= 0:
                raise RecipeValidationError("Portions must be positive")

            if recipe.metadata.calorias is not None and recipe.metadata.calorias < 0:
                raise RecipeValidationError("Calories cannot be negative")

            if recipe.metadata.tiempo_preparacion is not None and recipe.metadata.tiempo_preparacion < 0:
                raise RecipeValidationError("Preparation time cannot be negative")

            if recipe.metadata.tiempo_coccion is not None and recipe.metadata.tiempo_coccion < 0:
                raise RecipeValidationError("Cooking time cannot be negative")

            if recipe.metadata.dificultad is not None and recipe.metadata.dificultad not in ["Fácil", "Media", "Difícil"]:
                raise RecipeValidationError("Invalid difficulty level")

            return True

        except RecipeValidationError as e:
            logger.error(f"Recipe validation failed: {str(e)}")
            raise

        except Exception as e:
            logger.error(f"Unexpected error during recipe validation: {str(e)}")
            raise RecipeValidationError(f"Unexpected error: {str(e)}")

    async def process_recipe(self, recipe_input: Union[str, Recipe]) -> Union[Recipe, Dict[str, Any]]:
        """Process a recipe.

        Args:
            recipe_input: Recipe object to process OR text to extract and process

        Returns:
            Recipe: If input is text (extracted recipe)
            Dict[str, Any]: If input is Recipe object (processed in different formats)

        Raises:
            RecipeError: If processing fails
        """
        try:
            # Handle both text input and Recipe object input for backward compatibility
            if isinstance(recipe_input, str):
                # Extract recipe from text and return the Recipe object
                return await self.llm_processor.extract_recipe(recipe_input)
            else:
                # Process Recipe object and return different formats
                recipe = recipe_input
                self.validate_recipe(recipe)

                # Generate different formats
                return {
                    "markdown": self.generator.to_markdown(recipe), 
                    "html": self.generator.to_html(recipe), 
                    "json": self.generator.to_json(recipe), 
                    "yaml": self.generator.to_yaml(recipe), 
                    "notion_blocks": self.generator.to_notion_blocks(recipe)
                }

        except RecipeError as e:
            logger.error(f"Recipe processing failed: {str(e)}")
            raise

        except Exception as e:
            logger.error(f"Unexpected error during recipe processing: {str(e)}")
            raise RecipeError(f"Unexpected error: {str(e)}")

    def extract_recipe(self, text: str) -> Recipe:
        """Extract a recipe from text using LLM.

        Args:
            text: Text to extract from

        Returns:
            Recipe: Extracted recipe

        Raises:
            RecipeExtractionError: If extraction fails
        """
        try:
            # Use async LLM processor in sync context
            loop = None
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            
            if loop.is_running():
                # If we're already in an async context, create a new task
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(
                        lambda: asyncio.run(self.llm_processor.extract_recipe(text))
                    )
                    return future.result(timeout=180)  # 3 minute timeout
            else:
                # Run directly
                return loop.run_until_complete(self.llm_processor.extract_recipe(text))

        except RecipeExtractionError as e:
            logger.error(f"Recipe extraction failed: {str(e)}")
            raise

        except Exception as e:
            logger.error(f"Unexpected error during recipe extraction: {str(e)}")
            raise RecipeExtractionError(f"Unexpected error: {str(e)}")

    def process_text(self, text: str) -> Dict[str, Any]:
        """Process text into a recipe.

        Args:
            text: Text to process

        Returns:
            Dict[str, Any]: Processed recipe in different formats

        Raises:
            RecipeError: If processing fails
        """
        try:
            # Extract recipe using LLM
            recipe = self.extract_recipe(text)

            # Process recipe
            return self.process_recipe(recipe)

        except RecipeError as e:
            logger.error(f"Text processing failed: {str(e)}")
            raise

        except Exception as e:
            logger.error(f"Unexpected error during text processing: {str(e)}")
            raise RecipeError(f"Unexpected error: {str(e)}")

    # Additional methods for compatibility
    def get_extraction_stats(self) -> Dict[str, Any]:
        """Get extraction statistics from the LLM processor."""
        return self.llm_processor.get_extraction_stats()

    def clear_cache(self):
        """Clear the processing cache."""
        self.llm_processor.clear_cache()

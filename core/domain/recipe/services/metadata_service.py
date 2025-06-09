"""
Metadata service.

This module contains the metadata domain service.
"""

from ...exceptions.recipe import RecipeValidationError
from datetime import timedelta
from typing import List, Optional

from ..models.metadata import RecipeMetadata

class MetadataService:
    """Metadata service.

    This service handles metadata - related business logic.
    """

    @staticmethod
    def calculate_total_time(metadata: RecipeMetadata) -> int:
        """Calculate total recipe time.

        Args:
            metadata: Recipe metadata

        Returns:
            int: Total time in minutes
        """
        return metadata.tiempo_preparacion + metadata.tiempo_coccion

    @staticmethod
    def format_time(minutes: int) -> str:
        """Format time in minutes to human - readable format.

        Args:
            minutes: Time in minutes

        Returns:
            str: Formatted time
        """
        if minutes < 60:
            return f"{minutes} min"

        hours = minutes // 60
        remaining_minutes = minutes % 60

        if remaining_minutes == 0:
            return f"{hours} h"

        return f"{hours} h {remaining_minutes} min"

    @staticmethod
    def calculate_calories_per_portion(metadata: RecipeMetadata) -> float:
        """Calculate calories per portion.

        Args:
            metadata: Recipe metadata

        Returns:
            float: Calories per portion
        """
        return metadata.calorias / metadata.porciones

    @staticmethod
    def scale_metadata(metadata: RecipeMetadata, factor: float) -> RecipeMetadata:
        """Scale recipe metadata.

        Args:
            metadata: Recipe metadata
            factor: Scaling factor

        Returns:
            RecipeMetadata: Scaled metadata

        Raises:
            RecipeValidationError: If factor is invalid
        """
        if factor <= 0:
            raise RecipeValidationError("Scaling factor must be positive")

        # Scale portions and calories
        scaled_porciones = max(1, round(metadata.porciones * factor))
        scaled_calorias = round(metadata.calorias * factor)

        # Create scaled metadata
        return RecipeMetadata(
            porciones = scaled_porciones, 
            calorias = scaled_calorias, 
            tiempo_preparacion = metadata.tiempo_preparacion, 
            tiempo_coccion = metadata.tiempo_coccion, 
            dificultad = metadata.dificultad, 
            tags = metadata.tags
)

    @staticmethod
    def suggest_tags(metadata: RecipeMetadata) -> List[str]:
        """Suggest additional tags based on metadata.

        Args:
            metadata: Recipe metadata

        Returns:
            List[str]: Suggested tags
        """
        tags = set(metadata.tags)

        # Add difficulty tag
        tags.add(metadata.dificultad)

        # Add time tags
        total_time = MetadataService.calculate_total_time(metadata)
        if total_time <= 30:
            tags.add("Rapido")
        elif total_time <= 60:
            tags.add("Medio")
        else:
            tags.add("Lento")

        # Add portion tags
        if metadata.porciones <= 2:
            tags.add("Para 2")
        elif metadata.porciones <= 4:
            tags.add("Para 4")
        else:
            tags.add("Para muchos")

        # Add calorie tags
        calories_per_portion = MetadataService.calculate_calories_per_portion(metadata)
        if calories_per_portion <= 300:
            tags.add("Bajo en calorias")
        elif calories_per_portion <= 600:
            tags.add("Medio en calorias")
        else:
            tags.add("Alto en calorias")

        return sorted(list(tags))

"""
Meal plan metadata service.

This module contains the meal plan metadata domain service.
"""

from datetime import datetime, timedelta
from typing import List, Optional

from ...exceptions.meal_plan import MealPlanValidationError
from ..models.metadata import MealPlanMetadata

class MetadataService:
    """Meal plan metadata service.

    This service handles meal plan metadata - related business logic.
    """

    @staticmethod
    def calculate_duration(metadata: MealPlanMetadata) -> int:
        """Calculate meal plan duration in days.

        Args:
            metadata: Meal plan metadata

        Returns:
            int: Duration in days
        """
        start_date = datetime.strptime(metadata.start_date, "%Y-%m-%d")
        end_date = datetime.strptime(metadata.end_date, "%Y-%m-%d")

        return (end_date - start_date).days + 1

    @staticmethod
    def get_dates(metadata: MealPlanMetadata) -> List[str]:
        """Get all dates in meal plan.

        Args:
            metadata: Meal plan metadata

        Returns:
            List[str]: List of dates in YYYY - MM - DD format
        """
        start_date = datetime.strptime(metadata.start_date, "%Y-%m-%d")
        end_date = datetime.strptime(metadata.end_date, "%Y-%m-%d")

        dates = []
        current_date = start_date

        while current_date <= end_date:
            dates.append(current_date.strftime("%Y-%m-%d"))
            current_date += timedelta(days = 1)

        return dates

    @staticmethod
    def suggest_tags(metadata: MealPlanMetadata) -> List[str]:
        """Suggest additional tags based on metadata.

        Args:
            metadata: Meal plan metadata

        Returns:
            List[str]: Suggested tags
        """
        tags = set(metadata.tags)

        # Add duration tag
        duration = MetadataService.calculate_duration(metadata)
        if duration <= 7:
            tags.add("Semanal")
        elif duration <= 14:
            tags.add("Quincenal")
        else:
            tags.add("Mensual")

        # Add season tag based on start date
        start_date = datetime.strptime(metadata.start_date, "%Y-%m-%d")
        month = start_date.month

        if month in [12, 1, 2]:
            tags.add("Invierno")
        elif month in [3, 4, 5]:
            tags.add("Primavera")
        elif month in [6, 7, 8]:
            tags.add("Verano")
        else:
            tags.add("Otoño")

        return sorted(list(tags))

    @staticmethod
    def format_metadata(metadata: MealPlanMetadata) -> str:
        """Format metadata as text.

        Args:
            metadata: Meal plan metadata

        Returns:
            str: Formatted metadata
        """
        # Format title
        lines = [f"# {metadata.title}", ""]

        # Format dates
        duration = MetadataService.calculate_duration(metadata)
        lines.extend([
            "## Fechas", 
            f"- Inicio: {metadata.start_date}", 
            f"- Fin: {metadata.end_date}", 
            f"- Duración: {duration} días", 
            ""
        ])

        # Format tags
        if metadata.tags:
            lines.extend([
                "## Tags", 
                *[f"- {tag}" for tag in metadata.tags], 
                ""
            ])

        # Format notes
        if metadata.notas:
            lines.extend([
                "## Notas", 
                metadata.notas, 
                ""
            ])

        return "\n".join(lines)

    @staticmethod
    def validate_metadata(metadata: MealPlanMetadata) -> None:
        """Validate meal plan metadata.

        Args:
            metadata: Meal plan metadata

        Raises:
            MealPlanValidationError: If metadata is invalid
        """
        # Validate title
        if not metadata.title:
            raise MealPlanValidationError("Meal plan title is required")

        # Validate dates
        try:
            start_date = datetime.strptime(metadata.start_date, "%Y-%m-%d")
            end_date = datetime.strptime(metadata.end_date, "%Y-%m-%d")
        except ValueError:
            raise MealPlanValidationError("Invalid date format. Must be YYYY - MM - DD")

        if end_date < start_date:
            raise MealPlanValidationError("End date must be after start date")

        # Validate tags
        for tag in metadata.tags:
            if not tag:
                raise MealPlanValidationError("Empty tag found")

        # Validate notes
        if metadata.notas is not None and not metadata.notas:
            raise MealPlanValidationError("Notes cannot be empty")

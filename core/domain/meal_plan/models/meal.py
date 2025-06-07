"""
Meal model.

This module contains the meal domain model.
"""

from ...recipe.models.recipe import Recipe
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator

class Meal(BaseModel):
    """Meal domain model.

    This class represents a meal in the domain.
    """

    title: str = Field(
        ..., 
        min_length = 3, 
        max_length = 200, 
        description="Título de la comida"
)
    type: str = Field(
        ..., 
        pattern='^(Desayuno|Almuerzo|Cena|Snack)$', 
        description="Tipo de comida"
)
    time: str = Field(
        ..., 
        pattern = r'^([01]\d|2[0 - 3]):([0 - 5]\d)$', 
        description="Hora de la comida en formato HH:MM"
)
    date: str = Field(
        ..., 
        pattern = r'^\d{4}-\d{2}-\d{2}$', 
        description="Fecha de la comida en formato YYYY - MM - DD"
)
    recipes: List[Recipe] = Field(
        ..., 
        min_items = 1, 
        description="Lista de recetas"
)
    notes: Optional[str] = Field(
        None, 
        description="Notas adicionales"
)

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        """Validate meal title.

        Args:
            v: Title to validate

        Returns:
            str: Validated title

        Raises:
            ValueError: If title is invalid
        """
        # Remove extra whitespace
        v = " ".join(v.split())

        # Convert to title case
        v = v.title()

        return v

    @field_validator("type")
    @classmethod
    def validate_type(cls, v: str) -> str:
        """Validate meal type.

        Args:
            v: Type to validate

        Returns:
            str: Validated type

        Raises:
            ValueError: If type is invalid
        """
        valid_types = ["Desayuno", "Almuerzo", "Cena", "Snack"]

        if v not in valid_types:
            raise ValueError(f"Invalid meal type: {v}. Must be one of {valid_types}")

        return v

    @field_validator("time")
    @classmethod
    def validate_time(cls, v: str) -> str:
        """Validate meal time.

        Args:
            v: Time to validate

        Returns:
            str: Validated time

        Raises:
            ValueError: If time is invalid
        """
        try:
            datetime.strptime(v, "%H:%M")
        except ValueError:
            raise ValueError(f"Invalid time format: {v}. Must be HH:MM")

        return v

    @field_validator("date")
    @classmethod
    def validate_date(cls, v: str) -> str:
        """Validate meal date.

        Args:
            v: Date to validate

        Returns:
            str: Validated date

        Raises:
            ValueError: If date is invalid
        """
        try:
            datetime.strptime(v, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"Invalid date format: {v}. Must be YYYY - MM - DD")

        return v

    @field_validator('recipes')
    @classmethod
    def validate_recipes(cls, v: List[Recipe]) -> List[Recipe]:
        """Validate recipes.

        Args:
            v: Recipes to validate

        Returns:
            List[Recipe]: Validated recipes

        Raises:
            ValueError: If recipes are invalid
        """
        # Check for duplicate recipes
        titles = [recipe.title for recipe in v]
        if len(titles) != len(set(titles)):
            raise ValueError("Duplicate recipes found")

        return v

    def __str__(self) -> str:
        """Get string representation.

        Returns:
            str: String representation
        """
        return (
            f"Meal(type='{self.type}', "
            f"date='{self.date}', "
            f"time='{self.time}', "
            f"recipes={[r.title for r in self.recipes]})"
)

    def __repr__(self) -> str:
        """Get string representation.

        Returns:
            str: String representation
        """
        return self.__str__()

    def __eq__(self, other: object) -> bool:
        """Check equality.

        Args:
            other: Object to compare with

        Returns:
            bool: True if equal, False otherwise
        """
        if not isinstance(other, Meal):
            return False

        return (
            self.type == other.type and
            self.date == other.date and
            self.time == other.time and
            self.recipes == other.recipes
)

    def __hash__(self) -> int:
        """Get hash.

        Returns:
            int: Hash value
        """
        return hash((
            self.type, 
            self.date, 
            self.time, 
            tuple(self.recipes)
))

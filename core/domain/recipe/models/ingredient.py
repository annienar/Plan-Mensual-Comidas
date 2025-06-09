"""
Ingredient model.

This module contains the ingredient domain model.
"""

from typing import Optional, List
from fractions import Fraction
from pydantic import BaseModel, Field, field_validator

class Ingredient(BaseModel):
    """Ingredient domain model.

    This class represents an ingredient in the domain.
    """

    nombre: str = Field(
        ..., 
        min_length = 1, 
        max_length = 100, 
        description="Nombre del ingrediente"
)
    cantidad: float = Field(
        ..., 
        ge = 0, 
        description="Cantidad del ingrediente"
)
    unidad: Optional[str] = Field(
        None, 
        min_length = 1, 
        max_length = 20, 
        description="Unidad de medida del ingrediente"
)
    notas: Optional[str] = Field(
        None, 
        description="Notas adicionales sobre el ingrediente"
)
    alternativas: List[str] = Field(
        default_factory = list, 
        description="Ingredientes alternativos"
)

    @field_validator('nombre')
    @classmethod
    def validate_nombre(cls, v: str) -> str:
        """Validate name.

        Args:
            v: Name to validate

        Returns:
            str: Validated name

        Raises:
            ValueError: If name is invalid
        """
        # Remove extra whitespace
        v = ' '.join(v.split())

        # Keep original casing - don't auto-capitalize
        return v

    @field_validator('unidad')
    @classmethod
    def validate_unidad(cls, v: Optional[str]) -> Optional[str]:
        """Validate unit.

        Args:
            v: Unit to validate

        Returns:
            Optional[str]: Validated unit

        Raises:
            ValueError: If unit is invalid
        """
        if v is None:
            return v

        # Remove extra whitespace
        v = ' '.join(v.split())

        # Convert to lowercase
        v = v.lower()

        return v

    @property
    def formatted_quantity(self) -> str:
        """Get formatted quantity as a string with fractions.

        Returns:
            str: Formatted quantity
        """
        if self.cantidad == 0:
            return ""

        # Handle whole numbers
        if self.cantidad == int(self.cantidad):
            return str(int(self.cantidad))

        # Convert to fraction for common fractions
        try:
            fraction = Fraction(self.cantidad).limit_denominator(8)

            # Check if it's a proper fraction or mixed number
            if fraction.numerator < fraction.denominator:
                return f"{fraction.numerator}/{fraction.denominator}"
            else:
                # Mixed number
                whole = fraction.numerator // fraction.denominator
                remainder = fraction.numerator % fraction.denominator
                if remainder == 0:
                    return str(whole)
                else:
                    remainder_fraction = Fraction(remainder, fraction.denominator)
                    return f"{whole} {remainder_fraction.numerator}/{remainder_fraction.denominator}"
        except (ValueError, ZeroDivisionError):
            # Fallback to decimal if fraction conversion fails
            return str(self.cantidad)

    @property
    def formatted_unit(self) -> str:
        """Get formatted unit with proper pluralization.

        Returns:
            str: Formatted unit
        """
        if not self.unidad:
            return ""

        # Units that are typically pluralized
        pluralizable_units = {
            "cup": "cups", 
            "piece": "pieces", 
            "slice": "slices", 
            "tablespoon": "tablespoons", 
            "teaspoon": "teaspoons", 
            "clove": "cloves", 
            "item": "items", 
            "serving": "servings"
        }

        # Return plural if cantidad > 1 and unidad is pluralizable
        if self.cantidad > 1 and self.unidad.lower() in pluralizable_units:
            return pluralizable_units[self.unidad.lower()]

        return self.unidad

    def __str__(self) -> str:
        """Get string representation.

        Returns:
            str: String representation
        """
        parts = []
        if self.cantidad > 0:
            parts.append(self.formatted_quantity)
            if self.unidad:
                parts.append(self.formatted_unit)
        parts.append(self.nombre)

        if self.notas:
            parts.append(f"({self.notas})")

        if self.alternativas:
            parts.append(f"or {', '.join(self.alternativas)}")

        return ' '.join(parts)

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
        if not isinstance(other, Ingredient):
            return False

        return (
            self.nombre == other.nombre and
            self.cantidad == other.cantidad and
            self.unidad == other.unidad and
            self.notas == other.notas and
            self.alternativas == other.alternativas
)

    def __hash__(self) -> int:
        """Get hash.

        Returns:
            int: Hash value
        """
        return hash((
            self.nombre, 
            self.cantidad, 
            self.unidad, 
            self.notas, 
            tuple(self.alternativas)
))

    def to_dict(self) -> dict:
        """Convert ingredient to dictionary.

        Returns:
            dict: Ingredient as dictionary
        """
        return {
            "nombre": self.nombre, 
            "cantidad": self.cantidad, 
            "unidad": self.unidad, 
            "notas": self.notas, 
            "alternativas": self.alternativas
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Ingredient':
        """Create from dictionary.

        Args:
            data: Dictionary data

        Returns:
            Ingredient: Created ingredient
        """
        return cls(
            nombre=data.get('nombre', data.get('name', 'ingredient')),
            cantidad=data.get('cantidad', data.get('quantity', 0)),
            unidad=data.get('unidad', data.get('unit')),
            notas=data.get('notas', data.get('notes')),
            alternativas=data.get('alternativas', data.get('alternatives', []))
        )

    def to_string(self) -> str:
        """Convert ingredient to string representation.

        Returns:
            str: String representation of the ingredient
        """
        return str(self)

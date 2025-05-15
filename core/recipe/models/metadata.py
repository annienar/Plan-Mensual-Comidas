from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
from enum import Enum

class RecipeType(Enum):
    DESAYUNO = "Desayuno"
    ALMUERZO = "Almuerzo"
    CENA = "Cena"
    POSTRE = "Postre"
    SNACK = "Snack"
    BEBIDA = "Bebida"
    OTRO = "Otro"

@dataclass
class RecipeMetadata:
    """Metadata for a recipe, matching Notion database properties."""
    title: str
    url: Optional[str] = None
    porciones: Optional[int] = None
    calorias: Optional[int] = None
    tipo: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    hecho: bool = False
    date: Optional[str] = None
    dificultad: Optional[str] = None
    tiempo_preparacion: Optional[int] = None
    tiempo_coccion: Optional[int] = None
    tiempo_total: Optional[int] = None
    notas: Optional[str] = None

    def __post_init__(self):
        """Validate and normalize metadata after initialization."""
        # Ensure title is not empty
        if not self.title:
            self.title = "Receta sin título"

        # Ensure porciones is positive
        if self.porciones is not None and self.porciones <= 0:
            self.porciones = None

        # Ensure calorias is positive
        if self.calorias is not None and self.calorias <= 0:
            self.calorias = None

        # Normalize tipo to valid values
        if self.tipo:
            try:
                self.tipo = RecipeType[self.tipo.upper()].value
            except KeyError:
                self.tipo = RecipeType.OTRO.value

        # Ensure tags are unique and lowercase
        self.tags = list(set(tag.lower() for tag in self.tags))

        # Calculate total time if not provided
        if self.tiempo_total is None:
            prep = self.tiempo_preparacion or 0
            cook = self.tiempo_coccion or 0
            if prep > 0 or cook > 0:
                self.tiempo_total = prep + cook

    @classmethod
    def from_dict(cls, data: dict) -> 'RecipeMetadata':
        """Create a RecipeMetadata instance from a dictionary."""
        return cls(**{
            k: v for k, v in data.items()
            if k in cls.__dataclass_fields__
        }) 
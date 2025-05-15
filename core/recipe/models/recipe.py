from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
from .ingredient import Ingredient
from .metadata import RecipeMetadata

@dataclass
class Recipe:
    """A recipe with all its components and metadata."""
    metadata: RecipeMetadata
    ingredients: List[Ingredient] = field(default_factory=list)
    instructions: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    @property
    def title(self) -> str:
        """Get the recipe title from metadata."""
        return self.metadata.title

    @property
    def tipo(self) -> Optional[str]:
        """Get the recipe type from metadata."""
        return self.metadata.tipo

    @property
    def porciones(self) -> Optional[int]:
        """Get the number of portions from metadata."""
        return self.metadata.porciones

    @property
    def calorias(self) -> Optional[int]:
        """Get the calorie count from metadata."""
        return self.metadata.calorias

    @property
    def tags(self) -> List[str]:
        """Get the recipe tags from metadata."""
        return self.metadata.tags

    @property
    def hecho(self) -> bool:
        """Get the completion status from metadata."""
        return self.metadata.hecho

    @property
    def date(self) -> str:
        """Get the recipe date from metadata."""
        return self.metadata.date

    @property
    def source(self) -> Optional[str]:
        """Get the recipe source URL from metadata."""
        return self.metadata.url

    @classmethod
    def from_dict(cls, data: dict) -> 'Recipe':
        """Create a Recipe instance from a dictionary."""
        metadata = RecipeMetadata.from_dict(data)
        ingredients = [Ingredient.from_dict(i) for i in data.get('ingredients', [])]
        instructions = data.get('instructions', [])
        return cls(
            metadata=metadata,
            ingredients=ingredients,
            instructions=instructions
        )

    def to_dict(self) -> dict:
        """Convert the recipe to a dictionary."""
        return {
            'metadata': {
                'title': self.metadata.title,
                'url': self.metadata.url,
                'porciones': self.metadata.porciones,
                'calorias': self.metadata.calorias,
                'tipo': self.metadata.tipo,
                'tags': self.metadata.tags,
                'hecho': self.metadata.hecho,
                'date': self.metadata.date,
                'dificultad': self.metadata.dificultad,
                'tiempo_preparacion': self.metadata.tiempo_preparacion,
                'tiempo_coccion': self.metadata.tiempo_coccion,
                'tiempo_total': self.metadata.tiempo_total,
                'notas': self.metadata.notas,
            },
            'ingredients': [i.to_dict() for i in self.ingredients],
            'instructions': self.instructions,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        } 
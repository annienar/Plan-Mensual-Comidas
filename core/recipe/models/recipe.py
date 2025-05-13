from dataclasses import dataclass, field
from typing import List
from datetime import datetime
from .ingredient import Ingredient
from .metadata import RecipeMetadata

@dataclass
class Recipe:
    title: str
    ingredients: List[Ingredient]
    instructions: List[str]
    metadata: RecipeMetadata
    source: str | None = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now) 
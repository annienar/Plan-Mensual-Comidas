from dataclasses import dataclass, field
from typing import List

@dataclass
class RecipeMetadata:
    servings: int
    prep_time: int | None = None
    cook_time: int | None = None
    difficulty: str | None = None
    cuisine_type: str | None = None
    tags: List[str] = field(default_factory=list)
    calories_per_serving: float | None = None 
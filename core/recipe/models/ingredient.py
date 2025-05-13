from dataclasses import dataclass, field
from typing import List

@dataclass
class Ingredient:
    name: str
    quantity: float
    unit: str
    notes: str | None = None
    alternatives: List[str] = field(default_factory=list) 
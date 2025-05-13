from dataclasses import dataclass
from typing import List, Optional

@dataclass
class NotionRecipe:
    title: str
    portions: Optional[int] = None
    calories: Optional[int] = None
    ingredients: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    # Add more fields as needed

@dataclass
class NotionIngredient:
    name: str
    quantity: Optional[float] = None
    unit: Optional[str] = None
    # Add more fields as needed 
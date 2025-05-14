from dataclasses import dataclass
from typing import List, Optional

@dataclass
class NotionPantryItem:
    name: str
    category: Optional[str] = None
    unit: Optional[str] = None
    stock: Optional[float] = None
    # Add more pantry properties as needed

@dataclass
class NotionIngredient:
    name: str
    pantry_id: Optional[str] = None  # Notion page ID of linked pantry item
    quantity: Optional[float] = None
    unit: Optional[str] = None
    # Add more ingredient properties as needed

@dataclass
class NotionRecipe:
    title: str
    ingredient_ids: List[str]  # Notion page IDs of linked ingredients
    portions: Optional[int] = None
    calories: Optional[int] = None
    tags: Optional[List[str]] = None
    # Add more recipe properties as needed

# Add more fields as needed 
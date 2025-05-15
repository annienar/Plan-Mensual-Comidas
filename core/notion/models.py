from dataclasses import dataclass, field
from typing import List, Optional, Any

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
    receta_id: Optional[str] = None  # Notion page ID of linked recipe
    # Add more ingredient properties as needed

@dataclass
class NotionRecipe:
    title: str
    ingredient_ids: List[str]  # Notion page IDs of linked ingredients
    portions: Optional[int] = None
    calories: Optional[int] = None
    tags: Optional[List[str]] = None
    tipo: Optional[str] = None
    hecho: Optional[bool] = None
    date: Optional[str] = None
    dificultad: Optional[str] = None
    tiempo_preparacion: Optional[int] = None
    tiempo_coccion: Optional[int] = None
    tiempo_total: Optional[int] = None
    notas: Optional[str] = None
    url: Optional[str] = None
    ingredients: List[Any] = field(default_factory=list)  # List of ingredient objects
    instructions: List[str] = field(default_factory=list)  # List of preparation steps
    # Add more recipe properties as needed

# Add more fields as needed 
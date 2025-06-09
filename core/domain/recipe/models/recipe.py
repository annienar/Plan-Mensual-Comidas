"""
Recipe model.

This module contains the recipe domain model.
"""

from .ingredient import Ingredient
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any

from .metadata import RecipeMetadata
from pydantic import BaseModel, Field, field_validator, model_validator, model_validator

class Recipe(BaseModel):
    """Recipe domain model.

    This class represents a recipe in the domain.
    """

    title: str = Field(
        ..., 
        min_length = 1, 
        max_length = 100, 
        description="Título de la receta"
)
    ingredients: List[Ingredient] = Field(
        ..., 
        min_length=1,
        description="Lista de ingredientes"
)
    instructions: List[str] = Field(
        ..., 
        min_length=1,
        description="Lista de instrucciones de cocina"
)
    metadata: RecipeMetadata = Field(
        ..., 
        description="Metadatos de la receta"
)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Fecha de creación"
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Fecha de última actualización"
    )

    @field_validator('ingredients')
    @classmethod
    def validate_ingredients(cls, v: List[Ingredient]) -> List[Ingredient]:
        """Validate ingredients.

        Args:
            v: Ingredients to validate

        Returns:
            List[Ingredient]: Validated ingredients

        Raises:
            ValueError: If ingredients are invalid
        """
        # Check for empty ingredients list
        if not v:
            raise ValueError("recipe must have at least one ingredient")
            
        # Check for duplicate ingredients
        names = [ing.nombre.lower() for ing in v]
        if len(names) != len(set(names)):
            raise ValueError("Duplicate ingredients found")

        return v

    @field_validator('instructions')
    @classmethod
    def validate_instructions(cls, v: List[str]) -> List[str]:
        """Validate instructions.

        Args:
            v: Instructions to validate

        Returns:
            List[str]: Validated instructions

        Raises:
            ValueError: If instructions are invalid
        """
        # Check for empty instructions list
        if not v:
            raise ValueError("recipe must have at least one instruction")
            
        # Remove whitespace and filter out empty instructions first
        v = [instruction.strip() for instruction in v if instruction.strip()]
        
        # Check if we have any valid instructions after filtering
        if not v:
            raise ValueError("recipe must have at least one instruction")
            
        # Check for instruction length limits
        for i, instruction in enumerate(v, 1):
            if len(instruction) < 10:
                raise ValueError(f"instruction {i} is too short")
            if len(instruction) > 1000:
                raise ValueError(f"instruction {i} is too long")
        
        # Check for duplicate instructions
        if len(v) != len(set(v)):
            raise ValueError("Duplicate instructions found")

        return v

    def __str__(self) -> str:
        """Get string representation.

        Returns:
            str: String representation
        """
        return f"Recipe(title='{self.title}')"

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
        if not isinstance(other, Recipe):
            return False

        return (
            self.title == other.title and
            self.ingredients == other.ingredients and
            self.instructions == other.instructions and
            self.metadata == other.metadata
)

    def __hash__(self) -> int:
        """Get hash.

        Returns:
            int: Hash value
        """
        return hash((
            self.title, 
            tuple(self.ingredients), 
            tuple(self.instructions), 
            self.metadata
))

    # Property accessors for metadata fields
    @property
    def tipo(self) -> Optional[str]:
        """Get recipe type."""
        return self.metadata.tipo

    @property
    def porciones(self) -> Optional[int]:
        """Get servings."""
        return self.metadata.porciones

    @property
    def calorias(self) -> Optional[int]:
        """Get calories."""
        return self.metadata.calorias

    @property
    def tags(self) -> List[str]:
        """Get tags."""
        return self.metadata.tags

    @property
    def hecho(self) -> bool:
        """Get done status."""
        return self.metadata.hecho

    @property
    def date(self) -> str:
        """Get date."""
        return self.metadata.date

    @property
    def source_url(self) -> str:
        """Get source URL."""
        return self.metadata.url

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        """Validate recipe title.

        Args:
            v: Title to validate

        Returns:
            str: Validated title

        Raises:
            ValueError: If title is invalid
        """
        # Check for empty title
        if not v or not v.strip():
            raise ValueError("title must be a non - empty string")
            
        # Remove extra whitespace
        v = " ".join(v.split())

        # Keep original casing - don't auto-convert to title case
        return v

    @model_validator(mode='before')
    @classmethod 
    def validate_input_types(cls, data: Any) -> Any:
        """Validate input types.

        Args:
            data: Input data

        Returns:
            Any: Validated data

        Raises:
            ValueError: If input types are invalid
        """
        if isinstance(data, dict):
            # Check metadata type
            metadata = data.get('metadata')
            if metadata is not None and not isinstance(metadata, (dict, RecipeMetadata)):
                raise ValueError("metadata must be a RecipeMetadata instance")
                
            # Check ingredients type
            ingredients = data.get('ingredients')
            if ingredients is not None and not isinstance(ingredients, list):
                raise ValueError("ingredients must be a list")
            elif isinstance(ingredients, list):
                for ingredient in ingredients:
                    if not isinstance(ingredient, (dict, Ingredient)):
                        raise ValueError("all ingredients must be Ingredient instances")
                        
            # Check instructions type  
            instructions = data.get('instructions')
            if instructions is not None and not isinstance(instructions, list):
                raise ValueError("instructions must be a list")
            elif isinstance(instructions, list):
                for instruction in instructions:
                    if not isinstance(instruction, str):
                        raise ValueError("all instructions must be strings")
                        
            # Check title type
            title = data.get('title')
            if title is not None and not isinstance(title, str):
                raise ValueError("title must be a string")
            elif isinstance(title, str) and not title.strip():
                raise ValueError("title must be a non - empty string")
        
        return data

    @model_validator(mode='after')
    def validate_recipe(self) -> 'Recipe':
        """Validate recipe as a whole.

        Returns:
            Recipe: Validated recipe instance

        Raises:
            ValueError: If recipe is invalid
        """
        # Validate title matches metadata
        if self.title != self.metadata.title:
            raise ValueError("Recipe title must match metadata title")

        return self

    def to_dict(self) -> Dict[str, Any]:
        """Convert recipe to dictionary.

        Returns:
            Dict[str, Any]: Recipe as dictionary
        """
        return {
            'title': self.title, 
            'ingredients': [ingredient.to_dict() for ingredient in self.ingredients], 
            'instructions': self.instructions, 
            'metadata': self.metadata.to_dict(),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Recipe':
        """Create recipe from dictionary.

        Args:
            data: Dictionary data

        Returns:
            Recipe: Created recipe
        """
        from .ingredient import Ingredient
        from .metadata import RecipeMetadata
        from dateutil.parser import parse as parse_date
        
        ingredients = [
            Ingredient.from_dict(ing_data) 
            for ing_data in data.get('ingredients', [])
        ]
        
        metadata = RecipeMetadata(**data.get('metadata', {}))
        
        # Extract title from metadata if not provided directly
        title = data.get('title') or metadata.title
        
        # Parse timestamps if provided
        kwargs = {
            'title': title,
            'ingredients': ingredients,
            'instructions': data.get('instructions', []),
            'metadata': metadata
        }
        
        if 'created_at' in data:
            kwargs['created_at'] = parse_date(data['created_at'])
        if 'updated_at' in data:
            kwargs['updated_at'] = parse_date(data['updated_at'])
        
        return cls(**kwargs)

    def to_markdown(self) -> str:
        """Convert recipe to markdown.

        Returns:
            str: Recipe as markdown
        """
        lines = [
            f"# {self.title}", 
            "", 
            "## Ingredientes", 
            ""
        ]

        # Add ingredients
        for ingredient in self.ingredients:
            lines.append(f"- {ingredient.to_string()}")

        lines.extend([
            "", 
            "## Instrucciones", 
            ""
        ])

        # Add instructions
        for i, instruction in enumerate(self.instructions, 1):
            lines.append(f"{i}. {instruction}")

        # Add metadata
        lines.extend([
            "", 
            "## Metadatos", 
            "", 
            self.metadata.to_markdown()
        ])

        return "\n".join(lines)

    def to_notion_blocks(self) -> List[Dict[str, Any]]:
        """Convert recipe to Notion blocks.

        Returns:
            List[Dict[str, Any]]: Recipe as Notion blocks
        """
        blocks = [
            {
                "object": "block", 
                "type": "heading_1", 
                "heading_1": {
                    "rich_text": [{"type": "text", "text": {"content": self.title}}]
                }
            }, 
            {
                "object": "block", 
                "type": "heading_2", 
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": "Ingredients"}}]
                }
            }
        ]

        # Add ingredients
        for ingredient in self.ingredients:
            blocks.append({
                "object": "block", 
                "type": "bulleted_list_item", 
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": ingredient.to_string()}}]
                }
            })

        blocks.append({
            "object": "block", 
            "type": "heading_2", 
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "Instructions"}}]
            }
        })

        # Add instructions
        for i, instruction in enumerate(self.instructions, 1):
            blocks.append({
                "object": "block", 
                "type": "numbered_list_item", 
                "numbered_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": instruction}}]
                }
            })

        # Add metadata
        blocks.extend([
            {
                "object": "block", 
                "type": "heading_2", 
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": "Metadata"}}]
                }
            }
        ])

        blocks.extend(self.metadata.to_notion_blocks())

        return blocks

    def is_valid(self) -> bool:
        """Check if recipe is valid.

        Returns:
            bool: True if recipe is valid, False otherwise
        """
        try:
            # Check basic required fields
            if not self.title or not self.title.strip():
                return False
            if not self.ingredients:
                return False
            if not self.instructions:
                return False
            if not self.metadata:
                return False
            
            # Check if title matches metadata
            if self.title != self.metadata.title:
                return False
                
            return True
        except Exception:
            return False

    def to_json(self) -> str:
        """Convert recipe to JSON string.

        Returns:
            str: Recipe as JSON string
        """
        import json
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)

    @classmethod
    def from_json(cls, json_str: str) -> 'Recipe':
        """Create recipe from JSON string.

        Args:
            json_str: JSON string data

        Returns:
            Recipe: Created recipe
        """
        import json
        data = json.loads(json_str)
        return cls.from_dict(data)

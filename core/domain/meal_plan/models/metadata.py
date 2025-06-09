"""
Meal plan metadata model.

This module contains the meal plan metadata domain model.
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator

class MealPlanMetadata(BaseModel):
    """Meal plan metadata domain model.

    This class represents meal plan metadata in the domain.
    """

    title: str = Field(
        ..., 
        min_length = 3, 
        max_length = 200, 
        description="Título del plan de comidas"
)
    start_date: str = Field(
        ..., 
        pattern = r'^\d{4}-\d{2}-\d{2}$', 
        description="Fecha de inicio en formato YYYY - MM - DD"
)
    end_date: str = Field(
        ..., 
        pattern = r'^\d{4}-\d{2}-\d{2}$', 
        description="Fecha de fin en formato YYYY - MM - DD"
)
    description: str = Field(
        ..., 
        min_length = 1, 
        max_length = 500, 
        description="Descripción del plan de comidas"
)
    tags: List[str] = Field(
        default_factory = list, 
        description="Etiquetas del plan de comidas"
)
    hecho: bool = Field(
        False, 
        description="Si el plan de comidas está completado"
)
    notas: Optional[str] = Field(
        None, 
        description="Notas adicionales"
)

    @field_validator('start_date')
    @classmethod
    def validate_start_date(cls, v: str) -> str:
        """Validate start date.

        Args:
            v: Start date to validate

        Returns:
            str: Validated start date

        Raises:
            ValueError: If start date is invalid
        """
        try:
            datetime.strptime(v, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Invalid start date format. Use YYYY - MM - DD")

        return v

    @field_validator('end_date')
    @classmethod
    def validate_end_date(cls, v: str) -> str:
        """Validate end date.

        Args:
            v: End date to validate

        Returns:
            str: Validated end date

        Raises:
            ValueError: If end date is invalid
        """
        try:
            datetime.strptime(v, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Invalid end date format. Use YYYY - MM - DD")

        return v

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        """Validate meal plan title.

        Args:
            v: Title to validate

        Returns:
            str: Validated title

        Raises:
            ValueError: If title is invalid
        """
        # Remove extra whitespace
        v = " ".join(v.split())

        # Convert to title case
        v = v.title()

        return v

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, v: List[str]) -> List[str]:
        """Validate meal plan tags.

        Args:
            v: Tags to validate

        Returns:
            List[str]: Validated tags

        Raises:
            ValueError: If tags are invalid
        """
        # Remove duplicates
        v = list(dict.fromkeys(v))

        # Validate each tag
        for i, tag in enumerate(v):
            # Remove extra whitespace
            tag = " ".join(tag.split())

            # Convert to title case
            tag = tag.title()

            v[i] = tag

        return v

    def __str__(self) -> str:
        """Get string representation.

        Returns:
            str: String representation
        """
        return (
            f"Metadata(start_date='{self.start_date}', "
            f"end_date='{self.end_date}', "
            f"description='{self.description}')"
)

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
        if not isinstance(other, MealPlanMetadata):
            return False

        return (
            self.start_date == other.start_date and
            self.end_date == other.end_date and
            self.description == other.description
)

    def __hash__(self) -> int:
        """Get hash.

        Returns:
            int: Hash value
        """
        return hash((
            self.start_date, 
            self.end_date, 
            self.description
))

    def to_dict(self) -> dict:
        """Convert metadata to dictionary.

        Returns:
            dict: Metadata as dictionary
        """
        return {
            'title': self.title, 
            'start_date': self.start_date, 
            'end_date': self.end_date, 
            'description': self.description, 
            'tags': self.tags, 
            'hecho': self.hecho, 
            'notas': self.notas
        }

    def to_markdown(self) -> str:
        """Convert metadata to markdown.

        Returns:
            str: Metadata as markdown
        """
        lines = []

        lines.append(f"- **Fecha de Inicio:** {self.start_date}")
        lines.append(f"- **Fecha de Fin:** {self.end_date}")

        if self.tags:
            lines.append(f"- **Etiquetas:** {', '.join(self.tags)}")

        lines.append(f"- **Hecho:** {'Sí' if self.hecho else 'No'}")

        if self.notas:
            lines.append(f"- **Notas:** {self.notas}")

        return "\n".join(lines)

    def to_notion_blocks(self) -> List[dict]:
        """Convert metadata to Notion blocks.

        Returns:
            List[dict]: Metadata as Notion blocks
        """
        blocks = [
            {
                "object": "block", 
                "type": "bulleted_list_item", 
                "bulleted_list_item": {
                    "rich_text": [
                        {"type": "text", "text": {"content": "Fecha de Inicio: "}}, 
                        {"type": "text", "text": {"content": self.start_date}}
                    ]
                }
            }, 
            {
                "object": "block", 
                "type": "bulleted_list_item", 
                "bulleted_list_item": {
                    "rich_text": [
                        {"type": "text", "text": {"content": "Fecha de Fin: "}}, 
                        {"type": "text", "text": {"content": self.end_date}}
                    ]
                }
            }
        ]

        if self.tags:
            blocks.append({
                "object": "block", 
                "type": "bulleted_list_item", 
                "bulleted_list_item": {
                    "rich_text": [
                        {"type": "text", "text": {"content": "Etiquetas: "}}, 
                        {"type": "text", "text": {"content": ", ".join(self.tags)}}
                    ]
                }
            })

        blocks.append({
            "object": "block", 
            "type": "bulleted_list_item", 
            "bulleted_list_item": {
                "rich_text": [
                    {"type": "text", "text": {"content": "Hecho: "}}, 
                    {"type": "text", "text": {"content": "Sí" if self.hecho else "No"}}
                ]
            }
        })

        if self.notas:
            blocks.extend([
                {
                    "object": "block", 
                    "type": "bulleted_list_item", 
                    "bulleted_list_item": {
                        "rich_text": [
                            {"type": "text", "text": {"content": "Notas: "}}, 
                            {"type": "text", "text": {"content": self.notas}}
                        ]
                    }
                }
            ])

        return blocks

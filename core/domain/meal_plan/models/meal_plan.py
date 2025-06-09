"""
Meal plan model.

This module contains the meal plan domain model.
"""

from datetime import datetime
from typing import List, Optional, Dict, Any

from .meal import Meal
from .metadata import MealPlanMetadata
from pydantic import BaseModel, Field, field_validator, model_validator

class MealPlan(BaseModel):
    """Meal plan domain model.

    This class represents a meal plan in the domain.
    """

    title: str = Field(
        ..., 
        min_length = 1, 
        max_length = 100, 
        description="Título del plan de comidas"
)
    meals: List[Meal] = Field(
        ..., 
        min_length= 1, 
        description="Lista de comidas"
)
    metadata: MealPlanMetadata = Field(
        ..., 
        description="Metadatos del plan de comidas"
)

    @field_validator('title')
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

    @field_validator('meals')
    @classmethod
    def validate_meals(cls, v: List[Meal]) -> List[Meal]:
        """Validate meals.

        Args:
            v: Meals to validate

        Returns:
            List[Meal]: Validated meals

        Raises:
            ValueError: If meals are invalid
        """
        # Check for duplicate meals
        meal_keys = [(meal.type, meal.date, meal.time) for meal in v]
        if len(meal_keys) != len(set(meal_keys)):
            raise ValueError("Duplicate meals found")

        # Sort meals by date and time
        v.sort(key = lambda m: (m.date, m.time))

        return v

    @model_validator(mode='after')
    def validate_meal_plan(self) -> 'MealPlan':
        """Validate meal plan as a whole.

        Returns:
            MealPlan: Validated meal plan instance

        Raises:
            ValueError: If meal plan is invalid
        """
        # Validate title matches metadata
        if self.title != self.metadata.title:
            raise ValueError("Meal plan title must match metadata title")

        # Validate meal dates are within plan period
        start_date = self.metadata.start_date
        end_date = self.metadata.end_date

        if start_date and end_date:
            for meal in self.meals:
                meal_date = datetime.strptime(meal.date, "%Y-%m-%d")
                plan_start = datetime.strptime(start_date, "%Y-%m-%d")
                plan_end = datetime.strptime(end_date, "%Y-%m-%d")

                if not plan_start <= meal_date <= plan_end:
                    raise ValueError(f"Meal {meal.title} date must be within plan period")

        return self

    def __str__(self) -> str:
        """Get string representation.

        Returns:
            str: String representation
        """
        return f"MealPlan(title='{self.title}')"

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
        if not isinstance(other, MealPlan):
            return False

        return (
            self.title == other.title and
            self.meals == other.meals and
            self.metadata == other.metadata
)

    def __hash__(self) -> int:
        """Get hash.

        Returns:
            int: Hash value
        """
        return hash((
            self.title, 
            tuple(self.meals), 
            self.metadata
))

    def to_dict(self) -> Dict[str, Any]:
        """Convert meal plan to dictionary.

        Returns:
            Dict[str, Any]: Meal plan as dictionary
        """
        return {
            'title': self.title, 
            'meals': [meal.to_dict() for meal in self.meals], 
            'metadata': self.metadata.to_dict()
        }

    def to_markdown(self) -> str:
        """Convert meal plan to markdown.

        Returns:
            str: Meal plan as markdown
        """
        lines = [
            f"# {self.title}", 
            "", 
            "## Comidas", 
            ""
        ]

        # Group meals by date
        meals_by_date = {}
        for meal in self.meals:
            if meal.date not in meals_by_date:
                meals_by_date[meal.date] = []
            meals_by_date[meal.date].append(meal)

        # Add meals by date
        for date in sorted(meals_by_date.keys()):
            lines.extend([
                f"### {date}", 
                ""
            ])

            for meal in meals_by_date[date]:
                lines.extend([
                    f"#### {meal.title}", 
                    "", 
                    f"**Tipo:** {meal.type}", 
                    f"**Hora:** {meal.time}", 
                    "", 
                    "**Recetas:**", 
                    ""
                ])

                for recipe in meal.recipes:
                    lines.append(f"- {recipe.title}")

                if meal.notes:
                    lines.extend([
                        "", 
                        "**Notas:**", 
                        f"{meal.notes}", 
                        ""
                    ])

        # Add metadata
        lines.extend([
            "", 
            "## Metadatos", 
            "", 
            self.metadata.to_markdown()
        ])

        return "\n".join(lines)

    def to_notion_blocks(self) -> List[Dict[str, Any]]:
        """Convert meal plan to Notion blocks.

        Returns:
            List[Dict[str, Any]]: Meal plan as Notion blocks
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
                    "rich_text": [{"type": "text", "text": {"content": "Comidas"}}]
                }
            }
        ]

        # Group meals by date
        meals_by_date = {}
        for meal in self.meals:
            if meal.date not in meals_by_date:
                meals_by_date[meal.date] = []
            meals_by_date[meal.date].append(meal)

        # Add meals by date
        for date in sorted(meals_by_date.keys()):
            blocks.append({
                "object": "block", 
                "type": "heading_3", 
                "heading_3": {
                    "rich_text": [{"type": "text", "text": {"content": date}}]
                }
            })

            for meal in meals_by_date[date]:
                blocks.extend([
                    {
                        "object": "block", 
                        "type": "heading_4", 
                        "heading_4": {
                            "rich_text": [{"type": "text", "text": {"content": meal.title}}]
                        }
                    }, 
                    {
                        "object": "block", 
                        "type": "paragraph", 
                        "paragraph": {
                            "rich_text": [
                                {"type": "text", "text": {"content": "Tipo: "}}, 
                                {"type": "text", "text": {"content": meal.type}}
                            ]
                        }
                    }, 
                    {
                        "object": "block", 
                        "type": "paragraph", 
                        "paragraph": {
                            "rich_text": [
                                {"type": "text", "text": {"content": "Hora: "}}, 
                                {"type": "text", "text": {"content": meal.time}}
                            ]
                        }
                    }, 
                    {
                        "object": "block", 
                        "type": "paragraph", 
                        "paragraph": {
                            "rich_text": [{"type": "text", "text": {"content": "Recetas:"}}]
                        }
                    }
                ])

                for recipe in meal.recipes:
                    blocks.append({
                        "object": "block", 
                        "type": "bulleted_list_item", 
                        "bulleted_list_item": {
                            "rich_text": [{"type": "text", "text": {"content": recipe.title}}]
                        }
                    })

                if meal.notes:
                    blocks.extend([
                        {
                            "object": "block", 
                            "type": "paragraph", 
                            "paragraph": {
                                "rich_text": [{"type": "text", "text": {"content": "Notas:"}}]
                            }
                        }, 
                        {
                            "object": "block", 
                            "type": "paragraph", 
                            "paragraph": {
                                "rich_text": [{"type": "text", "text": {"content": meal.notes}}]
                            }
                        }
                    ])

        # Add metadata
        blocks.extend([
            {
                "object": "block", 
                "type": "heading_2", 
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": "Metadatos"}}]
                }
            }
        ])

        blocks.extend(self.metadata.to_notion_blocks())

        return blocks

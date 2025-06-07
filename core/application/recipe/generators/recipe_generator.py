"""
Recipe generator.

This module contains the recipe generator implementation.
"""

from core.domain.exceptions.recipe import RecipeGenerationError
from core.domain.recipe.models.ingredient import Ingredient
from core.domain.recipe.models.metadata import RecipeMetadata
from core.domain.recipe.models.recipe import Recipe
from datetime import datetime
from typing import List, Optional, Dict, Any
import json

from pydantic import BaseModel, Field
import markdown
import yaml

class RecipeGenerator:
    """Recipe generator.

    This class handles recipe generation in different formats.
    """

    def __init__(self):
        """Initialize the generator."""
        pass

    def to_markdown(self, recipe: Recipe) -> str:
        """Convert recipe to markdown.

        Args:
            recipe: Recipe to convert

        Returns:
            str: Markdown representation

        Raises:
            RecipeGenerationError: If generation fails
        """
        try:
            lines = [
                f"# {recipe.title}", 
                "", 
                "## Metadata", 
                f"- Porciones: {recipe.metadata.porciones}", 
                f"- Calorías: {recipe.metadata.calorias}", 
                f"- Tiempo total: {recipe.metadata.tiempo_preparacion + recipe.metadata.tiempo_coccion} minutos", 
                f"- Dificultad: {recipe.metadata.dificultad}", 
                f"- Tags: {', '.join(recipe.metadata.tags)}", 
                "", 
                "## Ingredientes", 
                *[f"- {ingredient.quantity} {ingredient.unit or ''} {ingredient.name}".strip()
                for ingredient in recipe.ingredients], 
                "", 
                "## Instrucciones", 
                *[f"{i + 1}. {instruction}"
                for i, instruction in enumerate(recipe.instructions)], 
                ""
            ]

            return "\n".join(lines)

        except Exception as e:
            raise RecipeGenerationError(f"Failed to generate markdown: {str(e)}")

    def to_html(self, recipe: Recipe) -> str:
        """Convert recipe to HTML.

        Args:
            recipe: Recipe to convert

        Returns:
            str: HTML representation

        Raises:
            RecipeGenerationError: If generation fails
        """
        try:
            # Convert to markdown first
            md = self.to_markdown(recipe)

            # Convert markdown to HTML
            html = markdown.markdown(
                md, 
                extensions=['tables', 'fenced_code']
)

            # Add CSS
            css = """
            <style>
                body {
                    font - family: Arial, sans - serif
                    line - height: 1.6
                    max - width: 800px
                    margin: 0 auto
                    padding: 20px
                }
                h1 {
                    color: #2c3e50
                    border - bottom: 2px solid #eee
                    padding - bottom: 10px
                }
                h2 {
                    color: #34495e
                    margin - top: 30px
                }
                ul, ol {
                    padding - left: 20px
                }
                li {
                    margin: 5px 0
                }
                .metadata {
                    background: #f8f9fa
                    padding: 15px
                    border - radius: 5px
                    margin: 20px 0
                }
                .tags {
                    margin - top: 10px
                }
                .tag {
                    display: inline - block
                    background: #e9ecef
                    padding: 3px 8px
                    border - radius: 3px
                    margin: 2px
                    font - size: 0.9em
                }
            </style>
            """

            return f"<!DOCTYPE html>\n < html>\n < head>\n{css}\n</head>\n < body>\n{html}\n</body>\n</html>"

        except Exception as e:
            raise RecipeGenerationError(f"Failed to generate HTML: {str(e)}")

    def to_json(self, recipe: Recipe) -> str:
        """Convert recipe to JSON.

        Args:
            recipe: Recipe to convert

        Returns:
            str: JSON representation

        Raises:
            RecipeGenerationError: If generation fails
        """
        try:
            data = {
                "title": recipe.title, 
                "ingredients": [
                    {
                        "name": ing.name, 
                        "quantity": ing.quantity, 
                        "unit": ing.unit
                    }
                    for ing in recipe.ingredients
                ], 
                "instructions": recipe.instructions, 
                "metadata": {
                    "porciones": recipe.metadata.porciones, 
                    "calorias": recipe.metadata.calorias, 
                    "tiempo_preparacion": recipe.metadata.tiempo_preparacion, 
                    "tiempo_coccion": recipe.metadata.tiempo_coccion, 
                    "dificultad": recipe.metadata.dificultad, 
                    "tags": recipe.metadata.tags
                }
            }

            return json.dumps(data, indent = 2, ensure_ascii = False)

        except Exception as e:
            raise RecipeGenerationError(f"Failed to generate JSON: {str(e)}")

    def to_yaml(self, recipe: Recipe) -> str:
        """Convert recipe to YAML.

        Args:
            recipe: Recipe to convert

        Returns:
            str: YAML representation

        Raises:
            RecipeGenerationError: If generation fails
        """
        try:
            data = {
                "title": recipe.title, 
                "ingredients": [
                    {
                        "name": ing.name, 
                        "quantity": ing.quantity, 
                        "unit": ing.unit
                    }
                    for ing in recipe.ingredients
                ], 
                "instructions": recipe.instructions, 
                "metadata": {
                    "porciones": recipe.metadata.porciones, 
                    "calorias": recipe.metadata.calorias, 
                    "tiempo_preparacion": recipe.metadata.tiempo_preparacion, 
                    "tiempo_coccion": recipe.metadata.tiempo_coccion, 
                    "dificultad": recipe.metadata.dificultad, 
                    "tags": recipe.metadata.tags
                }
            }

            return yaml.dump(data, allow_unicode = True, sort_keys = False)

        except Exception as e:
            raise RecipeGenerationError(f"Failed to generate YAML: {str(e)}")

    def to_notion_blocks(self, recipe: Recipe) -> List[Dict[str, Any]]:
        """Convert recipe to Notion blocks.

        Args:
            recipe: Recipe to convert

        Returns:
            List[Dict[str, Any]]: Notion blocks

        Raises:
            RecipeGenerationError: If generation fails
        """
        try:
            blocks = [
                {
                    "object": "block", 
                    "type": "heading_1", 
                    "heading_1": {
                        "rich_text": [
                            {
                                "type": "text", 
                                "text": {
                                    "content": recipe.title
                                }
                            }
                        ]
                    }
                }, 
                {
                    "object": "block", 
                    "type": "heading_2", 
                    "heading_2": {
                        "rich_text": [
                            {
                                "type": "text", 
                                "text": {
                                    "content": "Metadata"
                                }
                            }
                        ]
                    }
                }, 
                {
                    "object": "block", 
                    "type": "bulleted_list_item", 
                    "bulleted_list_item": {
                        "rich_text": [
                            {
                                "type": "text", 
                                "text": {
                                    "content": f"Porciones: {recipe.metadata.porciones}"
                                }
                            }
                        ]
                    }
                }, 
                {
                    "object": "block", 
                    "type": "bulleted_list_item", 
                    "bulleted_list_item": {
                        "rich_text": [
                            {
                                "type": "text", 
                                "text": {
                                    "content": f"Calorías: {recipe.metadata.calorias}"
                                }
                            }
                        ]
                    }
                }, 
                {
                    "object": "block", 
                    "type": "bulleted_list_item", 
                    "bulleted_list_item": {
                        "rich_text": [
                            {
                                "type": "text", 
                                "text": {
                                    "content": f"Tiempo total: {recipe.metadata.tiempo_preparacion + recipe.metadata.tiempo_coccion} minutos"
                                }
                            }
                        ]
                    }
                }, 
                {
                    "object": "block", 
                    "type": "bulleted_list_item", 
                    "bulleted_list_item": {
                        "rich_text": [
                            {
                                "type": "text", 
                                "text": {
                                    "content": f"Dificultad: {recipe.metadata.dificultad}"
                                }
                            }
                        ]
                    }
                }, 
                {
                    "object": "block", 
                    "type": "bulleted_list_item", 
                    "bulleted_list_item": {
                        "rich_text": [
                            {
                                "type": "text", 
                                "text": {
                                    "content": f"Tags: {', '.join(recipe.metadata.tags)}"
                                }
                            }
                        ]
                    }
                }, 
                {
                    "object": "block", 
                    "type": "heading_2", 
                    "heading_2": {
                        "rich_text": [
                            {
                                "type": "text", 
                                "text": {
                                    "content": "Ingredientes"
                                }
                            }
                        ]
                    }
                }
            ]

            # Add ingredients
            for ingredient in recipe.ingredients:
                blocks.append({
                    "object": "block", 
                    "type": "bulleted_list_item", 
                    "bulleted_list_item": {
                        "rich_text": [
                            {
                                "type": "text", 
                                "text": {
                                    "content": f"{ingredient.quantity} {ingredient.unit or ''} {ingredient.name}".strip()
                                }
                            }
                        ]
                    }
                })

            # Add instructions heading
            blocks.append({
                "object": "block", 
                "type": "heading_2", 
                "heading_2": {
                    "rich_text": [
                        {
                            "type": "text", 
                            "text": {
                                "content": "Instrucciones"
                            }
                        }
                    ]
                }
            })

            # Add instructions
            for i, instruction in enumerate(recipe.instructions):
                blocks.append({
                    "object": "block", 
                    "type": "numbered_list_item", 
                    "numbered_list_item": {
                        "rich_text": [
                            {
                                "type": "text", 
                                "text": {
                                    "content": instruction
                                }
                            }
                        ]
                    }
                })

            return blocks

        except Exception as e:
            raise RecipeGenerationError(f"Failed to generate Notion blocks: {str(e)}")

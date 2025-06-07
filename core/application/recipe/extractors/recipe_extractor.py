"""
Recipe extractor.

This module contains the recipe extractor implementation.
"""

from core.domain.exceptions.recipe import RecipeExtractionError
from core.domain.recipe.models.ingredient import Ingredient
from core.domain.recipe.models.metadata import RecipeMetadata
from core.domain.recipe.models.recipe import Recipe
from datetime import datetime
from typing import List, Optional, Dict, Any, Union
import json
import re

from pydantic import BaseModel, Field, validator
import yaml

class RecipeExtractor:
    """Recipe extractor.

    This class handles recipe extraction from different formats.
    """

    def __init__(self):
        """Initialize the extractor."""
        pass

    def from_markdown(self, text: str) -> Recipe:
        """Extract recipe from markdown.

        Args:
            text: Markdown text

        Returns:
            Recipe: Extracted recipe

        Raises:
            RecipeExtractionError: If extraction fails
        """
        try:
            # Split into sections
            sections = text.split("\n## ")

            # Extract title
            title = sections[0].strip("# \n")

            # Initialize metadata
            metadata = {
                "porciones": 1, 
                "calorias": 0, 
                "tiempo_preparacion": 0, 
                "tiempo_coccion": 0, 
                "dificultad": "Media", 
                "tags": []
            }

            # Extract metadata
            for section in sections:
                if section.startswith("Metadata"):
                    lines = section.split("\n")[1:]
                    for line in lines:
                        line = line.strip("- ")
                        if line.startswith("Porciones:"):
                            metadata["porciones"] = int(line.split(":")[1].strip())
                        elif line.startswith("Calorías:"):
                            metadata["calorias"] = int(line.split(":")[1].strip())
                        elif line.startswith("Tiempo total:"):
                            total_time = int(line.split(":")[1].strip().split()[0])
                            metadata["tiempo_preparacion"] = total_time // 2
                            metadata["tiempo_coccion"] = total_time // 2
                        elif line.startswith("Dificultad:"):
                            metadata["dificultad"] = line.split(":")[1].strip()
                        elif line.startswith("Tags:"):
                            metadata["tags"] = [
                                tag.strip()
                                for tag in line.split(":")[1].strip().split(", ")
                            ]

            # Extract ingredients
            ingredients = []
            for section in sections:
                if section.startswith("Ingredientes"):
                    lines = section.split("\n")[1:]
                    for line in lines:
                        line = line.strip("- ")
                        if not line:
                            continue

                        # Parse quantity and unit
                        match = re.match(r"^(\d + (?:\.\d+)?)\s * ([a - zA - Z]+)?\s + (.+)$", line)
                        if match:
                            quantity = float(match.group(1))
                            unit = match.group(2)
                            name = match.group(3)

                            ingredients.append(
                                Ingredient(
                                    name = name, 
                                    quantity = quantity, 
                                    unit = unit
)
)

            # Extract instructions
            instructions = []
            for section in sections:
                if section.startswith("Instrucciones"):
                    lines = section.split("\n")[1:]
                    for line in lines:
                        line = re.sub(r"^\d+\.\s*", "", line.strip())
                        if line:
                            instructions.append(line)

            # Create recipe
            return Recipe(
                title = title, 
                ingredients = ingredients, 
                instructions = instructions, 
                metadata = RecipeMetadata(**metadata)
)

        except Exception as e:
            raise RecipeExtractionError(f"Failed to extract recipe from markdown: {str(e)}")

    def from_json(self, text: str) -> Recipe:
        """Extract recipe from JSON.

        Args:
            text: JSON text

        Returns:
            Recipe: Extracted recipe

        Raises:
            RecipeExtractionError: If extraction fails
        """
        try:
            data = json.loads(text)

            # Extract ingredients
            ingredients = [
                Ingredient(
                    name = ing["name"], 
                    quantity = ing["quantity"], 
                    unit = ing.get("unit")
)
                for ing in data["ingredients"]
            ]

            # Create recipe
            return Recipe(
                title = data["title"], 
                ingredients = ingredients, 
                instructions = data["instructions"], 
                metadata = RecipeMetadata(**data["metadata"])
)

        except Exception as e:
            raise RecipeExtractionError(f"Failed to extract recipe from JSON: {str(e)}")

    def from_yaml(self, text: str) -> Recipe:
        """Extract recipe from YAML.

        Args:
            text: YAML text

        Returns:
            Recipe: Extracted recipe

        Raises:
            RecipeExtractionError: If extraction fails
        """
        try:
            data = yaml.safe_load(text)

            # Extract ingredients
            ingredients = [
                Ingredient(
                    name = ing["name"], 
                    quantity = ing["quantity"], 
                    unit = ing.get("unit")
)
                for ing in data["ingredients"]
            ]

            # Create recipe
            return Recipe(
                title = data["title"], 
                ingredients = ingredients, 
                instructions = data["instructions"], 
                metadata = RecipeMetadata(**data["metadata"])
)

        except Exception as e:
            raise RecipeExtractionError(f"Failed to extract recipe from YAML: {str(e)}")

    def from_notion_blocks(self, blocks: List[Dict[str, Any]]) -> Recipe:
        """Extract recipe from Notion blocks.

        Args:
            blocks: Notion blocks

        Returns:
            Recipe: Extracted recipe

        Raises:
            RecipeExtractionError: If extraction fails
        """
        try:
            # Initialize data
            title = ""
            metadata = {
                "porciones": 1, 
                "calorias": 0, 
                "tiempo_preparacion": 0, 
                "tiempo_coccion": 0, 
                "dificultad": "Media", 
                "tags": []
            }
            ingredients = []
            instructions = []

            # Process blocks
            current_section = None
            for block in blocks:
                block_type = block.get("type")

                if block_type == "heading_1":
                    title = block["heading_1"]["rich_text"][0]["text"]["content"]

                elif block_type == "heading_2":
                    current_section = block["heading_2"]["rich_text"][0]["text"]["content"]

                elif block_type == "bulleted_list_item":
                    text = block["bulleted_list_item"]["rich_text"][0]["text"]["content"]

                    if current_section == "Metadata":
                        if text.startswith("Porciones:"):
                            metadata["porciones"] = int(text.split(":")[1].strip())
                        elif text.startswith("Calorías:"):
                            metadata["calorias"] = int(text.split(":")[1].strip())
                        elif text.startswith("Tiempo total:"):
                            total_time = int(text.split(":")[1].strip().split()[0])
                            metadata["tiempo_preparacion"] = total_time // 2
                            metadata["tiempo_coccion"] = total_time // 2
                        elif text.startswith("Dificultad:"):
                            metadata["dificultad"] = text.split(":")[1].strip()
                        elif text.startswith("Tags:"):
                            metadata["tags"] = [
                                tag.strip()
                                for tag in text.split(":")[1].strip().split(", ")
                            ]

                    elif current_section == "Ingredientes":
                        # Parse quantity and unit
                        match = re.match(r"^(\d + (?:\.\d+)?)\s * ([a - zA - Z]+)?\s + (.+)$", text)
                        if match:
                            quantity = float(match.group(1))
                            unit = match.group(2)
                            name = match.group(3)

                            ingredients.append(
                                Ingredient(
                                    name = name, 
                                    quantity = quantity, 
                                    unit = unit
)
)

                elif block_type == "numbered_list_item":
                    if current_section == "Instrucciones":
                        text = block["numbered_list_item"]["rich_text"][0]["text"]["content"]
                        instructions.append(text)

            # Create recipe
            return Recipe(
                title = title, 
                ingredients = ingredients, 
                instructions = instructions, 
                metadata = RecipeMetadata(**metadata)
)

        except Exception as e:
            raise RecipeExtractionError(f"Failed to extract recipe from Notion blocks: {str(e)}")

    def from_text(self, text: str) -> Recipe:
        """Extract recipe from plain text.

        Args:
            text: Plain text

        Returns:
            Recipe: Extracted recipe

        Raises:
            RecipeExtractionError: If extraction fails
        """
        try:
            # Try to detect format
            if text.strip().startswith("# "):
                return self.from_markdown(text)

            try:
                return self.from_json(text)
            except:
                pass

            try:
                return self.from_yaml(text)
            except:
                pass

            # If no format detected, treat as markdown
            return self.from_markdown(text)

        except Exception as e:
            raise RecipeExtractionError(f"Failed to extract recipe from text: {str(e)}")

"""
Meal plan response parsers.

This module provides parsers for LLM responses related to meal plans.
"""

from core.domain.meal_plan.models.meal import Meal
from core.domain.meal_plan.models.metadata import MealPlanMetadata
from core.domain.recipe.models.ingredient import Ingredient
from core.domain.recipe.models.metadata import RecipeMetadata
from core.domain.recipe.models.recipe import Recipe
from datetime import datetime
from typing import List, Dict, Any, Optional
import re

def parse_recipe_response(response: str) -> Recipe:
    """Parse LLM response for recipe generation.

    Args:
        response: LLM response

    Returns:
        Recipe: Parsed recipe

    Raises:
        ValueError: If response cannot be parsed
    """
    # Extract title
    title_match = re.search(r"Title:\s * (.+?)(?:\n|$)", response)
    if not title_match:
        raise ValueError("Could not find recipe title")
    title = title_match.group(1).strip()

    # Extract ingredients
    ingredients_section = re.search(r"Ingredients:(.*?)(?:\n\n|\nInstructions:)", response, re.DOTALL)
    if not ingredients_section:
        raise ValueError("Could not find ingredients section")

    ingredients = []
    for line in ingredients_section.group(1).strip().split("\n"):
        if not line.strip() or not line.startswith("-"):
            continue

        # Parse ingredient line
        ingredient_text = line.strip("- ").strip()
        ingredient_match = re.match(r"(\d + (?:\.\d+)?)\s * (\w+)?\s + (.+?)(?:\s + to\s + taste)?$", ingredient_text)

        if ingredient_match:
            quantity, unit, name = ingredient_match.groups()
            ingredients.append(Ingredient(
                name = name.strip(), 
                quantity = float(quantity), 
                unit = unit.strip() if unit else None
))
        else:
            # Handle ingredients without quantities
            ingredients.append(Ingredient(
                name = ingredient_text, 
                quantity = 0.0, 
                unit = None
))

    # Extract instructions
    instructions_section = re.search(r"Instructions:(.*?)(?:\n\n|\nMetadata:)", response, re.DOTALL)
    if not instructions_section:
        raise ValueError("Could not find instructions section")

    instructions = []
    for line in instructions_section.group(1).strip().split("\n"):
        if not line.strip():
            continue

        # Remove numbering if present
        instruction = re.sub(r"^\d+\.\s*", "", line.strip())
        instructions.append(instruction)

    # Extract metadata
    metadata_section = re.search(r"Metadata:(.*?)$", response, re.DOTALL)
    if not metadata_section:
        raise ValueError("Could not find metadata section")

    metadata = {}
    for line in metadata_section.group(1).strip().split("\n"):
        if not line.strip() or not line.startswith("-"):
            continue

        # Parse metadata line
        key, value = line.strip("- ").split(":", 1)
        key = key.strip().lower().replace(" ", "_")
        value = value.strip()

        if key == "portions":
            metadata["porciones"] = int(value)
        elif key == "calories":
            metadata["calorias"] = int(value)
        elif key == "preparation_time":
            metadata["tiempo_preparacion"] = int(value.split()[0])
        elif key == "cooking_time":
            metadata["tiempo_coccion"] = int(value.split()[0])
        elif key == "difficulty":
            metadata["dificultad"] = value.lower()
        elif key == "tags":
            metadata["tags"] = [tag.strip() for tag in value.split(", ")]

    # Create recipe
    return Recipe(
        title = title, 
        ingredients = ingredients, 
        instructions = instructions, 
        metadata = RecipeMetadata(**metadata)
)

def parse_metadata_response(response: str) -> MealPlanMetadata:
    """Parse LLM response for metadata extraction.

    Args:
        response: LLM response

    Returns:
        MealPlanMetadata: Parsed metadata

    Raises:
        ValueError: If response cannot be parsed
    """
    # Extract title
    title_match = re.search(r"Title:\s * (.+?)(?:\n|$)", response)
    if not title_match:
        raise ValueError("Could not find meal plan title")
    title = title_match.group(1).strip()

    # Extract start date
    start_date_match = re.search(r"Start Date:\s * (\d{4}-\d{2}-\d{2})", response)
    if not start_date_match:
        raise ValueError("Could not find start date")
    start_date = start_date_match.group(1)

    # Extract end date
    end_date_match = re.search(r"End Date:\s * (\d{4}-\d{2}-\d{2})", response)
    if not end_date_match:
        raise ValueError("Could not find end date")
    end_date = end_date_match.group(1)

    # Extract tags
    tags_match = re.search(r"Tags:\s * (.+?)(?:\n|$)", response)
    tags = []
    if tags_match:
        tags = [tag.strip() for tag in tags_match.group(1).split(", ")]

    # Extract notes
    notes_match = re.search(r"Notes:\s * (.+?)(?:\n|$)", response)
    notes = notes_match.group(1).strip() if notes_match else None

    # Create metadata
    return MealPlanMetadata(
        title = title, 
        start_date = start_date, 
        end_date = end_date, 
        tags = tags, 
        hecho = False, 
        notas = notes
)

def parse_meals_response(response: str) -> List[Meal]:
    """Parse LLM response for meal extraction.

    Args:
        response: LLM response

    Returns:
        List[Meal]: Parsed meals

    Raises:
        ValueError: If response cannot be parsed
    """
    meals = []
    current_meal = None

    for line in response.split("\n"):
        line = line.strip()
        if not line:
            continue

        # Check for meal title
        title_match = re.match(r"Title:\s * (.+?)$", line)
        if title_match:
            # Save previous meal if exists
            if current_meal:
                meals.append(current_meal)

            # Start new meal
            current_meal = {
                "title": title_match.group(1).strip(), 
                "type": "", 
                "time": "", 
                "date": "", 
                "recipes": [], 
                "notes": None
            }
            continue

        # Parse meal details
        if current_meal:
            if line.startswith("Type:"):
                current_meal["type"] = line.split(":", 1)[1].strip()
            elif line.startswith("Time:"):
                current_meal["time"] = line.split(":", 1)[1].strip()
            elif line.startswith("Date:"):
                current_meal["date"] = line.split(":", 1)[1].strip()
            elif line.startswith("Recipes:"):
                # Start collecting recipes
                continue
            elif line.startswith("- "):
                # Add recipe
                current_meal["recipes"].append(line.strip("- "))
            elif line.startswith("Notes:"):
                current_meal["notes"] = line.split(":", 1)[1].strip()

    # Add last meal
    if current_meal:
        meals.append(current_meal)

    # Convert to Meal objects
    return [
        Meal(
            title = meal["title"], 
            type = meal["type"], 
            time = meal["time"], 
            date = meal["date"], 
            recipes=[Recipe(title = recipe) for recipe in meal["recipes"]], 
            notes = meal["notes"]
)
        for meal in meals
    ]

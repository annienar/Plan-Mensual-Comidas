"""
Prompt management for LLM tasks.

This module provides a structured way to manage and version prompts used by the LLM client.
Each prompt is versioned and can be easily updated or rolled back if needed.
"""

from datetime import datetime
from typing import Dict, Any

from dataclasses import dataclass, field
from enum import Enum

class PromptTask(Enum):
    """Enumeration of available prompt tasks."""
    RECIPE_PARSER = "recipe_parser"
    INGREDIENT_NORMALIZER = "ingredient_normalizer"
    RECIPE_EXTRACTION = "recipe_extraction"
    MEAL_PLAN_GENERATION = "meal_plan_generation"
    MEAL_PLAN_METADATA_EXTRACTION = "meal_plan_metadata_extraction"
    MEAL_PLAN_MEALS_EXTRACTION = "meal_plan_meals_extraction"

@dataclass

class PromptVersion:
    """Version information for a prompt."""
    version: str
    created_at: datetime
    template: str
    description: str = ""
    author: str = ""
    changes: list[str] = field(default_factory = list)

@dataclass

class Prompt:
    """A prompt with version history."""
    current_version: PromptVersion
    versions: Dict[str, PromptVersion] = field(default_factory = dict)

    def __post_init__(self):
        """Initialize versions dictionary with current version."""
        self.versions[self.current_version.version] = self.current_version

class PromptManager:
    """Manages versioned prompts for different LLM tasks."""

    def __init__(self):
        """Initialize the prompt manager with default prompts."""
        self.prompts: Dict[PromptTask, Prompt] = {
            PromptTask.RECIPE_PARSER: Prompt(
                current_version = PromptVersion(
                    version="1.0.0", 
                    created_at = datetime.now(), 
                    template="""
                    Parse this recipe into JSON with the following structure:
                    {{
                        "title": "string", 
                        "ingredients": [
                            {{"name": "string", "quantity": "string", "unit": "string"}}
                        ], 
                        "steps": ["string"], 
                        "portions": "string", 
                        "calories": "string"
                    }}

                    Recipe:
                    {recipe_text}
                    """, 
                    description="Basic recipe parsing prompt", 
                    author="System"
)
), 
            PromptTask.INGREDIENT_NORMALIZER: Prompt(
                current_version = PromptVersion(
                    version="1.0.0", 
                    created_at = datetime.now(), 
                    template="""
                    Normalize these ingredients into JSON format with name, quantity, and unit:
                    {ingredients_json}

                    Return as a JSON array of objects with structure:
                    [
                        {{"name": "string", "quantity": "string", "unit": "string"}}
                    ]
                    """, 
                    description="Ingredient normalization prompt", 
                    author="System"
)
), 
            PromptTask.RECIPE_EXTRACTION: Prompt(
                current_version = PromptVersion(
                    version="1.0.0", 
                    created_at = datetime.now(), 
                    template="""Extrae la información de la receta del siguiente texto. Asegúrate de:
1. Extraer TODOS los ingredientes mencionados, incluyendo los que aparecen en las instrucciones, combinados con otros, opcionales o en cualquier formato.
2. Para cada ingrediente, proporciona:
- nombre: nombre del ingrediente
- cantidad: cantidad numérica (0.0 si no se especifica)
- unidad: unidad de medida (vacío si no se especifica)
- categoria: categoría del ingrediente (proteínas, vegetales, lácteos, granos, especias, líquidos, otros)
- notas: notas adicionales o especificaciones
- alternativas: ingredientes alternativos si se mencionan
3. El título debe ser conciso, amigable para SEO y en español, sin ningún prefijo.
4. Las instrucciones deben ser claras y numeradas.

Ejemplo de formato esperado:
{
    "metadata": {
        "title": "Pollo al Curry", 
        "servings": 4, 
        "prep_time": 15, 
        "cook_time": 30, 
        "difficulty": "fácil"
    }, 
    "ingredients": [
        {
            "nombre": "pollo", 
            "cantidad": 500, 
            "unidad": "g", 
            "categoria": "proteínas", 
            "notas": "en cubos", 
            "alternativas": []
        }, 
        {
            "nombre": "cebolla", 
            "cantidad": 1, 
            "unidad": "", 
            "categoria": "vegetales", 
            "notas": "picada", 
            "alternativas": []
        }
    ], 
    "instructions": [
        "Cortar el pollo en cubos", 
        "Picar la cebolla finamente"
    ]
}

IMPORTANTE:
- NO omitas ningún ingrediente mencionado
- NO combines ingredientes diferentes
- Asegúrate de asignar una categoría a cada ingrediente
- Si un ingrediente no tiene cantidad o unidad, usa valores vacíos o 0.0
- Si hay ingredientes opcionales, inclúyelos con una nota indicándolo
- Si hay alternativas, inclúyelas en el campo alternativas

Texto de la receta:
{text}""", 
                    description="Spanish recipe extraction prompt", 
                    author="System"
)
), 
            PromptTask.MEAL_PLAN_GENERATION: Prompt(
                current_version = PromptVersion(
                    version="1.0.0", 
                    created_at = datetime.now(), 
                    template="""Generate a recipe for a {meal_type} meal. The recipe should be healthy, easy to prepare, and use common ingredients.

The recipe should include:
1. A descriptive title
2. A list of ingredients with quantities and units
3. Step - by - step instructions
4. Metadata including:
- Number of portions
- Calorie count
- Preparation time
- Cooking time
- Difficulty level
- Tags

Format the recipe in a clear, structured way that can be easily parsed.

Example format:
Title: Grilled Chicken Salad
Ingredients:
- 2 chicken breasts
- 1 head of lettuce
- 1 cucumber
- 1 tomato
- 2 tbsp olive oil
- 1 tbsp balsamic vinegar
- Salt and pepper to taste

Instructions:
1. Season chicken breasts with salt and pepper
2. Grill chicken for 6 - 8 minutes per side
3. Chop lettuce, cucumber, and tomato
4. Slice grilled chicken
5. Combine all ingredients in a bowl
6. Drizzle with olive oil and balsamic vinegar
7. Toss and serve

Metadata:
- Portions: 2
- Calories: 350
- Preparation time: 15 minutes
- Cooking time: 15 minutes
- Difficulty: Easy
- Tags: healthy, quick, lunch, salad""", 
                    description="Meal plan recipe generation prompt", 
                    author="System"
)
), 
            PromptTask.MEAL_PLAN_METADATA_EXTRACTION: Prompt(
                current_version = PromptVersion(
                    version="1.0.0", 
                    created_at = datetime.now(), 
                    template="""Extract meal plan metadata from the following text. The metadata should include:
1. Title
2. Start date (YYYY - MM - DD)
3. End date (YYYY - MM - DD)
4. Tags
5. Notes (if any)

Text:
{text}

Format the metadata in a clear, structured way that can be easily parsed.

Example format:
Title: Weekly Meal Plan
Start Date: 2024 - 03 - 18
End Date: 2024 - 03 - 24
Tags: healthy, quick, family - friendly
Notes: Focus on quick and easy meals for busy weekdays""", 
                    description="Meal plan metadata extraction prompt", 
                    author="System"
)
), 
            PromptTask.MEAL_PLAN_MEALS_EXTRACTION: Prompt(
                current_version = PromptVersion(
                    version="1.0.0", 
                    created_at = datetime.now(), 
                    template="""Extract meals from the following text. Each meal should include:
1. Title
2. Type (breakfast, lunch, dinner)
3. Time (HH:MM)
4. Date (YYYY - MM - DD)
5. List of recipes
6. Notes (if any)

Text:
{text}

Format the meals in a clear, structured way that can be easily parsed.

Example format:
Title: Monday Breakfast
Type: breakfast
Time: 08:00
Date: 2024 - 03 - 18
Recipes:
- Oatmeal with Berries
- Greek Yogurt with Honey
Notes: Prepare oatmeal the night before

Title: Monday Lunch
Type: lunch
Time: 13:00
Date: 2024 - 03 - 18
Recipes:
- Grilled Chicken Salad
- Whole Grain Bread
Notes: Pack lunch in advance""", 
                    description="Meal plan meals extraction prompt", 
                    author="System"
)
)
        }

    def get_prompt(self, task: PromptTask, **kwargs) -> str:
        """Get a formatted prompt for the specified task.

        Args:
            task: The prompt task to get
            **kwargs: Format arguments for the prompt template

        Returns:
            str: The formatted prompt

        Raises:
            ValueError: If the task is unknown
        """
        if task not in self.prompts:
            raise ValueError(f"Unknown prompt task: {task}")

        return self.prompts[task].current_version.template.format(**kwargs)

    def get_prompt_version(self, task: PromptTask) -> str:
        """Get the current version of a prompt.

        Args:
            task: The prompt task to get the version for

        Returns:
            str: The current version

        Raises:
            ValueError: If the task is unknown
        """
        if task not in self.prompts:
            raise ValueError(f"Unknown prompt task: {task}")

        return self.prompts[task].current_version.version

    def add_prompt_version(
        self, 
        task: PromptTask, 
        version: str, 
        template: str, 
        description: str = "", 
        author: str = "", 
        changes: list[str] = None
) -> None:
        """Add a new version of a prompt.

        Args:
            task: The prompt task to add a version for
            version: The version string
            template: The prompt template
            description: Description of the prompt
            author: Author of the prompt
            changes: List of changes from previous version

        Raises:
            ValueError: If the task is unknown or version already exists
        """
        if task not in self.prompts:
            raise ValueError(f"Unknown prompt task: {task}")

        if version in self.prompts[task].versions:
            raise ValueError(f"Version {version} already exists for task {task}")

        prompt_version = PromptVersion(
            version = version, 
            created_at = datetime.now(), 
            template = template, 
            description = description, 
            author = author, 
            changes = changes or []
)

        self.prompts[task].versions[version] = prompt_version
        self.prompts[task].current_version = prompt_version

    def rollback_prompt(self, task: PromptTask, version: str) -> None:
        """Rollback a prompt to a previous version.

        Args:
            task: The prompt task to rollback
            version: The version to rollback to

        Raises:
            ValueError: If the task is unknown or version doesn't exist
        """
        if task not in self.prompts:
            raise ValueError(f"Unknown prompt task: {task}")

        if version not in self.prompts[task].versions:
            raise ValueError(f"Version {version} doesn't exist for task {task}")

        self.prompts[task].current_version = self.prompts[task].versions[version]

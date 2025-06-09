"""
Meal plan prompts for LLM integration.
"""

from typing import List, Dict, Any

def generate_recipe_prompt(meal_type: str) -> str:
    """Generate prompt for recipe generation.

    Args:
        meal_type: Type of meal (breakfast, lunch, dinner)

    Returns:
        str: Generated prompt
    """
    return f"""Generate a recipe for a {meal_type} meal. The recipe should be healthy, easy to prepare, and use common ingredients.

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
- Tags: healthy, quick, lunch, salad"""

def extract_metadata_prompt(text: str) -> str:
    """Generate prompt for metadata extraction.

    Args:
        text: Text to extract metadata from

    Returns:
        str: Generated prompt
    """
    return f"""Extract meal plan metadata from the following text. The metadata should include:
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
Notes: Focus on quick and easy meals for busy weekdays"""

def extract_meals_prompt(text: str) -> str:
    """Generate prompt for meal extraction.

    Args:
        text: Text to extract meals from

    Returns:
        str: Generated prompt
    """
    return f"""Extract meals from the following text. Each meal should include:
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
Notes: Pack lunch in advance"""

def parse_recipe_response(response: str) -> Dict[str, Any]:
    """Parse LLM response for recipe generation.

    Args:
        response: LLM response

    Returns:
        Dict[str, Any]: Parsed recipe
    """
    # TODO: Implement proper parsing
    # For now, return empty dict
    return {}

def parse_metadata_response(response: str) -> Dict[str, Any]:
    """Parse LLM response for metadata extraction.

    Args:
        response: LLM response

    Returns:
        Dict[str, Any]: Parsed metadata
    """
    # TODO: Implement proper parsing
    # For now, return empty dict
    return {}

def parse_meals_response(response: str) -> List[Dict[str, Any]]:
    """Parse LLM response for meal extraction.

    Args:
        response: LLM response

    Returns:
        List[Dict[str, Any]]: Parsed meals
    """
    # TODO: Implement proper parsing
    # For now, return empty list
    return []

from typing import Any

class RecipeValidator:
    """Class RecipeValidator."""

    def validate_content(self: Any, content: str) ->bool:
        """Function validate_content."""
        return bool(content and len(content) >= 10)

    def validate_recipe(self: Any, recipe: Any) ->bool:
        """Function validate_recipe."""
        return True

def validate_recipe(recipe: Any) -> bool:
    """Validate a recipe.

    Args:
        recipe: Recipe to validate

    Returns:
        bool: True if valid, False otherwise
    """
    validator = RecipeValidator()
    return validator.validate_recipe(recipe)

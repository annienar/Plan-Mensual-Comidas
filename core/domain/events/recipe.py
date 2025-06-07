"""
Recipe events module.

This module contains recipe - related domain events.
"""

from ..recipe.models.recipe import Recipe
from typing import Dict, Any

from .base import DomainEvent

class RecipeCreated(DomainEvent):
    """Event raised when a recipe is created.

    Attributes:
        recipe: Created recipe
    """

    def __init__(self, recipe: Recipe, metadata: Dict[str, Any] = None):
        """Initialize the event.

        Args:
            recipe: Created recipe
            metadata: Additional event metadata
        """
        super().__init__(metadata)
        self.recipe = recipe

    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary.

        Returns:
            Dict[str, Any]: Event as dictionary
        """
        data = super().to_dict()
        data["recipe"] = self.recipe.dict()
        return data

class RecipeUpdated(DomainEvent):
    """Event raised when a recipe is updated.

    Attributes:
        recipe: Updated recipe
        changes: Changes made to the recipe
    """

    def __init__(
        self, 
        recipe: Recipe, 
        changes: Dict[str, Any], 
        metadata: Dict[str, Any] = None
):
        """Initialize the event.

        Args:
            recipe: Updated recipe
            changes: Changes made to the recipe
            metadata: Additional event metadata
        """
        super().__init__(metadata)
        self.recipe = recipe
        self.changes = changes

    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary.

        Returns:
            Dict[str, Any]: Event as dictionary
        """
        data = super().to_dict()
        data["recipe"] = self.recipe.dict()
        data["changes"] = self.changes
        return data

class RecipeDeleted(DomainEvent):
    """Event raised when a recipe is deleted.

    Attributes:
        recipe_title: Title of deleted recipe
    """

    def __init__(self, recipe_title: str, metadata: Dict[str, Any] = None):
        """Initialize the event.

        Args:
            recipe_title: Title of deleted recipe
            metadata: Additional event metadata
        """
        super().__init__(metadata)
        self.recipe_title = recipe_title

    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary.

        Returns:
            Dict[str, Any]: Event as dictionary
        """
        data = super().to_dict()
        data["recipe_title"] = self.recipe_title
        return data

class RecipeScaled(DomainEvent):
    """Event raised when a recipe is scaled.

    Attributes:
        recipe: Scaled recipe
        original_recipe: Original recipe
        factor: Scaling factor
    """

    def __init__(
        self, 
        recipe: Recipe, 
        original_recipe: Recipe, 
        factor: float, 
        metadata: Dict[str, Any] = None
):
        """Initialize the event.

        Args:
            recipe: Scaled recipe
            original_recipe: Original recipe
            factor: Scaling factor
            metadata: Additional event metadata
        """
        super().__init__(metadata)
        self.recipe = recipe
        self.original_recipe = original_recipe
        self.factor = factor

    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary.

        Returns:
            Dict[str, Any]: Event as dictionary
        """
        data = super().to_dict()
        data["recipe"] = self.recipe.dict()
        data["original_recipe"] = self.original_recipe.dict()
        data["factor"] = self.factor
        return data

"""
Meal plan events module.

This module contains meal plan - related domain events.
"""

from typing import Dict, Any

from ..meal_plan.models.meal import Meal
from ..meal_plan.models.meal_plan import MealPlan
from .base import DomainEvent

class MealPlanCreated(DomainEvent):
    """Event raised when a meal plan is created.

    Attributes:
        meal_plan: Created meal plan
    """

    def __init__(self, meal_plan: MealPlan, metadata: Dict[str, Any] = None):
        """Initialize the event.

        Args:
            meal_plan: Created meal plan
            metadata: Additional event metadata
        """
        super().__init__(metadata)
        self.meal_plan = meal_plan

    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary.

        Returns:
            Dict[str, Any]: Event as dictionary
        """
        data = super().to_dict()
        data["meal_plan"] = self.meal_plan.dict()
        return data

class MealPlanUpdated(DomainEvent):
    """Event raised when a meal plan is updated.

    Attributes:
        meal_plan: Updated meal plan
        changes: Changes made to the meal plan
    """

    def __init__(
        self, 
        meal_plan: MealPlan, 
        changes: Dict[str, Any], 
        metadata: Dict[str, Any] = None
):
        """Initialize the event.

        Args:
            meal_plan: Updated meal plan
            changes: Changes made to the meal plan
            metadata: Additional event metadata
        """
        super().__init__(metadata)
        self.meal_plan = meal_plan
        self.changes = changes

    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary.

        Returns:
            Dict[str, Any]: Event as dictionary
        """
        data = super().to_dict()
        data["meal_plan"] = self.meal_plan.dict()
        data["changes"] = self.changes
        return data

class MealPlanDeleted(DomainEvent):
    """Event raised when a meal plan is deleted.

    Attributes:
        meal_plan_title: Title of deleted meal plan
    """

    def __init__(self, meal_plan_title: str, metadata: Dict[str, Any] = None):
        """Initialize the event.

        Args:
            meal_plan_title: Title of deleted meal plan
            metadata: Additional event metadata
        """
        super().__init__(metadata)
        self.meal_plan_title = meal_plan_title

    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary.

        Returns:
            Dict[str, Any]: Event as dictionary
        """
        data = super().to_dict()
        data["meal_plan_title"] = self.meal_plan_title
        return data

class MealAdded(DomainEvent):
    """Event raised when a meal is added to a meal plan.

    Attributes:
        meal_plan: Meal plan
        meal: Added meal
    """

    def __init__(
        self, 
        meal_plan: MealPlan, 
        meal: Meal, 
        metadata: Dict[str, Any] = None
):
        """Initialize the event.

        Args:
            meal_plan: Meal plan
            meal: Added meal
            metadata: Additional event metadata
        """
        super().__init__(metadata)
        self.meal_plan = meal_plan
        self.meal = meal

    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary.

        Returns:
            Dict[str, Any]: Event as dictionary
        """
        data = super().to_dict()
        data["meal_plan"] = self.meal_plan.dict()
        data["meal"] = self.meal.dict()
        return data

class MealRemoved(DomainEvent):
    """Event raised when a meal is removed from a meal plan.

    Attributes:
        meal_plan: Meal plan
        meal: Removed meal
    """

    def __init__(
        self, 
        meal_plan: MealPlan, 
        meal: Meal, 
        metadata: Dict[str, Any] = None
):
        """Initialize the event.

        Args:
            meal_plan: Meal plan
            meal: Removed meal
            metadata: Additional event metadata
        """
        super().__init__(metadata)
        self.meal_plan = meal_plan
        self.meal = meal

    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary.

        Returns:
            Dict[str, Any]: Event as dictionary
        """
        data = super().to_dict()
        data["meal_plan"] = self.meal_plan.dict()
        data["meal"] = self.meal.dict()
        return data

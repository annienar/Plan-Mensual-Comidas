"""
Event handlers module.

This module contains event handlers.
"""

from datetime import datetime
from typing import Dict, Any, Optional

from .base import DomainEvent
from .recipe import (
    RecipeCreated, 
    RecipeUpdated, 
    RecipeDeleted, 
    RecipeScaled
)
from .meal_plan import (
    MealPlanCreated, 
    MealPlanUpdated, 
    MealPlanDeleted, 
    MealAdded, 
    MealRemoved
)

class EventLogger:
    """Event logger.

    This class logs events to a file.
    """

    def __init__(self, log_file: str = "events.log"):
        """Initialize the logger.

        Args:
            log_file: Path to log file
        """
        self.log_file = log_file

    async def handle_event(self, event: DomainEvent) -> None:
        """Handle any event by logging it.

        Args:
            event: Event to log
        """
        with open(self.log_file, "a") as f:
            f.write(f"{datetime.now().isoformat()} - {event}\n")

class RecipeEventHandler:
    """Recipe event handler.

    This class handles recipe - related events.
    """

    def __init__(self, logger: Optional[EventLogger] = None):
        """Initialize the handler.

        Args:
            logger: Optional event logger
        """
        self.logger = logger

    async def handle_recipe_created(self, event: RecipeCreated) -> None:
        """Handle recipe created event.

        Args:
            event: Recipe created event
        """
        if self.logger:
            await self.logger.handle_event(event)

    async def handle_recipe_updated(self, event: RecipeUpdated) -> None:
        """Handle recipe updated event.

        Args:
            event: Recipe updated event
        """
        if self.logger:
            await self.logger.handle_event(event)

    async def handle_recipe_deleted(self, event: RecipeDeleted) -> None:
        """Handle recipe deleted event.

        Args:
            event: Recipe deleted event
        """
        if self.logger:
            await self.logger.handle_event(event)

    async def handle_recipe_scaled(self, event: RecipeScaled) -> None:
        """Handle recipe scaled event.

        Args:
            event: Recipe scaled event
        """
        if self.logger:
            await self.logger.handle_event(event)

class MealPlanEventHandler:
    """Meal plan event handler.

    This class handles meal plan - related events.
    """

    def __init__(self, logger: Optional[EventLogger] = None):
        """Initialize the handler.

        Args:
            logger: Optional event logger
        """
        self.logger = logger

    async def handle_meal_plan_created(self, event: MealPlanCreated) -> None:
        """Handle meal plan created event.

        Args:
            event: Meal plan created event
        """
        if self.logger:
            await self.logger.handle_event(event)

    async def handle_meal_plan_updated(self, event: MealPlanUpdated) -> None:
        """Handle meal plan updated event.

        Args:
            event: Meal plan updated event
        """
        if self.logger:
            await self.logger.handle_event(event)

    async def handle_meal_plan_deleted(self, event: MealPlanDeleted) -> None:
        """Handle meal plan deleted event.

        Args:
            event: Meal plan deleted event
        """
        if self.logger:
            await self.logger.handle_event(event)

    async def handle_meal_added(self, event: MealAdded) -> None:
        """Handle meal added event.

        Args:
            event: Meal added event
        """
        if self.logger:
            await self.logger.handle_event(event)

    async def handle_meal_removed(self, event: MealRemoved) -> None:
        """Handle meal removed event.

        Args:
            event: Meal removed event
        """
        if self.logger:
            await self.logger.handle_event(event)

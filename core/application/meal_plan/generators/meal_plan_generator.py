"""
Meal plan generation service.
"""
from core.domain.meal_plan.models.meal import Meal
from core.domain.meal_plan.models.meal_plan import MealPlan
from core.domain.meal_plan.models.metadata import MealPlanMetadata
from core.domain.recipe.models.recipe import Recipe
from core.infrastructure.llm.client import LLMClient
from core.infrastructure.llm.parsers.meal_plan import parse_recipe_response
from core.infrastructure.llm.prompts import PromptManager, PromptTask
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any

from pydantic import BaseModel, Field

class MealPlanGenerationRequest(BaseModel):
    """Meal plan generation request.

    Attributes:
        title: Meal plan title
        start_date: Start date
        end_date: End date
        tags: Meal plan tags
        notes: Additional notes
    """
    title: str = Field(..., min_length = 3, max_length = 200, description=
        'Meal plan title')
    start_date: str = Field(..., description='Start date in YYYY - MM - DD format')
    end_date: str = Field(..., description='End date in YYYY - MM - DD format')
    tags: List[str] = Field(default_factory = list, description='Meal plan tags')
    notes: Optional[str] = Field(None, description='Additional notes')

class MealPlanGenerationService:
    """Meal plan generation service.

    This service is responsible for generating meal plans using LLMs.
    """

    def __init__(self: Any, llm_client: LLMClient) -> None:
        """Initialize the service.

        Args:
            llm_client: LLM client
        """
        self.llm_client = llm_client
        self.prompt_manager = PromptManager()

    async def generate_meal_plan(self, request: MealPlanGenerationRequest
) ->MealPlan:
        """Generate a meal plan.

        Args:
            request: Generation request

        Returns:
            MealPlan: Generated meal plan

        Raises:
            ValueError: If request is invalid
        """
        start_date = datetime.strptime(request.start_date, '%Y-%m-%d')
        end_date = datetime.strptime(request.end_date, '%Y-%m-%d')
        if end_date < start_date:
            raise ValueError('End date must be after start date')
        meals = []
        current_date = start_date
        while current_date <= end_date:
            day_meals = await self._generate_day_meals(current_date)
            meals.extend(day_meals)
            current_date += timedelta(days = 1)
        metadata = MealPlanMetadata(title = request.title, start_date = request
            .start_date, end_date = request.end_date, tags = request.tags, 
            hecho = False, notas = request.notes)
        return MealPlan(title = request.title, meals = meals, metadata = metadata)

    async def _generate_day_meals(self, date: datetime) ->List[Meal]:
        """Generate meals for a day.

        Args:
            date: Date to generate meals for

        Returns:
            List[Meal]: Generated meals
        """
        breakfast = await self._generate_meal(title='Breakfast', type=
            'breakfast', time='08:00', date = date.strftime('%Y-%m-%d'))
        lunch = await self._generate_meal(title='Lunch', type='lunch', time
            ='13:00', date = date.strftime('%Y-%m-%d'))
        dinner = await self._generate_meal(title='Dinner', type='dinner', 
            time='20:00', date = date.strftime('%Y-%m-%d'))
        return [breakfast, lunch, dinner]

    async def _generate_meal(self, title: str, type: str, time: str, date: str
) ->Meal:
        """Generate a meal.

        Args:
            title: Meal title
            type: Meal type
            time: Meal time
            date: Meal date

        Returns:
            Meal: Generated meal
        """
        recipes = await self._generate_recipes(type)
        return Meal(title = title, type = type, time = time, date = date, recipes=
            recipes)

    async def _generate_recipes(self, meal_type: str) ->List[Recipe]:
        """Generate recipes for a meal type.

        Args:
            meal_type: Meal type

        Returns:
            List[Recipe]: Generated recipes
        """
        prompt = self.prompt_manager.get_prompt(PromptTask.
            MEAL_PLAN_GENERATION, meal_type = meal_type)
        response = await self.llm_client.generate(prompt)
        try:
            recipe = parse_recipe_response(response)
            return [recipe]
        except ValueError as e:
            print(f'Error parsing recipe response: {e}')
            return []

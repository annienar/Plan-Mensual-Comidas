"""
Meal plan extraction service.
"""
from core.domain.meal_plan.models.meal import Meal
from core.domain.meal_plan.models.meal_plan import MealPlan
from core.domain.meal_plan.models.metadata import MealPlanMetadata
from core.domain.recipe.models.recipe import Recipe
from core.infrastructure.llm.client import LLMClient
from core.infrastructure.llm.parsers.meal_plan import parse_metadata_response, parse_meals_response
from core.infrastructure.llm.prompts import PromptManager, PromptTask
from datetime import datetime
from typing import List, Optional, Dict, Any

from pydantic import BaseModel, Field

class MealPlanExtractionRequest(BaseModel):
    """Meal plan extraction request.

    Attributes:
        text: Text to extract meal plan from
    """
    text: str = Field(..., min_length = 1, description=
        'Text to extract meal plan from')

class MealPlanExtractionService:
    """Meal plan extraction service.

    This service is responsible for extracting meal plans from text using LLMs.
    """

    def __init__(self: Any, llm_client: LLMClient) -> None:
        """Initialize the service.

        Args:
            llm_client: LLM client
        """
        self.llm_client = llm_client
        self.prompt_manager = PromptManager()

    async def extract_meal_plan(self, request: MealPlanExtractionRequest
) ->MealPlan:
        """Extract a meal plan from text.

        Args:
            request: Extraction request

        Returns:
            MealPlan: Extracted meal plan

        Raises:
            ValueError: If request is invalid
        """
        metadata = await self._extract_metadata(request.text)
        meals = await self._extract_meals(request.text)
        return MealPlan(title = metadata.title, meals = meals, metadata = metadata)

    async def _extract_metadata(self, text: str) ->MealPlanMetadata:
        """Extract metadata from text.

        Args:
            text: Text to extract metadata from

        Returns:
            MealPlanMetadata: Extracted metadata
        """
        prompt = self.prompt_manager.get_prompt(PromptTask.
            MEAL_PLAN_METADATA_EXTRACTION, text = text)
        response = await self.llm_client.generate(prompt)
        try:
            return parse_metadata_response(response)
        except ValueError as e:
            print(f'Error parsing metadata response: {e}')
            return MealPlanMetadata(title='Extracted Meal Plan', start_date
                =datetime.now().strftime('%Y-%m-%d'), end_date = datetime.now
                ().strftime('%Y-%m-%d'), tags=[], hecho = False)

    async def _extract_meals(self, text: str) ->List[Meal]:
        """Extract meals from text.

        Args:
            text: Text to extract meals from

        Returns:
            List[Meal]: Extracted meals
        """
        prompt = self.prompt_manager.get_prompt(PromptTask.
            MEAL_PLAN_MEALS_EXTRACTION, text = text)
        response = await self.llm_client.generate(prompt)
        try:
            return parse_meals_response(response)
        except ValueError as e:
            print(f'Error parsing meals response: {e}')
            return []

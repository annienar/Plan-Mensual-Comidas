"""
LLM-based recipe extractor that uses Ollama with Phi model for accurate recipe parsing.
"""
from core.domain.recipe.extractors.base import BaseExtractor
from core.domain.recipe.models import Recipe, Ingredient
from core.domain.recipe.models.metadata import RecipeMetadata
from core.exceptions import RecipeError
from core.infrastructure.llm.client import LLMClient
from core.utils.logger import get_logger
from typing import Dict, List, Any, Optional
import json
from datetime import datetime

logger = get_logger(__name__)

class LLMExtractor(BaseExtractor):
    """LLM-based recipe extractor using Ollama with Phi model."""

    def __init__(self, llm_client: Optional[LLMClient] = None) -> None:
        """Initialize the LLM extractor with an optional LLM client."""
        self.llm_client = llm_client or LLMClient(model="phi")
        self.system_prompt = """You are a recipe extraction expert specializing in Spanish cuisine. Your task is to analyze recipe text and extract structured information. 

IMPORTANT TRANSLATION REQUIREMENTS:
- If the recipe text contains ANY content in English, translate it to Spanish
- ALL extracted content must be in Spanish (titles, ingredients, instructions, notes)
- Maintain culinary authenticity and proper Spanish terminology
- Use proper Spanish cooking terms and measurements when applicable
- Always respond with valid JSON only."""

    async def extract_recipe(self, text: str) -> Recipe:
        """Extract recipe information using LLM."""
        try:
            # Use the structured completion method for better JSON handling
            data = await self.llm_client.get_structured_completion(
                prompt=self._build_extraction_prompt(text),
                required_fields=['title', 'ingredients', 'instructions'],
                numeric_fields=['servings', 'prep_time', 'cook_time', 'calories'],
                array_fields=['ingredients', 'instructions', 'tags'],
                system_prompt=self.system_prompt
            )
            
            return self._create_recipe_from_data(data)
            
        except Exception as e:
            logger.error(f'Error in LLM extraction: {str(e)}')
            raise RecipeError(f'Failed to extract recipe: {str(e)}')

    def _build_extraction_prompt(self, text: str) -> str:
        """Build the extraction prompt for the LLM."""
        return f"""Extract recipe information from the following text and return it as JSON with this exact structure:

{{
  "title": "Recipe title",
  "servings": 4,
  "prep_time": 15,
  "cook_time": 30,
  "difficulty": "easy/medium/hard",
  "calories": 250,
  "tags": ["tag1", "tag2"],
  "ingredients": [
    {{
      "name": "ingredient name",
      "quantity": 2.0,
      "unit": "cups",
      "category": "vegetable/protein/grain/dairy/spice/other"
    }}
  ],
  "instructions": [
    "Step 1 description",
    "Step 2 description"
  ],
  "notes": "Any additional notes or tips"
}}

Recipe text:
{text}

Important:
- **TRANSLATE TO SPANISH**: If any content is in English, translate it to Spanish. Examples:
  * "chicken" → "pollo", "beef" → "carne", "onion" → "cebolla"
  * "Preheat oven" → "Precalentar horno"
  * "Mix ingredients" → "Mezclar ingredientes"
- Extract exact ingredient quantities and convert fractions to decimals (1/2 = 0.5, 1 1/2 = 1.5)
- Normalize units to standard forms (tbsp, tsp, cup, oz, lb, kg, g, ml, l)
- Categorize ingredients appropriately
- Keep instructions as separate, clear steps
- If information is missing, use reasonable defaults
- Ensure all numeric fields are numbers, not strings"""

    def _create_recipe_from_data(self, data: Dict[str, Any]) -> Recipe:
        """Create a Recipe object from LLM extraction data."""
        # Ensure we have a meaningful title
        # Check both top-level and metadata for title
        title = data.get('title', '').strip()
        if not title:
            title = data.get('metadata', {}).get('title', '').strip()
        
        if not title or title.lower() in ['recipe title', 'sin título', 'untitled']:
            # Generate title from ingredients if none provided
            title = self._generate_title_from_ingredients(data.get('ingredients', []))
        
        # Create metadata - prioritize metadata section, fallback to top-level
        metadata_data = data.get('metadata', {})
        metadata = RecipeMetadata(
            title=title,
            tags=metadata_data.get('tags', data.get('tags', ['general'])),
            date=datetime.now().strftime("%Y-%m-%d"),  # Use proper date format
            porciones=metadata_data.get('servings', data.get('servings', 4)),
            tiempo_preparacion=metadata_data.get('prep_time', data.get('prep_time', 0)),
            tiempo_coccion=metadata_data.get('cook_time', data.get('cook_time', 0)),
            tiempo_total=max(1, metadata_data.get('prep_time', data.get('prep_time', 0)) + metadata_data.get('cook_time', data.get('cook_time', 0))),  # Ensure > 0
            dificultad=self._normalize_difficulty(metadata_data.get('difficulty', data.get('difficulty', 'media'))),
            calorias=metadata_data.get('calories', data.get('calories', 0)),
            notas=metadata_data.get('notes', data.get('notes', ''))
        )

        # Create ingredients
        ingredients = []
        for ing_data in data.get('ingredients', []):
            ingredient = Ingredient(
                nombre=ing_data.get('name', ''),
                cantidad=float(ing_data.get('quantity', 0)),
                unidad=ing_data.get('unit', ''),
                notas=ing_data.get('notes', ''),
                alternativas=ing_data.get('alternatives', [])
            )
            ingredients.append(ingredient)

        # Create recipe
        recipe = Recipe(
            title=title,
            metadata=metadata,
            ingredients=ingredients,
            instructions=data.get('instructions', [])
        )
        
        return recipe

    def _generate_title_from_ingredients(self, ingredients: List[Dict[str, Any]]) -> str:
        """Generate a title based on ingredient list."""
        if not ingredients:
            return 'Receta Casera'
        
        # Get main ingredients
        main_ingredients = []
        for ing in ingredients[:3]:  # Take first 3 ingredients
            name = ing.get('name', '').strip()
            if name:
                main_ingredients.append(name.title())
        
        if len(main_ingredients) >= 2:
            if len(main_ingredients) == 2:
                return f"{main_ingredients[0]} con {main_ingredients[1]}"
            else:
                return f"{main_ingredients[0]} con {main_ingredients[1]} y {main_ingredients[2]}"
        elif len(main_ingredients) == 1:
            return f"Receta de {main_ingredients[0]}"
        else:
            return 'Receta Casera'

    def _normalize_difficulty(self, difficulty: str) -> str:
        """Normalize difficulty level to match model expectations."""
        difficulty_lower = difficulty.lower().strip()
        
        if difficulty_lower in ['easy', 'fácil', 'facil']:
            return 'Fácil'
        elif difficulty_lower in ['medium', 'media', 'medio']:
            return 'Media'
        elif difficulty_lower in ['hard', 'difficult', 'difícil', 'dificil']:
            return 'Difícil'
        else:
            return 'Media'  # Default to medium

    async def extract(self, text: str) -> Dict[str, Any]:
        """Extract recipe information from text using LLM.

        Args:
            text: Recipe text to extract from

        Returns:
            Dict containing extracted recipe information

        Raises:
            RecipeError: If extraction fails
        """
        try:
            # Use structured completion for better reliability
            result = await self.llm_client.get_structured_completion(
                prompt=self._build_detailed_prompt(text),
                required_fields=['metadata', 'ingredients', 'instructions'],
                array_fields=['ingredients', 'instructions'],
                system_prompt=self.system_prompt
            )
            
            return result
            
        except Exception as e:
            logger.error(f'Error in LLM extraction: {str(e)}')
            # Return fallback structure instead of raising exception
            return self._get_fallback_result(text, str(e))

    def _build_detailed_prompt(self, text: str) -> str:
        """Build a detailed extraction prompt."""
        return f"""Extract complete recipe information from the following text and return it as JSON:

{{
  "metadata": {{
    "title": "Recipe title",
    "servings": 4,
    "prep_time": 15,
    "cook_time": 30,
    "difficulty": "easy",
    "calories": 250,
    "tags": ["main dish", "vegetarian"],
    "notes": "Additional notes"
  }},
  "ingredients": [
    {{
      "name": "ingredient name",
      "quantity": 2.0,
      "unit": "cups",
      "category": "vegetable",
      "notes": "optional preparation notes"
    }}
  ],
  "instructions": [
    "Step 1: Detailed instruction",
    "Step 2: Next step"
  ]
}}

Recipe text:
{text}

Guidelines:
- **MANDATORY TRANSLATION**: If the recipe contains ANY English text, translate ALL content to Spanish:
  * Ingredients: "chicken breast" → "pechuga de pollo", "olive oil" → "aceite de oliva"
  * Instructions: "Heat the pan" → "Calentar la sartén", "Season with salt" → "Sazonar con sal"
  * Titles: "Chicken Soup" → "Sopa de Pollo", "Beef Stew" → "Estofado de Carne"
  * Use proper Spanish culinary terminology
- **TITLE CREATION**: If no clear title is provided, create an appealing and descriptive title based on the main ingredients and cooking method. Examples:
  * "Chicken with rice" → "Pollo con Arroz al Cilantro"
  * "Pasta with tomatoes" → "Pasta con Tomates Frescos"
  * "Soup with vegetables" → "Sopa de Verduras Casera"
  * Use Spanish titles when appropriate, make them appetizing and specific
- Convert all fractions to decimals (1/2 = 0.5, 2 1/3 = 2.33)
- Use standard units: tsp, tbsp, cup, oz, lb, kg, g, ml, l
- Categories: vegetable, fruit, protein, grain, dairy, spice, condiment, other
- Split multi-sentence instructions into separate steps
- Use "easy", "medium", or "hard" for difficulty
- Extract realistic calorie estimates if mentioned
- Always provide a meaningful, appetizing title even if the original text doesn't have one"""

    def _get_fallback_result(self, content: str = '', reason: str = 'Unknown error') -> Dict[str, Any]:
        """Return a fallback result when LLM extraction fails."""
        title = self._extract_title_fallback(content)
        
        return {
            'metadata': {
                'title': title,
                'servings': 4,
                'prep_time': 0,
                'cook_time': 0,
                'difficulty': 'medium',
                'calories': 0,
                'tags': ['general'],
                'notes': f'Error en extracción automática: {reason}'
            },
            'ingredients': [{
                'name': 'ingrediente base',
                'quantity': 1.0,
                'unit': '',
                'category': 'other',
                'notes': f'Error en extracción: {reason}'
            }],
            'instructions': [
                f'Error en la extracción automática: {reason}',
                'Por favor, revisar la receta original para obtener los ingredientes y pasos correctos.'
            ],
            'confidence': 0.1  # Low confidence for fallback
        }

    def _extract_title_fallback(self, content: str) -> str:
        """Extract title using intelligent text parsing as fallback."""
        lines = content.splitlines()
        
        # First, look for explicit title patterns
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Look for title patterns
            if line.lower().startswith('título:'):
                return line[7:].strip()
            elif line.lower().startswith('title:'):
                return line[6:].strip()
            elif line.lower().startswith('recipe:'):
                return line[7:].strip()
            elif len(line) < 100 and not any(word in line.lower() for word in ['ingredientes', 'ingredients', 'preparación', 'instructions', 'pasos']):
                # Likely a title if it's short and doesn't contain ingredient/instruction keywords
                return line
        
        # If no explicit title found, generate one based on ingredients
        return self._generate_title_from_content(content)

    def _generate_title_from_content(self, content: str) -> str:
        """Generate an intelligent title based on recipe content."""
        # Extract main ingredients
        main_ingredients = []
        lines = content.lower().splitlines()
        
        # Common main ingredients to look for
        protein_keywords = ['pollo', 'chicken', 'carne', 'beef', 'cerdo', 'pork', 'pescado', 'fish', 'camarones', 'shrimp']
        carb_keywords = ['arroz', 'rice', 'pasta', 'papas', 'potatoes', 'pan', 'bread']
        cooking_methods = ['al horno', 'baked', 'frito', 'fried', 'asado', 'grilled', 'guisado', 'stewed']
        
        found_protein = None
        found_carb = None
        found_method = None
        
        content_lower = content.lower()
        
        # Find main protein
        for protein in protein_keywords:
            if protein in content_lower:
                found_protein = protein
                break
                
        # Find main carb
        for carb in carb_keywords:
            if carb in content_lower:
                found_carb = carb
                break
                
        # Find cooking method
        for method in cooking_methods:
            if method in content_lower:
                found_method = method
                break
        
        # Generate title based on findings
        if found_protein and found_carb:
            if found_protein == 'pollo':
                return f"Pollo con {found_carb.title()}"
            elif found_protein == 'chicken':
                return f"Chicken with {found_carb.title()}"
            elif found_protein == 'carne':
                return f"Carne con {found_carb.title()}"
            else:
                return f"{found_protein.title()} con {found_carb.title()}"
        elif found_protein:
            if found_method:
                return f"{found_protein.title()} {found_method}"
            else:
                return f"Receta de {found_protein.title()}"
        elif found_carb:
            return f"Receta de {found_carb.title()}"
        else:
            # Look for any obvious food words
            food_words = ['sopa', 'soup', 'ensalada', 'salad', 'postre', 'dessert', 'torta', 'cake']
            for food in food_words:
                if food in content_lower:
                    return f"Receta de {food.title()}"
            
            return 'Receta Casera'

    async def extract_with_confidence(self, text: str) -> Dict[str, Any]:
        """Extract recipe with confidence scoring."""
        try:
            result = await self.extract(text)
            
            # Calculate confidence based on completeness
            confidence = self._calculate_confidence(result)
            result['confidence'] = confidence
            
            return result
            
        except Exception as e:
            logger.error(f'Error in confident extraction: {str(e)}')
            fallback = self._get_fallback_result(text, str(e))
            fallback['confidence'] = 0.1  # Very low confidence for fallback
            return fallback

    def _calculate_confidence(self, result: Dict[str, Any]) -> float:
        """Calculate extraction confidence score."""
        confidence = 0.0
        
        # Check metadata completeness
        metadata = result.get('metadata', {})
        if metadata.get('title') and metadata['title'] != 'Receta Sin Título':
            confidence += 0.2
        if metadata.get('servings', 0) > 0:
            confidence += 0.1
        if metadata.get('prep_time', 0) > 0 or metadata.get('cook_time', 0) > 0:
            confidence += 0.1
            
        # Check ingredients
        ingredients = result.get('ingredients', [])
        if len(ingredients) > 0:
            confidence += 0.3
            # Bonus for complete ingredient info
            complete_ingredients = sum(1 for ing in ingredients 
                                     if ing.get('name') and ing.get('quantity', 0) > 0)
            if complete_ingredients == len(ingredients):
                confidence += 0.2
                
        # Check instructions
        instructions = result.get('instructions', [])
        if len(instructions) > 0:
            confidence += 0.2
            
        return min(confidence, 1.0)

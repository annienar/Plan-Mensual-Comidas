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
import time
import logging

logger = logging.getLogger(__name__)

# Performance metrics for llava-phi3 optimization
PERFORMANCE_METRICS = {
    'extraction_times': [],
    'prompt_lengths': [],
    'success_rate': 0,
    'cache_hits': 0
}

class LLMExtractor(BaseExtractor):
    """LLM-based recipe extractor using llava-phi3 with configurable language support."""

    def __init__(self, llm_client: Optional[LLMClient] = None, language: str = "spanish") -> None:
        """Initialize the LLM extractor with an optional LLM client."""
        # Use longer timeout for llava-phi3 model
        self.llm_client = llm_client or LLMClient(model="llava-phi3", timeout=120)
        self.language = language  # Always "spanish" for this system
        
        # System always forces Spanish translation for consistency
        self.system_prompt = """Eres un experto en extracción de recetas que SIEMPRE traduce todo al español. Tu tarea es analizar cualquier texto de receta (en cualquier idioma) y extraer información estructurada completamente en español.

TRADUCCIÓN OBLIGATORIA:
- TODO el contenido debe estar en español, sin excepción
- Traduce ingredientes: "chicken" → "pollo", "beef" → "carne", "onion" → "cebolla"
- Traduce instrucciones: "Heat the pan" → "Calentar la sartén", "Mix well" → "Mezclar bien"
- Traduce títulos: "Chicken Soup" → "Sopa de Pollo", "Beef Stew" → "Estofado de Carne"
- Usa terminología culinaria española auténtica
- Propiedades para Notion: nombre, porciones, calorias, dificultad (en español)
- Unidades en español: taza, cda, cdta, g, kg, ml, l
- Responde únicamente con JSON válido en español"""

    @classmethod
    def for_notion(cls) -> 'LLMExtractor':
        """Create an extractor for Notion integration (always Spanish)."""
        return cls(language="spanish")
    
    @classmethod  
    def create(cls) -> 'LLMExtractor':
        """Create a standard extractor (always Spanish)."""
        return cls(language="spanish")

    async def extract_recipe(self, text: str) -> Recipe:
        """Extract recipe information using optimized llava-phi3."""
        start_time = time.time()
        try:
            # Use optimized structured completion for llava-phi3
            data = await self.llm_client.get_structured_completion(
                prompt=self._build_extraction_prompt(text),
                required_fields=['title', 'ingredients', 'instructions'],
                numeric_fields=['servings', 'prep_time', 'cook_time', 'calories'],
                array_fields=['ingredients', 'instructions', 'tags'],
                system_prompt=self.system_prompt
            )
            
            # Track performance metrics
            extraction_time = time.time() - start_time
            logger.info(f"llava-phi3 extraction completed in {extraction_time:.2f}s")
            
            return self._create_recipe_from_data(data)
            
        except Exception as e:
            extraction_time = time.time() - start_time
            logger.error(f'llava-phi3 extraction failed after {extraction_time:.2f}s: {str(e)}')
            raise RecipeError(f'Failed to extract recipe: {str(e)}')

    def _build_extraction_prompt(self, text: str) -> str:
        """Build Spanish-only extraction prompt for llava-phi3."""
        
        return f"""Extrae información de esta receta y devuelve TODO en español:

{{
  "title": "Título en Español",
  "servings": 4,
  "prep_time": 15,
  "cook_time": 30,
  "difficulty": "fácil",
  "calories": 250,
  "tags": ["etiqueta1", "etiqueta2"],
  "ingredients": [
    {{
      "name": "nombre en español",
      "quantity": 2.0,
      "unit": "taza",
      "category": "proteína"
    }}
  ],
  "instructions": [
    "Paso 1 en español",
    "Paso 2 en español"
  ],
  "notes": "Notas en español"
}}

Texto de receta (puede estar en cualquier idioma):
{text}

REGLAS DE TRADUCCIÓN:
- SIEMPRE traduce TODO al español, sin excepción
- Ingredientes: chicken→pollo, beef→carne, onion→cebolla, garlic→ajo, oil→aceite
- Acciones: heat→calentar, mix→mezclar, add→agregar, cook→cocinar, serve→servir
- Unidades: cup→taza, tbsp→cda, tsp→cdta, lb→libra, oz→onza
- Convierte fracciones a decimales (1/2 = 0.5)
- Categorías: proteína, vegetal, grano, lácteo, especia, condimento, otro
- Dificultad: fácil, media, difícil
- Instrucciones claras y numeradas en español"""

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
        """Build Spanish-only detailed prompt for llava-phi3."""
        
        return f"""Extrae información completa de esta receta y traduce TODO al español:

{{
  "metadata": {{
    "title": "Título atractivo en español",
    "servings": 4,
    "prep_time": 15,
    "cook_time": 30,
    "difficulty": "fácil",
    "calories": 250,
    "tags": ["plato principal", "vegetariano"],
    "notes": "Notas adicionales"
  }},
  "ingredients": [
    {{
      "name": "nombre ingrediente en español",
      "quantity": 2.0,
      "unit": "taza",
      "category": "vegetal",
      "notes": "notas preparación"
    }}
  ],
  "instructions": [
    "Paso 1: Instrucción detallada",
    "Paso 2: Siguiente paso"
  ]
}}

Texto de receta (cualquier idioma):
{text}

REGLAS DE TRADUCCIÓN FORZADA:
- SIEMPRE traduce TODO al español, sin excepción
- Ingredientes: chicken→pollo, beef→carne, onion→cebolla, garlic→ajo, oil→aceite, salt→sal, pepper→pimienta
- Verbos: heat→calentar, mix→mezclar, add→agregar, cook→cocinar, serve→servir, cut→cortar, season→sazonar
- Títulos creativos: "Chicken Rice"→"Pollo con Arroz al Cilantro", "Beef Stew"→"Estofado de Carne con Vegetales"
- Unidades: cup→taza, tbsp→cda, tsp→cdta, lb→libra, oz→onza
- Fracciones a decimales: 1/2=0.5, 1/4=0.25, 3/4=0.75
- Categorías: vegetal, fruta, proteína, grano, lácteo, especia, condimento, otro
- Instrucciones separadas y detalladas en español
- Dificultad: fácil/media/difícil
- Título siempre atractivo y específico en español"""

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

"""
Generate Notion blocks for a recipe.
"""
from core.domain.recipe.models.metadata import RecipeMetadata
from core.domain.recipe.models.recipe import Recipe
from typing import List, Dict, Any, Optional
MAX_TEXT_LENGTH = 2000

# Define difficulty enum here since it doesn't exist elsewhere
from enum import Enum

class Difficulty(Enum):
    """Difficulty levels for recipes."""
    FACIL = "Fácil"
    MEDIA = "Media"
    DIFICIL = "Difícil"

class RecipeType(Enum):
    """Recipe types."""
    DESAYUNO = 'Desayuno'
    ALMUERZO = 'Almuerzo'
    CENA = 'Cena'
    POSTRE = 'Postre'
    SNACK = 'Snack'
    BEBIDA = 'Bebida'
    OTRO = 'Otro'

def truncate_text(text: str, max_length: int = MAX_TEXT_LENGTH) ->str:
    """
    Truncate text to fit Notion's limits.

    Args:
        text: Text to truncate
        max_length: Maximum length allowed

    Returns:
        Truncated text with ellipsis if needed
    """
    if not text:
        return ''
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + '...'

def recipe_to_notion_blocks(recipe: Recipe) ->List[Dict[str, Any]]:
    """
    Generate Notion blocks for a recipe.

    Args:
        recipe: Recipe instance to convert to Notion blocks

    Returns:
        List of Notion blocks

    Raises:
        ValueError: If recipe is invalid or empty
    """
    if not isinstance(recipe, Recipe):
        raise ValueError('recipe must be a Recipe instance')
    if not recipe.title:
        raise ValueError('recipe must have a title')
    if not recipe.ingredients:
        raise ValueError('recipe must have at least one ingredient')
    if not recipe.instructions:
        raise ValueError('recipe must have at least one instruction')
    blocks = []
    blocks.append({'object': 'block', 'type': 'heading_1', 'heading_1': {
        'rich_text': [{'type': 'text', 'text': {'content': truncate_text(
        recipe.title)}}]}})
    metadata_blocks = []
    if recipe.source_url:
        metadata_blocks.append({'object': 'block', 'type': 'paragraph', 
            'paragraph': {'rich_text': [{'type': 'text', 'text': {'content':
            'Source: '}}, {'type': 'text', 'text': {'content':
            truncate_text(recipe.source_url), 'link': {'url': recipe.
            source_url}}}]}})
    if recipe.porciones:
        metadata_blocks.append({'object': 'block', 'type': 'paragraph', 
            'paragraph': {'rich_text': [{'type': 'text', 'text': {'content':
            f'Portions: {recipe.porciones}'}}]}})
    if recipe.calorias:
        metadata_blocks.append({'object': 'block', 'type': 'paragraph', 
            'paragraph': {'rich_text': [{'type': 'text', 'text': {'content':
            f'Calories: {recipe.calorias}'}}]}})
    if recipe.tipo:
        try:
            recipe_type = RecipeType(recipe.tipo)
            metadata_blocks.append({'object': 'block', 'type': 'paragraph', 
                'paragraph': {'rich_text': [{'type': 'text', 'text': {
                'content': f'Tipo: {recipe_type.value}'}}]}})
        except ValueError:
            # If the recipe type is not in the enum, just display it as - is
            metadata_blocks.append({'object': 'block', 'type': 'paragraph', 
                'paragraph': {'rich_text': [{'type': 'text', 'text': {
                'content': f'Tipo: {recipe.tipo}'}}]}})
    if recipe.tags:
        metadata_blocks.append({'object': 'block', 'type': 'paragraph', 
            'paragraph': {'rich_text': [{'type': 'text', 'text': {'content':
            f"Etiquetas: {', '.join(recipe.tags)}"}}]}})
    metadata_blocks.append({'object': 'block', 'type': 'paragraph', 
        'paragraph': {'rich_text': [{'type': 'text', 'text': {'content':
        f"Estado: {'Hecho' if recipe.hecho else 'No hecho'}"}}]}})
    if recipe.date:
        metadata_blocks.append({'object': 'block', 'type': 'paragraph', 
            'paragraph': {'rich_text': [{'type': 'text', 'text': {'content':
            f'Fecha: {recipe.date}'}}]}})
    if recipe.metadata.dificultad:
        try:
            # Try to map the difficulty value to the enum
            difficulty_map = {
                "facil": Difficulty.FACIL, 
                "fácil": Difficulty.FACIL, 
                "media": Difficulty.MEDIA, 
                "dificil": Difficulty.DIFICIL, 
                "difícil": Difficulty.DIFICIL
            }
            difficulty = difficulty_map.get(recipe.metadata.dificultad.lower())
            if difficulty:
                metadata_blocks.append({'object': 'block', 'type': 'paragraph', 
                    'paragraph': {'rich_text': [{'type': 'text', 'text': {
                    'content': f'Dificultad: {difficulty.value}'}}]}})
            else:
                # Just display the difficulty as - is if not in map
                metadata_blocks.append({'object': 'block', 'type': 'paragraph', 
                    'paragraph': {'rich_text': [{'type': 'text', 'text': {
                    'content': f'Dificultad: {recipe.metadata.dificultad}'}}]}})
        except (ValueError, AttributeError):
            pass
    if recipe.metadata.tiempo_preparacion:
        metadata_blocks.append({'object': 'block', 'type': 'paragraph', 
            'paragraph': {'rich_text': [{'type': 'text', 'text': {'content':
            f'Tiempo de preparación: {recipe.metadata.tiempo_preparacion} minutos'}}]}})
    if recipe.metadata.tiempo_coccion:
        metadata_blocks.append({'object': 'block', 'type': 'paragraph', 
            'paragraph': {'rich_text': [{'type': 'text', 'text': {'content':
            f'Tiempo de cocción: {recipe.metadata.tiempo_coccion} minutos'}}]}})
    if recipe.metadata.tiempo_total:
        metadata_blocks.append({'object': 'block', 'type': 'paragraph', 
            'paragraph': {'rich_text': [{'type': 'text', 'text': {'content':
            f'Tiempo total: {recipe.metadata.tiempo_total} minutos'}}]}})
    if recipe.metadata.notas:
        metadata_blocks.append({'object': 'block', 'type': 'paragraph', 
            'paragraph': {'rich_text': [{'type': 'text', 'text': {'content':
            f'Notes: {truncate_text(recipe.metadata.notas)}'}}]}})
    blocks.extend(metadata_blocks)
    if recipe.ingredients:
        blocks.append({'object': 'block', 'type': 'heading_2', 'heading_2':
            {'rich_text': [{'type': 'text', 'text': {'content':
            'Ingredients'}}]}})
        for ingredient in recipe.ingredients:
            ingredient_text = []
            if ingredient.quantity > 0:
                ingredient_text.append(ingredient.formatted_quantity)
                if ingredient.unit:
                    ingredient_text.append(ingredient.formatted_unit)
            ingredient_text.append(ingredient.name)
            if ingredient.notes:
                ingredient_text.append(f'({ingredient.notes})')
            if ingredient.alternatives:
                ingredient_text.append(f"or {', '.join(ingredient.alternatives)}")
            blocks.append({'object': 'block', 'type': 'bulleted_list_item', 
                'bulleted_list_item': {'rich_text': [{'type': 'text', 
                'text': {'content': ' '.join(ingredient_text)}}]}})
    if recipe.instructions:
        blocks.append({'object': 'block', 'type': 'heading_2', 'heading_2':
            {'rich_text': [{'type': 'text', 'text': {'content':
            'Instructions'}}]}})
        for i, instruction in enumerate(recipe.instructions, 1):
            blocks.append({'object': 'block', 'type': 'numbered_list_item', 
                'numbered_list_item': {'rich_text': [{'type': 'text', 
                'text': {'content': truncate_text(instruction)}}]}})
    return blocks

# Alias for backwards compatibility
generate_notion_blocks = recipe_to_notion_blocks

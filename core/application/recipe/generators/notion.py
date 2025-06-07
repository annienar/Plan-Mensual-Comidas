"""
Notion generator for recipes.

This module handles the generation of Notion blocks for recipes.
"""
from core.domain.recipe.models.recipe import Recipe
from typing import List, Dict, Any

class NotionGenerator:
    """Generator for Notion recipe blocks."""

    def generate(self, recipe: Recipe) -> List[Dict[str, Any]]:
        """Generate Notion blocks for a recipe.

        Args:
            recipe: The recipe to generate blocks for

        Returns:
            List[Dict[str, Any]]: List of Notion blocks
        """
        blocks: List[Dict[str, Any]] = []
        blocks.append({'type': 'heading_1', 'content': {'text': [{'type':
            'text', 'text': {'content': recipe.title}}]}})

        if recipe.metadata:
            info_parts = []
            if recipe.metadata.porciones:
                info_parts.append(f'Porciones: {recipe.metadata.porciones}')
            if recipe.metadata.tiempo_preparacion and recipe.metadata.tiempo_coccion:
                total_time = recipe.metadata.tiempo_preparacion + recipe.metadata.tiempo_coccion
                info_parts.append(f'Tiempo total: {total_time} minutos')
            if info_parts:
                blocks.append({'type': 'paragraph', 'content': {'text': [{'type':
                    'text', 'text': {'content': ' | '.join(info_parts)}}]}})

        blocks.append({'type': 'heading_2', 'content': {'text': [{'type':
            'text', 'text': {'content': 'Ingredientes'}}]}})
        for ingredient in recipe.ingredients:
            if ingredient.cantidad and ingredient.unidad:
                content = f'{ingredient.nombre} - {ingredient.cantidad} {ingredient.unidad}'
            elif ingredient.cantidad:
                content = f'{ingredient.nombre} - {ingredient.cantidad}'
            else:
                content = ingredient.nombre
            blocks.append({'type': 'bulleted_list_item', 'content': {'text':
                [{'type': 'text', 'text': {'content': content}}]}})
        blocks.append({'type': 'heading_2', 'content': {'text': [{'type':
            'text', 'text': {'content': 'Instrucciones'}}]}})
        for i, instruction in enumerate(recipe.instructions, 1):
            blocks.append({'type': 'numbered_list_item', 'content': {'text':
                [{'type': 'text', 'text': {'content': instruction}}]}})
        return blocks

    def generate_batch(self, recipes: List[Recipe]) -> List[List[Dict[str, Any]]]:
        """Generate Notion blocks for multiple recipes.

        Args:
            recipes: List of recipes to generate blocks for

        Returns:
            List[List[Dict[str, Any]]]: List of Notion block lists
        """
        return [self.generate(recipe) for recipe in recipes]

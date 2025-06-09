"""
Markdown generator for recipes.

This module handles the generation of Markdown content for recipes.
"""
from core.domain.recipe.models.recipe import Recipe
from typing import List, Any

class MarkdownRecipeGenerator:
    """Generator for Markdown recipe content."""

    def generate(self, recipe: Recipe) -> str:
        """Generate Markdown content for a recipe.

        Args:
            recipe: The recipe to generate content for

        Returns:
            str: Markdown content
        """
        lines: List[str] = []
        lines.append(f'# {recipe.title}\n')
        if recipe.metadata:
            if recipe.metadata.porciones:
                lines.append(f'**Porciones:** {recipe.metadata.porciones}')
            if recipe.metadata.tiempo_preparacion and recipe.metadata.tiempo_coccion:
                total_time = recipe.metadata.tiempo_preparacion + recipe.metadata.tiempo_coccion
                lines.append(f'**Tiempo total:** {total_time} minutos\n')
        lines.append('## Ingredientes\n')
        for ingredient in recipe.ingredients:
            if ingredient.cantidad and ingredient.unidad:
                lines.append(f'- {ingredient.nombre} - {ingredient.cantidad} {ingredient.unidad}')
            elif ingredient.cantidad:
                lines.append(f'- {ingredient.nombre} - {ingredient.cantidad}')
            else:
                lines.append(f'- {ingredient.nombre}')
        lines.append('')
        lines.append('## Instrucciones\n')
        for i, instruction in enumerate(recipe.instructions, 1):
            lines.append(f'{i}. {instruction}')
        lines.append('')
        return '\n'.join(lines)

    def generate_batch(self, recipes: List[Recipe]) -> List[str]:
        """Generate Markdown content for multiple recipes.

        Args:
            recipes: List of recipes to generate content for

        Returns:
            List[str]: List of Markdown content strings
        """
        return [self.generate(recipe) for recipe in recipes]

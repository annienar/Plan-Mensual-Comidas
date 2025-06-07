"""
Generate markdown files for recipes.
"""
from core.domain.recipe.models.ingredient import Ingredient
from core.domain.recipe.models.metadata import RecipeMetadata
from core.domain.recipe.models.recipe import Recipe
from pathlib import Path
from typing import List, Dict, Any, Optional
import json

def format_ingredient(ingredient: Ingredient) ->str:
    """
    Format an ingredient for markdown display.

    Args:
        ingredient: Ingredient instance to format

    Returns:
        Formatted ingredient string
    """
    parts = []
    if ingredient.quantity > 0:
        parts.append(ingredient.formatted_quantity)
        if ingredient.unit:
            parts.append(ingredient.formatted_unit)
    parts.append(ingredient.name)
    if ingredient.notes:
        parts.append(f'({ingredient.notes})')
    if ingredient.alternatives:
        parts.append(f"or {', '.join(ingredient.alternatives)}")
    return ' '.join(parts)

def generate_markdown(recipe: Recipe, output_path: Path) ->bool:
    """
    Generate a markdown file for a recipe.

    Args:
        recipe: Recipe instance to convert to markdown
        output_path: Path to save the markdown file

    Returns:
        True if successful, False otherwise

    Raises:
        ValueError: If recipe is invalid
    """
    if not isinstance(recipe, Recipe):
        raise ValueError('recipe must be a Recipe instance')
    if not recipe.title:
        raise ValueError('recipe must have a title')
    if not recipe.ingredients:
        raise ValueError('recipe must have at least one ingredient')
    if not recipe.instructions:
        raise ValueError('recipe must have at least one instruction')
    try:
        output_path.parent.mkdir(parents = True, exist_ok = True)
        lines = []
        lines.append(f'# {recipe.title}\n')
        metadata_lines = []
        if hasattr(recipe.metadata, 'url') and recipe.metadata.url:
            metadata_lines.append(
                f'Source: [{recipe.metadata.url}]({recipe.metadata.url})')
        if recipe.metadata.porciones:
            metadata_lines.append(f'Porciones: {recipe.metadata.porciones}')
        if recipe.metadata.calorias:
            metadata_lines.append(f'Calorías: {recipe.metadata.calorias}')
        if recipe.metadata.tipo:
            metadata_lines.append(f'Tipo: {recipe.metadata.tipo}')
        if recipe.metadata.tags:
            metadata_lines.append(f"Etiquetas: {', '.join(recipe.metadata.tags)}")
        metadata_lines.append(
            f"Estado: {'Hecho' if recipe.metadata.hecho else 'No hecho'}")
        if recipe.metadata.date:
            metadata_lines.append(f'Fecha: {recipe.metadata.date}')
        if recipe.metadata.dificultad:
            metadata_lines.append(f'Dificultad: {recipe.metadata.dificultad}')
        if recipe.metadata.tiempo_preparacion:
            metadata_lines.append(
                f'Tiempo de preparación: {recipe.metadata.tiempo_preparacion} minutos')
        if recipe.metadata.tiempo_coccion:
            metadata_lines.append(
                f'Tiempo de cocción: {recipe.metadata.tiempo_coccion} minutos')
        if recipe.metadata.tiempo_total:
            metadata_lines.append(
                f'Tiempo total: {recipe.metadata.tiempo_total} minutos')
        if recipe.metadata.notas:
            metadata_lines.append(f'Notas: {recipe.metadata.notas}')
        if metadata_lines:
            lines.append('## Metadatos')
            lines.extend(metadata_lines)
            lines.append('')
        if recipe.ingredients:
            lines.append('## Ingredientes')
            for ingredient in recipe.ingredients:
                lines.append(f'- {format_ingredient(ingredient)}')
            lines.append('')
        if recipe.instructions:
            lines.append('## Instrucciones')
            for i, instruction in enumerate(recipe.instructions, 1):
                lines.append(f'{i}. {instruction}')
            lines.append('')
        try:
            output_path.write_text('\n'.join(lines), encoding='utf - 8')
            output_path.chmod(420)
            return True
        except (IOError, PermissionError) as e:
            print(f'Error writing to {output_path}: {str(e)}')
            return False
    except Exception as e:
        print(f'Error generating markdown for {recipe.title}: {str(e)}')
        return False

def generate_all_markdown(json_dir: Path, output_dir: Path) ->bool:
    """
    Generate markdown files for all recipes in a directory.

    Args:
        json_dir: Directory containing recipe JSON files
        output_dir: Directory to save markdown files

    Returns:
        True if all recipes were processed successfully, False otherwise
    """
    if not json_dir.exists():
        print(f'Directory not found: {json_dir}')
        return False
    output_dir.mkdir(parents = True, exist_ok = True)
    success = True
    for json_file in json_dir.glob('*.json'):
        try:
            with open(json_file, 'r', encoding='utf - 8') as f:
                data = json.load(f)
            recipe = Recipe.from_dict(data)
            output_path = output_dir / f'{json_file.stem}.md'
            if not generate_markdown(recipe, output_path):
                success = False
                print(f'Failed to generate markdown for {json_file.name}')
        except json.JSONDecodeError as e:
            success = False
            print(f'Invalid JSON in {json_file.name}: {str(e)}')
        except Exception as e:
            success = False
            print(f'Error processing {json_file.name}: {str(e)}')
    return success

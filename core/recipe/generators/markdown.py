"""
Markdown generator for recipes.

Generates markdown files from processed recipes.
"""

import json
from fractions import Fraction
from pathlib import Path
from typing import Dict, Union

from core.recipe.models.recipe import Recipe
from core.utils.logger import get_logger, log_info

logger = get_logger("recipe.generators.markdown")


def format_ingredient(ingredient: Dict[str, Union[float, str]]) -> str:
    """
    Format an ingredient for markdown display.

    Args:
        ingredient: Dictionary with ingredient data

    Returns:
        str: Formatted ingredient line
    """
    quantity = float(ingredient.get("cantidad", 0))
    unit = str(ingredient.get("unidad", ""))
    name = str(ingredient.get("nombre", "")).lower().split(",")[0].strip()

    # No quantity (e.g. 'salt to taste')
    if not quantity:
        return f"- {name}"

    # Convert decimal to mixed fraction or integer
    if quantity.is_integer():
        qty = str(int(quantity))
    else:
        frac = Fraction(quantity).limit_denominator()
        if frac.denominator == 1:
            qty = str(frac.numerator)
        elif frac.numerator > frac.denominator:
            whole = frac.numerator // frac.denominator
            rem = frac.numerator - whole * frac.denominator
            qty = f"{whole} {rem}/{frac.denominator}"
        else:
            qty = f"{frac.numerator}/{frac.denominator}"

    # Singularize unit if qty == 1
    if unit in {"tazas", "cucharadas", "cucharaditas"} and qty == "1":
        unit = unit[:-1]  # Remove 's'

    # Format line
    if unit and unit != "u":
        return f"- {qty} {unit} de {name}"
    else:
        return f"- {qty} {name}"


def generate_markdown(recipe: Recipe, output_path: Path) -> bool:
    """
    Generate a markdown file for a recipe.

    Args:
        recipe: Recipe object to generate markdown for
        output_path: Path where to save the markdown file

    Returns:
        bool: True if generation was successful
    """
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            # Title and optional author
            f.write(f"# {recipe.name}\n\n")
            if recipe.author:
                f.write(f"*Receta de {recipe.author}*\n\n")

            # Metadata
            f.write(f"- **Porciones:** {recipe.servings or 'Desconocido'}\n")
            f.write(f"- **Calorías totales:** {recipe.calories or 'Desconocido'}\n")
            f.write(f"- **Origen:** {recipe.source_url or 'Desconocido'}\n\n")

            # Ingredients
            f.write("## Ingredientes\n")
            for ingredient in recipe.ingredients:
                f.write(format_ingredient(ingredient) + "\n")
            f.write("\n")

            # Preparation
            f.write("## Preparación\n")
            for idx, step in enumerate(recipe.preparation_steps, 1):
                f.write(f"{idx}. {step}\n")

        log_info(f"✅ Markdown generado: {output_path}")
        return True

    except Exception as e:
        logger.error(f"Error al generar Markdown: {e}")
        return False


def generate_all_markdown(json_dir: Path, md_dir: Path) -> bool:
    """
    Generate markdown files for all processed recipes.

    Args:
        json_dir: Directory containing JSON recipe files
        md_dir: Directory where to save markdown files

    Returns:
        bool: True if all files were generated successfully
    """
    if not json_dir.is_dir():
        logger.warning(f"⚠️ No se encontró carpeta JSON: {json_dir}")
        return True

    md_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"📁 Creada carpeta: {md_dir}")

    success = True
    for json_file in json_dir.glob("*.json"):
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                recipe_data = json.load(f)
                recipe = Recipe.from_dict(recipe_data)

            md_file = md_dir / f"{json_file.stem}.md"
            if not generate_markdown(recipe, md_file):
                success = False

        except Exception as e:
            logger.error(f"❌ Error procesando {json_file}: {e}")
            success = False

    return success 
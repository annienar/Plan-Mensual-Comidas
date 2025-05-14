"""
Command-line interface for the Recipe Management System.

Provides a CLI for processing recipes and generating documents using Click.
"""

import os
from dotenv import load_dotenv
load_dotenv()
import click
import shutil
from pathlib import Path
from core.recipe.processor import RecipeProcessor
from core.notion.client import NotionClient
from core.notion.sync import NotionSync
from core.notion.models import NotionRecipe, NotionIngredient, NotionPantryItem
from core.utils.logger import get_logger
import asyncio

SIN_PROCESAR = Path("recetas/sin_procesar")
PROCESADAS = Path("recetas/procesadas")
# ERRORES = Path("recetas/errores")  # Optional: create if you want to move failed files

logger = get_logger("cli")

@click.group()
def cli():
    """Recipe Management CLI (Click-based)."""
    pass

@cli.command()
def process_recipes():
    """Process all recipes in 'recetas/sin_procesar' and sync to Notion."""
    files = list(SIN_PROCESAR.glob("*"))
    if not files:
        click.echo("No files to process in 'recetas/sin_procesar'.")
        return

    # Setup Notion sync
    notion_token = os.getenv("NOTION_TOKEN")
    db_ids = {
        "Recetas": os.getenv("NOTION_RECETAS_DB"),
        "Ingredientes": os.getenv("NOTION_INGREDIENTES_DB"),
        "Alacena": os.getenv("NOTION_ALACENA_DB"),
    }
    
    # Debug: Print database IDs
    click.echo("Using database IDs:")
    for db_name, db_id in db_ids.items():
        click.echo(f"  {db_name}: {db_id}")
    
    notion_client = NotionClient(token=notion_token)
    notion_sync = NotionSync(notion_client, db_ids)
    processor = RecipeProcessor()

    for file in files:
        try:
            click.echo(f"Processing: {file.name}")
            # 1. Extract and process recipe (async)
            content = file.read_text(encoding="utf-8")
            recipe_obj = asyncio.run(processor.process_recipe(content))
            # 2. Sync pantry items and ingredients
            pantry_ids = {}
            ingredient_ids = []
            for ing in recipe_obj.ingredients:
                pantry_item = NotionPantryItem(name=ing.name)  # Add more fields as needed
                pantry_id = notion_sync.sync_pantry_item(pantry_item)
                pantry_ids[ing.name] = pantry_id
                ingredient = NotionIngredient(name=ing.name, pantry_id=pantry_id)
                ingredient_id = notion_sync.sync_ingredient(ingredient)
                ingredient_ids.append(ingredient_id)
            # 3. Sync recipe, link to ingredients
            notion_recipe = NotionRecipe(title=recipe_obj.title, ingredient_ids=ingredient_ids)
            notion_sync.sync_recipe(notion_recipe)
            # 4. Ensure processed directory exists and move file
            PROCESADAS.mkdir(parents=True, exist_ok=True)
            shutil.move(str(file), PROCESADAS / file.name)
            click.secho(f"SUCCESS: {file.name} processed and moved.", fg="green")
        except Exception as e:
            logger.error(f"Failed to process {file.name}: {e}")
            click.secho(f"ERROR: Failed to process {file.name}: {e}", fg="red")
            # Optionally move to ERRORES / file.name

if __name__ == "__main__":
    cli() 
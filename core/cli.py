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
import time

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
            recipe_start_time = time.time()
            # 1. Extract and process recipe (async)
            extract_start = time.time()
            content = file.read_text(encoding="utf-8")
            recipe_obj = asyncio.run(processor.process_recipe(content))
            extract_time = time.time() - extract_start
            click.echo(f"  Extraction & parsing took {extract_time:.2f} seconds")

            # 2. Sync pantry items and ingredients
            sync_ingredients_start = time.time()
            pantry_ids = {}
            ingredient_row_ids = []  # IDs of Ingredientes DB rows
            for ing in recipe_obj.ingredients:
                logger.info(f"Processing ingredient: {ing.name}")
                logger.info(f"  Raw quantity: {ing.quantity}")
                logger.info(f"  Raw unit: {ing.unit}")
                
                pantry_item = NotionPantryItem(name=ing.name)  # Add more fields as needed
                pantry_id = notion_sync.sync_pantry_item(pantry_item)
                pantry_ids[ing.name] = pantry_id
                
                ingredient = NotionIngredient(
                    name=ing.name,
                    pantry_id=pantry_id,
                    quantity=ing.quantity,
                    unit=ing.unit
                )
                logger.info(f"Created NotionIngredient object:")
                logger.info(f"  Name: {ingredient.name}")
                logger.info(f"  Quantity: {ingredient.quantity}")
                logger.info(f"  Unit: {ingredient.unit}")
                logger.info(f"  Pantry ID: {ingredient.pantry_id}")
                
                ing_sync_start = time.time()
                ingredient_row_id = notion_sync.sync_ingredient(ingredient)
                ing_sync_time = time.time() - ing_sync_start
                click.echo(f"    Synced ingredient '{ing.name}' in {ing_sync_time:.2f} seconds")
                ingredient_row_ids.append(ingredient_row_id)
                time.sleep(1)  # Wait for Notion to index the ingredient page

            sync_ingredients_time = time.time() - sync_ingredients_start
            click.echo(f"  Ingredient sync took {sync_ingredients_time:.2f} seconds")

            # 3. Sync recipe, link to ingredient rows (not pantry items)
            time.sleep(2)  # Wait for Notion to index all ingredient rows
            meta = recipe_obj.metadata
            notion_recipe = NotionRecipe(
                title=meta.title,
                ingredient_ids=ingredient_row_ids,  # Use ingredient row IDs
                portions=meta.porciones,
                calories=meta.calorias,
                tags=meta.tags,
                tipo=meta.tipo,
                hecho=meta.hecho,
                date=meta.date,
                dificultad=meta.dificultad,
                tiempo_preparacion=meta.tiempo_preparacion,
                tiempo_coccion=meta.tiempo_coccion,
                tiempo_total=meta.tiempo_total,
                notas=meta.notas,
                url=meta.url,
                ingredients=recipe_obj.ingredients,  # Pass the full ingredient objects
                instructions=recipe_obj.instructions,  # Pass the preparation steps
            )
            recipe_sync_start = time.time()
            recipe_page_id = notion_sync.sync_recipe(notion_recipe)
            recipe_sync_time = time.time() - recipe_sync_start
            click.echo(f"  Recipe sync took {recipe_sync_time:.2f} seconds")
            time.sleep(2)  # Wait for Notion to index the recipe page

            # 4. Update each ingredient row with the recipe relation
            update_ingredient_start = time.time()
            for ingredient_row_id in ingredient_row_ids:
                rel_sync_start = time.time()
                notion_sync.update_ingredient_with_recipe(ingredient_row_id, recipe_page_id)
                rel_sync_time = time.time() - rel_sync_start
                click.echo(f"    Updated ingredient relation in {rel_sync_time:.2f} seconds")
                time.sleep(1)  # Wait for Notion to index each update
            update_ingredient_time = time.time() - update_ingredient_start
            click.echo(f"  Ingredient relation updates took {update_ingredient_time:.2f} seconds")

            # 5. Ensure processed directory exists and move file
            PROCESADAS.mkdir(parents=True, exist_ok=True)
            shutil.move(str(file), PROCESADAS / file.name)
            total_recipe_time = time.time() - recipe_start_time
            click.secho(f"SUCCESS: {file.name} processed and moved in {total_recipe_time:.2f} seconds.", fg="green")
        except Exception as e:
            logger.error(f"Failed to process {file.name}: {e}")
            click.secho(f"ERROR: Failed to process {file.name}: {e}", fg="red")
            # Optionally move to ERRORES / file.name

if __name__ == "__main__":
    cli() 
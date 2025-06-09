"""
Command - line interface for the Recipe Management System.

Provides a CLI for processing recipes and generating documents using Click.
"""

import os
from dotenv import load_dotenv
load_dotenv()
import click
import shutil
from pathlib import Path
from core.application.recipe.processor import RecipeProcessor
from core.infrastructure.notion.client import NotionClient
from core.infrastructure.notion.sync import NotionSync
from core.infrastructure.notion.models import NotionRecipe, NotionIngredient, NotionPantryItem
from core.utils.logger import get_logger
import asyncio
import time
from typing import List, Dict, Any
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

SIN_PROCESAR = Path("data / recipes / sin_procesar")
PROCESADAS = Path("data / recipes / procesadas")
ERRORES = Path("data / recipes / errores")

logger = get_logger("cli")

def validate_env_vars() -> Dict[str, str]:
    """Validate required environment variables."""
    required_vars = {
        "NOTION_TOKEN": os.getenv("NOTION_TOKEN"), 
        "NOTION_RECETAS_DB": os.getenv("NOTION_RECETAS_DB"), 
        "NOTION_INGREDIENTES_DB": os.getenv("NOTION_INGREDIENTES_DB"), 
        "NOTION_ALACENA_DB": os.getenv("NOTION_ALACENA_DB"), 
    }
    missing = [var for var, value in required_vars.items() if not value]
    if missing:
        raise click.ClickException(f"Missing required environment variables: {', '.join(missing)}")
    return {
        "Recetas": required_vars["NOTION_RECETAS_DB"], 
        "Ingredientes": required_vars["NOTION_INGREDIENTES_DB"], 
        "Alacena": required_vars["NOTION_ALACENA_DB"], 
    }

@click.group()

def cli():
    """Recipe Management CLI (Click - based)."""
    pass

@retry(stop = stop_after_attempt(3), wait = wait_exponential(multiplier = 1, min = 2, max = 10))
async def process_single_recipe(file: Path, notion_sync: NotionSync, processor: RecipeProcessor, progress_bar) -> bool:
    """Process a single recipe file with retry logic."""
    try:
        progress_bar.update(1, f"Processing: {file.name}")
        recipe_start_time = time.time()
        timing_info = {}

        # 1. Extract and process recipe
        extract_start = time.time()
        content = file.read_text(encoding="utf-8")
        recipe_obj = await processor.process_recipe(content)
        timing_info['extraction'] = time.time() - extract_start

        # 2. Sync pantry items and ingredients
        pantry_start = time.time()
        pantry_ids = {}
        ingredient_row_ids = []
        for ing in recipe_obj.ingredients:
            pantry_item = NotionPantryItem(name = ing.nombre)
            pantry_id = await notion_sync.sync_pantry_item(pantry_item)
            pantry_ids[ing.nombre] = pantry_id

            ingredient = NotionIngredient(
                name = ing.nombre, 
                pantry_id = pantry_id, 
                quantity = ing.cantidad, 
                unit = ing.unidad
)
            ingredient_row_id = await notion_sync.sync_ingredient(ingredient)
            ingredient_row_ids.append(ingredient_row_id)
            await asyncio.sleep(0.1)  # Rate limiting
        timing_info['pantry_sync'] = time.time() - pantry_start

        # 3. Sync recipe
        recipe_sync_start = time.time()
        notion_recipe = NotionRecipe(
            title = recipe_obj.metadata.title, 
            ingredient_ids = ingredient_row_ids, 
            portions = recipe_obj.metadata.porciones, 
            calories = recipe_obj.metadata.calorias, 
            tags = recipe_obj.metadata.tags, 
            tipo = recipe_obj.metadata.tipo, 
            hecho = recipe_obj.metadata.hecho, 
            date = recipe_obj.metadata.date, 
            dificultad = recipe_obj.metadata.dificultad, 
            tiempo_preparacion = recipe_obj.metadata.tiempo_preparacion, 
            tiempo_coccion = recipe_obj.metadata.tiempo_coccion, 
            tiempo_total = recipe_obj.metadata.tiempo_total, 
            notas = recipe_obj.metadata.notas, 
            url = recipe_obj.metadata.url, 
            ingredients = recipe_obj.ingredients, 
            instructions = recipe_obj.instructions, 
)
        recipe_page_id = await notion_sync.sync_recipe(notion_recipe)
        timing_info['recipe_sync'] = time.time() - recipe_sync_start

        # 4. Update ingredient relations
        relations_start = time.time()
        for ingredient_row_id in ingredient_row_ids:
            await notion_sync.update_ingredient_with_recipe(ingredient_row_id, recipe_page_id)
            await asyncio.sleep(0.1)  # Rate limiting
        timing_info['relations_update'] = time.time() - relations_start

        # 5. Move processed file
        move_start = time.time()
        PROCESADAS.mkdir(parents = True, exist_ok = True)
        shutil.move(str(file), PROCESADAS / file.name)
        timing_info['file_move'] = time.time() - move_start

        total_time = time.time() - recipe_start_time
        timing_summary = ", ".join([f"{k}: {v:.2f}s" for k, v in timing_info.items()])
        progress_bar.update(1, f"SUCCESS: {file.name} processed in {total_time:.2f}s ({timing_summary})")
        return True

    except Exception as e:
        logger.error(f"Failed to process {file.name}: {e}")
        ERRORES.mkdir(parents = True, exist_ok = True)
        shutil.move(str(file), ERRORES / file.name)
        progress_bar.update(1, f"ERROR: {file.name} failed: {str(e)}")
        return False

@cli.command()
@click.option('--concurrency', default = 3, help='Number of concurrent recipe processing tasks')

def process_recipes(concurrency: int):
    """Process all recipes in the sin_procesar directory."""
    files = list(SIN_PROCESAR.glob("*"))
    if not files:
        click.echo("No files to process in 'data / recipes / sin_procesar'.")
        return

    try:
        db_ids = validate_env_vars()
    except click.ClickException as e:
        click.echo(str(e), err = True)
        return

    async def process_all_recipes():
        async with NotionClient() as notion_client:
            notion_sync = NotionSync(notion_client, db_ids)
            processor = RecipeProcessor()
            semaphore = asyncio.Semaphore(concurrency)

            with click.progressbar(length = len(files), label="Processing recipes") as progress_bar:
                async def process_with_semaphore(file):
                    async with semaphore:
                        return await process_single_recipe(file, notion_sync, processor, progress_bar)

                tasks = [process_with_semaphore(file) for file in files]
                results = await asyncio.gather(*tasks)

                success_count = sum(1 for r in results if r)
                click.echo(f"\nProcessed {len(files)} recipes: {success_count} successful, {len(files) - success_count} failed")

    asyncio.run(process_all_recipes())

@cli.command()

def list_recipes():
    """List all recipes in the system."""
    click.echo("Unprocessed recipes:")
    for file in SIN_PROCESAR.glob("*"):
        click.echo(f"  {file.name}")

    click.echo("\nProcessed recipes:")
    for file in PROCESADAS.glob("*"):
        click.echo(f"  {file.name}")

    click.echo("\nFailed recipes:")
    for file in ERRORES.glob("*"):
        click.echo(f"  {file.name}")

if __name__ == "__main__":
    cli()

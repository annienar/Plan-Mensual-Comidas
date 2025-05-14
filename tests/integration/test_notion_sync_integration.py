import os
import pytest
from core.notion.client import NotionClient
from core.notion.sync import NotionSync
from core.recipe.models.recipe import Recipe

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_TEST_DB = os.getenv("NOTION_TEST_DB")

pytestmark = pytest.mark.integration

@pytest.mark.skipif(
    not NOTION_TOKEN or not NOTION_TEST_DB,
    reason="Notion integration env vars not set"
)
def test_notion_sync_create_retrieve_delete():
    client = NotionClient(token=NOTION_TOKEN)
    sync = NotionSync(client, NOTION_TEST_DB)

    # Create a test recipe
    recipe = Recipe(
        name="Integration Test Recipe",
        source_url="https://example.com",
        servings=2,
        ingredients=["1 cup flour", "2 eggs"],
        preparation_steps=["Mix ingredients", "Bake"],
        calories=123
    )

    # Create
    page_id = sync.sync_recipe(recipe)
    assert page_id

    # Retrieve
    page = sync.get_recipe(page_id)
    assert page["id"] == page_id
    assert page["properties"]["Nombre"]["title"][0]["text"]["content"] == "Integration Test Recipe"

    # Delete (archive)
    sync.delete_recipe(page_id)
    page_after = sync.get_recipe(page_id)
    assert page_after["archived"] is True 
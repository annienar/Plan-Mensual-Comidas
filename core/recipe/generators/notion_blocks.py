"""
Generate Notion blocks for recipe pages.
"""

from typing import List, Dict, Any

def recipe_to_notion_blocks(recipe) -> List[Dict[str, Any]]:
    """
    Convert a Recipe object into a list of Notion blocks for page formatting.
    
    Args:
        recipe: Recipe object containing all recipe data
        
    Returns:
        List of Notion block objects
    """
    blocks = []
    
    # Title as heading
    blocks.append({
        "object": "block",
        "type": "heading_1",
        "heading_1": {
            "rich_text": [{"type": "text", "text": {"content": recipe.title}}]
        }
    })
    
    # Metadata section
    meta_text = []
    if getattr(recipe, 'porciones', None):
        meta_text.append(f"🍽 Porciones: {recipe.porciones}")
    if getattr(recipe, 'tiempo_preparacion', None):
        meta_text.append(f"⏱ Prep: {recipe.tiempo_preparacion}")
    if getattr(recipe, 'tiempo_coccion', None):
        meta_text.append(f"🔥 Cocción: {recipe.tiempo_coccion}")
    if getattr(recipe, 'tiempo_total', None):
        meta_text.append(f"⏰ Total: {recipe.tiempo_total}")
    if getattr(recipe, 'dificultad', None):
        meta_text.append(f"📊 Dificultad: {recipe.dificultad}")
    if getattr(recipe, 'calorias', None):
        meta_text.append(f"⚡ Calorías: {recipe.calorias}")
    
    if meta_text:
        blocks.append({
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": " | ".join(meta_text)}}]
            }
        })
    
    # Ingredients section
    blocks.append({
        "object": "block",
        "type": "heading_2",
        "heading_2": {
            "rich_text": [{"type": "text", "text": {"content": "🧾 Ingredientes"}}]
        }
    })
    
    # Ingredients as bulleted list
    for ing in getattr(recipe, 'ingredients', []):
        ing_text = f"{ing.quantity} {ing.unit} {ing.name}".strip()
        if getattr(ing, 'optional', False):
            ing_text = f"Opcional: {ing_text}"
        blocks.append({
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": ing_text}}]
            }
        })
    
    # Instructions section
    blocks.append({
        "object": "block",
        "type": "heading_2",
        "heading_2": {
            "rich_text": [{"type": "text", "text": {"content": "🔪 Preparación"}}]
        }
    })
    
    # Instructions as numbered list
    for i, step in enumerate(getattr(recipe, 'instructions', []), 1):
        blocks.append({
            "object": "block",
            "type": "numbered_list_item",
            "numbered_list_item": {
                "rich_text": [{"type": "text", "text": {"content": step}}]
            }
        })
    
    # Notes section (if any)
    if getattr(recipe, 'notas', None):
        blocks.append({
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "📝 Notas"}}]
            }
        })
        
        for note in recipe.notas.split('\n'):
            if note.strip():
                blocks.append({
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": note.strip()}}]
                    }
                })
    
    return blocks 
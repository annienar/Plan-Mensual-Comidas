from core.recipe.extractors.sections import SectionExtractor
from core.recipe.extractors.ingredients import IngredientExtractor
from core.recipe.extractors.metadata import MetadataExtractor
from core.recipe.normalizers.ingredients import IngredientNormalizer
from core.recipe.models.recipe import Recipe
from core.recipe.models.metadata import RecipeMetadata

class RecipeProcessor:
    def __init__(self):
        self.section_extractor = SectionExtractor()
        self.ingredient_extractor = IngredientExtractor()
        self.ingredient_normalizer = IngredientNormalizer()
        self.metadata_extractor = MetadataExtractor()

    async def process_recipe(self, content: str) -> Recipe:
        """Process recipe content into structured data."""
        # 1. Extract sections
        sections = self.section_extractor.extract(content)
        # 2. Extract and normalize ingredients
        raw_ingredients = self.ingredient_extractor.extract("\n".join(sections["ingredients"]))
        normalized_ingredients = self.ingredient_normalizer.normalize(raw_ingredients)
        # 3. Extract and normalize metadata
        metadata_dict = self.metadata_extractor.extract(content)
        metadata = RecipeMetadata(
            title=metadata_dict.get("title", "Desconocido"),
            url=metadata_dict.get("url"),
            porciones=metadata_dict.get("porciones"),
            calorias=metadata_dict.get("calorias"),
            tipo=metadata_dict.get("tipo"),
            tags=metadata_dict.get("tags", []),
            hecho=metadata_dict.get("hecho", False),
            date=metadata_dict.get("date"),
            dificultad=metadata_dict.get("dificultad"),
            tiempo_preparacion=metadata_dict.get("tiempo_preparacion"),
            tiempo_coccion=metadata_dict.get("tiempo_coccion"),
            tiempo_total=metadata_dict.get("tiempo_total"),
            notas=metadata_dict.get("notas"),
        )
        # 4. Create recipe object
        recipe = Recipe(
            metadata=metadata,
            ingredients=normalized_ingredients,
            instructions=sections["instructions"],
        )
        return recipe

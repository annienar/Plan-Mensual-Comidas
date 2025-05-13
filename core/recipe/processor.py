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
            servings=metadata_dict.get("servings", 0) or 0,
            calories_per_serving=metadata_dict.get("calories", None),
            # Add more fields as needed
        )
        # 4. Create recipe object
        recipe = Recipe(
            title=metadata_dict.get("title", "Desconocido"),
            ingredients=normalized_ingredients,
            instructions=sections["instructions"],
            metadata=metadata,
            source=metadata_dict.get("url", None),
        )
        return recipe

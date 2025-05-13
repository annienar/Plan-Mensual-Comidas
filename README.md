# Monthly Meal Plan

## Project Structure (as of latest migration)

```
core/
  extraction/         # PDF, OCR, and TXT extractors (class-based)
  recipe/             # Recipe models, extractors, normalizers, processor
  notion/             # Notion integration (to be refactored)
  utils/              # Config, logger, and utilities
recetas/              # Real recipes to be loaded and processed (not test data)
tests/
  unit/               # Unit tests for all core modules
    test_recipe/      # Recipe extractors, normalizers, processor
    test_extraction/  # Text, PDF, OCR extractors
  fixtures/           # Test data (e.g., sample recipes)
    recipes/
      sin_procesar/   # Realistic test recipes for extraction/processing
  integration/        # (Currently empty, for future integration tests)

migration.md          # Migration progress and next steps
requirements.txt      # Project dependencies
documentation.md      # Technical documentation

```

## Key Points
- **recetas/** is for real, user-supplied recipes (not test data).
- **tests/fixtures/recipes/sin_procesar/** contains only test data for automated tests.
- All core modules are now modular and class-based.
- Integration tests will be added as the Notion migration progresses.

## Next Migration Phase
- Refactor Notion integration into `core/notion/`:
  - Split `notion_sync.py` into `client.py`, `sync.py`, and `models.py`.
  - Add error handling and retry mechanisms.
  - See `migration.md` for details.

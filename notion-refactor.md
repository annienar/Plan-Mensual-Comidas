# Notion Refactor Plan

[See full technical documentation here.](documentation.md)

## Current Workflow (as of May 2024)

### What Happens When a File is Processed

1. **File Discovery**
   - CLI scans `recetas/sin_procesar` for files.

2. **Recipe Extraction**
   - Reads file as UTF-8 text.
   - Processes with `RecipeProcessor.process_recipe()`.

3. **Notion Setup**
   - Loads Notion token and DB IDs from `.env`.
   - Instantiates `NotionClient` and `NotionSync`.

4. **Sync Pantry Items (Alacena)**
   - For each ingredient:
     - Creates a new page in Alacena DB with:
       - `Nombre` (title): ingredient name
       - `Categoría`, `Stock alacena`, `Unidad` (if present)

5. **Sync Ingredients (Ingredientes)**
   - For each ingredient:
     - Creates a new page in Ingredientes DB with:
       - `Ingrediente` (relation): links to pantry item
       - `Cantidad Usada` (title): quantity (as string)
       - `Unidad` (rich_text): unit (as string)

6. **Sync Recipe (Recetas)**
   - Creates/updates a page in Recetas DB with:
     - `Nombre` (title): recipe title
     - `Porciones`, `Calorías`, `Tags` (if present)
     - `Ingredientes` (relation): links to ingredient pages

7. **File Movement**
   - Moves processed file to `recetas/procesadas`.

8. **Feedback**
   - Prints success/error messages to console.

### What Appears in Notion

- **Recetas**: New/updated page with title, portions, calories, tags, and ingredient relations.
- **Ingredientes**: New page for each ingredient with relation to pantry, quantity (title), and unit.
- **Alacena**: New page for each ingredient with name, category, stock, and unit.

### What is NOT Happening
- No deduplication (creates new entries every time).
- No updating of existing ingredient/pantry pages.
- No advanced Notion features (rollups, bi-directional, etc.).
- No rollback on partial sync failure.
- No content blocks/instructions in Notion pages—only properties.

## Actual Results in Notion (Observed)

### Ingredientes (Ingredients) DB
- Each ingredient from the recipe is added as a new row.
- "Ingrediente" column links to the corresponding pantry item in Alacena.
- "Cantidad Usada" (title) is present, but values are empty.
- "Unidad" column is present, but values are empty.
- "Receta" relation is empty (not set by the code).

### Alacena (Pantry) DB
- Each ingredient is added as a new row.
- Many duplicate entries for the same ingredient (e.g., "pasta").
- All other columns ("Categoría", "Stock alacena", "En lista de compras", "Unidad") are empty.

### Recetas Completas (Recipes) DB
- Each recipe is added as a new row with the correct title.
- All other properties ("Tipo", "Porciones", "Calorías", "Tags", "Ingredientes", "Date") are empty.
- "Ingredientes" relation is empty (not set by the code).

### Key Issues Observed
- **Duplication:** Ingredients and pantry items are duplicated for every recipe processed.
- **Missing Data:** Only the title property is being set for recipes and ingredients; all other properties are left empty.
- **Missing Relations:** Relations (e.g., linking ingredients to recipes, or recipes to ingredients) are not being set.
- **No Property Mapping:** The code is not mapping or extracting values for properties like "Porciones", "Calorías", "Tags", "Unidad", etc., even if they exist in the recipe object.

## Goals
- Improve modularity, maintainability, and testability of Notion integration.
- Ensure robust error handling and clear user feedback.
- Support advanced Notion features (relations, rollups, etc.) as needed.
- Make the sync layer extensible for future features (e.g., shopping list, advanced pantry management).

## Tasks

### 1. Code Structure & Modularity
- [ ] Review and refactor `core/notion/client.py` for clarity and separation of concerns.
- [ ] Split sync logic into smaller, testable units (e.g., separate syncers for Recetas, Ingredientes, Alacena).
- [ ] Ensure all Notion property mappings are centralized and easy to update.

### 2. Error Handling & Logging
- [ ] Standardize error handling for all Notion operations (custom exceptions, retries, user-friendly messages).
- [ ] Improve logging for all Notion sync actions (success, failure, skipped, etc.).

### 3. Advanced Notion Features
- [ ] Add support for rollups and advanced relations if needed.
- [ ] Ensure all relations (Recetas <-> Ingredientes <-> Alacena) are robust and bi-directional where appropriate.

### 4. Testing & Validation
- [ ] Expand unit and integration tests for Notion sync (mock Notion API where possible).
- [ ] Add tests for edge cases (missing properties, permission errors, etc.).

### 5. CLI & User Experience
- [ ] Add CLI commands for Notion diagnostics (e.g., test connection, list databases, validate schema).
- [ ] Improve CLI feedback for Notion sync (summary, error details, etc.).

### 6. Documentation
- [ ] Document Notion integration architecture and property mapping.
- [ ] Add troubleshooting guide for common Notion sync issues.

## Priorities
- [ ] Start with code structure and error handling.
- [ ] Then address advanced features and testing.
- [ ] Finally, polish CLI and documentation.

## Comparison: Expected vs. Actual Notion Sync

### What is Expected (from documentation.md and project goals)
- All relevant data (title, ingredients, instructions, metadata) is extracted and mapped to Notion.
- All properties are set for each Notion DB (Recetas, Ingredientes, Alacena).
- Relations are established between recipes, ingredients, and pantry items.
- Deduplication: No duplicate entries for ingredients or pantry items.
- Content blocks (instructions, notes) are added to Notion pages.
- Existing entries are updated, not always created anew.
- Robust error handling and user feedback.
- Advanced Notion features (rollups, bi-directional relations) are supported as needed.

### What is Actually Happening (from code and screenshots)
- Only the title property is set for recipes and ingredients; all other properties are left empty.
- No property mapping for porciones, calorías, tags, tipo, unidad, etc.
- No content blocks are added to Notion pages.
- Duplication: Every ingredient and pantry item is created anew for each recipe.
- No updating of existing entries; always creates new pages.
- No relations between recipes, ingredients, and pantry items.
- No advanced Notion features are used.
- Only basic error print for failures.

### Gaps and Actions Needed
| Area                | Expected (docs)         | Actual (code/screenshots)         | Gap/Action Needed                |
|---------------------|------------------------|-----------------------------------|----------------------------------|
| Property Mapping    | All properties mapped  | Only title mapped                 | Map all properties               |
| Relations           | All relations set      | None set                          | Implement relations              |
| Deduplication       | No duplicates          | Duplicates for each sync          | Add deduplication logic          |
| Content Blocks      | Instructions, notes    | Not present                       | Add content block support        |
| Error Handling      | Robust, user-friendly  | Basic print                       | Improve error handling           |
| Advanced Features   | Rollups, bi-directional| Not used                          | Implement as needed              |
| Update Logic        | Update existing entries| Always creates new                | Add update logic                 |

## Missing: Recipe Page Content in Notion

### What is Missing
- The Notion recipe page (e.g., "Pasta con Albóndigas") only has the title and empty properties.
- The main page content (instructions, ingredients table, notes, etc.) is completely empty.
- No preparation steps, ingredient tables, or metadata blocks are present.

### What is Expected
- The recipe page should include:
  - A formatted title (with emoji, if present)
  - General information (portions, time, method, type, origin link)
  - An ingredients table (ingredient, quantity, unit)
  - Preparation steps as a numbered list
  - Variations and notes as bullet points or sections
  - Calorie breakdown as a table
  - System notes or metadata

### What the Code Does
- Only sets Notion database properties (title, etc.).
- **Does NOT create any content blocks** (paragraphs, tables, lists, etc.) in the Notion page body.
- As a result, the recipe page is empty except for the title and properties.

### Gap
- **No recipe content is being added to the Notion page body.**
- Users do not see the actual recipe, instructions, or ingredient details in Notion—just an empty page with a title.

### Action Needed
- Implement logic to convert the extracted recipe (ingredients, steps, notes, etc.) into Notion content blocks.
- Use the Notion API's `children` parameter when creating/updating a page to add these blocks.
- Map markdown sections (like in your pancakes example) to Notion block types (heading, table, bulleted/numbered list, etc.).

---

## Action Plan: Achieving Notion Refactor Goals (Checklist)

### 1. Property Mapping & Extraction
- [ ] **Audit and Document Model Fields**
  - [ ] List all fields currently extracted and stored in your `Recipe` and `Ingredient` models.
  - [ ] Compare with the properties required by your Notion DBs (see below):

#### Recetas Completas (Recipes)
| Notion Property      | In Recipe Model?         | In Metadata?         | Notes/Action Needed                |
|----------------------|-------------------------|----------------------|------------------------------------|
| Nombre (title)       | `title`                 |                      | ✅ Present                         |
| Tipo                 |                         | `difficulty`/`cuisine_type` | ❌ Not mapped, needs extraction/mapping |
| Porciones            |                         | `servings`           | ✅ Present (as `servings`)         |
| Calorías             |                         | `calories_per_serving` | ✅ Present (as `calories_per_serving`) |
| Tags                 |                         | `tags`               | ✅ Present                         |
| Ingredientes (rel.)  | `ingredients` (list)    |                      | ✅ Present (but relation logic needed) |
| Hecho                |                         |                      | ❌ Not present, add to model       |
| Date                 | `created_at`/`updated_at` |                      | ✅ Present (as datetime fields)    |

#### Alacena (Pantry)
| Notion Property         | In Ingredient Model? | Notes/Action Needed                |
|-------------------------|---------------------|------------------------------------|
| Nombre (title)          | `name`              | ✅ Present                         |
| Categoría               |                     | ❌ Not present, add to model       |
| Stock alacena           |                     | ❌ Not present, add to model       |
| En lista de compras     |                     | ❌ Not present, add to model       |
| Unidad                  | `unit`              | ✅ Present                         |

#### Lista de Compras (Shopping List)
| Notion Property         | In Codebase?        | Notes/Action Needed                |
|-------------------------|---------------------|------------------------------------|
| Producto (title)        |                     | ❌ Not present, not modeled yet    |
| Cantidad                |                     | ❌ Not present, not modeled yet    |
| Categoría               |                     | ❌ Not present, not modeled yet    |
| Comprado                |                     | ❌ Not present, not modeled yet    |
| Origen (relation)       |                     | ❌ Not present, not modeled yet    |

#### Ingredientes (Ingredients)
| Notion Property         | In Ingredient Model? | Notes/Action Needed                |
|-------------------------|---------------------|------------------------------------|
| Receta (relation)       |                     | ❌ Not present, add to model       |
| Ingrediente (relation)  | `name` (maps to pantry) | Needs relation logic              |
| Cantidad Usada (title)  | `quantity`          | ✅ Present (as `quantity`)         |
| Unidad (text)           | `unit`              | ✅ Present                         |

- [ ] Identify missing fields and update the extraction logic and models to include them.
- [ ] Update the recipe model to include all necessary fields.
- [ ] Update Notion sync code to map and set all these properties for:
  - [ ] Recetas (Nombre, Porciones, Calorías, Tipo, Tags, Hecho, Date)
  - [ ] Ingredientes (Cantidad Usada, Unidad, Receta, Ingrediente)
  - [ ] Alacena (Nombre, Categoría, Stock alacena, Unidad, En lista de compras)
- [ ] Add/expand unit tests to verify property mapping for each DB.

**Concrete Next Steps:**
1. **Update Data Models**
   - Update Recipe model: add fields for `tipo`, `hecho`, `porciones`, `calorias`, `tags`, `date`, etc.
   - Update Ingredient model: add fields for `categoria`, `stock_alacena`, `en_lista_de_compras`, `receta_id`, `ingrediente_id`, etc.
   - Create/expand Shopping List model as needed.
2. **Update Extraction Logic**
   - Update `core/recipe/extractors/metadata.py` to extract all new fields:
     - [ ] Add extraction logic for `tipo` (e.g., look for "Tipo de comida" or similar in the text).
     - [ ] Ensure `porciones` and `calorias` are robustly extracted (already present, but check for edge cases).
     - [ ] Add extraction for `tags` (e.g., from a "Tags" or "Etiquetas" line, or infer from content).
     - [ ] Optionally extract `hecho` (default to `False` unless explicitly marked).
     - [ ] Extract `date` if present, or set to current date.
   - Update `core/recipe/processor.py` to use all extracted metadata fields when constructing a `Recipe`:
     - [ ] Update the call to `Recipe(...)` to pass all new fields.
     - [ ] Ensure `ingredients` and `instructions` are still populated as before.
   - **Example MetadataExtractor structure:**
     ```python
     class MetadataExtractor(BaseExtractor):
         def extract(self, content: str) -> Dict[str, Any]:
             return {
                 'title': self._extract_title(content),
                 'url': self._extract_url(content),
                 'porciones': self._extract_servings(content),
                 'calorias': self._extract_calories(content),
                 'tipo': self._extract_tipo(content),
                 'tags': self._extract_tags(content),
                 'hecho': self._extract_hecho(content),
                 'date': self._extract_date(content),
             }
         # ...implement _extract_tipo, _extract_tags, _extract_hecho, _extract_date...
     ```
   - **Update RecipeProcessor construction:**
     ```python
     metadata_dict = self.metadata_extractor.extract(content)
     recipe = Recipe(
         title=metadata_dict.get("title", "Desconocido"),
         tipo=metadata_dict.get("tipo"),
         porciones=metadata_dict.get("porciones"),
         calorias=metadata_dict.get("calorias"),
         tags=metadata_dict.get("tags", []),
         hecho=metadata_dict.get("hecho", False),
         date=metadata_dict.get("date"),
         ingredients=normalized_ingredients,
         instructions=sections["instructions"],
         source=metadata_dict.get("url", None),
     )
     ```
3. **Update Notion Sync Logic**
   - Map all new model fields to the correct Notion properties.
   - Ensure all relations are set.
4. **Add/Expand Unit Tests**
   - Test that all fields are correctly extracted, stored, and mapped.

### 2. Content Block Creation
- [ ] Design a function to convert a parsed recipe (or markdown) into Notion API block objects.
- [ ] Implement support for:
  - [ ] Headings (e.g., "Información general", "Preparación")
  - [ ] Paragraphs and rich text
  - [ ] Numbered lists (for steps)
  - [ ] Bulleted lists (for notes/variations)
  - [ ] Tables (for ingredients, calories)
- [ ] Update Notion sync logic to use the `children` parameter when creating/updating recipe pages.
- [ ] Add/expand tests to verify correct rendering in Notion.

### 3. Relations & Linking
- [ ] Implement logic to set relations:
  - [ ] Recetas → Ingredientes
  - [ ] Ingredientes → Recetas
  - [ ] Ingredientes → Alacena
- [ ] Ensure relations are bi-directional where appropriate.
- [ ] Add/expand tests to verify relations are set correctly.

### 4. Deduplication & Update Logic
- [ ] Implement lookup logic before creating new pages (by name/title) for:
  - [ ] Ingredientes
  - [ ] Alacena
- [ ] If an entry exists, update it instead of creating a new one.
- [ ] Add/expand tests to verify deduplication and update behavior.

### 5. Error Handling & Logging
- [ ] Standardize error handling for all Notion operations (custom exceptions, retries, clear messages).
- [ ] Improve logging for all sync actions (success, failure, skipped, etc.).
- [ ] Add CLI feedback for errors and summaries.
- [ ] Add/expand tests for error scenarios.

### 6. Advanced Notion Features (Optional)
- [ ] Identify any advanced features needed (e.g., rollups for ingredient usage).
- [ ] Implement and test as needed.

### 7. Testing & Validation
- [ ] Expand unit and integration tests for Notion sync, including edge cases (missing properties, permission errors, etc.).
- [ ] Mock Notion API where possible for fast, reliable tests.

### 8. Documentation & CLI Improvements
- [ ] Document Notion integration architecture, property mapping, and troubleshooting.
- [ ] Add CLI commands for Notion diagnostics (test connection, list DBs, validate schema).
- [ ] Improve CLI feedback for Notion sync (summary, error details, etc.).

## Clarification: Correct Notion Database Relationships

- **Recetas DB**
  - The **Ingredientes** relation should link to all ingredient rows in the **Ingredientes DB** that belong to that recipe (not to Alacena directly).
- **Ingredientes DB**
  - Each row should:
    - Link to one **Receta** (the parent recipe).
    - Link to one **Ingrediente** (the pantry item in Alacena DB).
- **Alacena DB**
  - Is referenced by both Recetas (indirectly, via Ingredientes) and Ingredientes (directly).

**What this means for sync logic:**
- When creating a recipe, the "Ingredientes" relation in Recetas DB must be set to the Notion page IDs of the ingredient rows created in Ingredientes DB for that recipe.
- When creating an ingredient row in Ingredientes DB, it must link to the parent recipe (Receta) and the pantry item (Alacena).

## Current Issues and Gaps (May 2024)

1. **Units (Unidades) Not Always Extracted or Synced**
   - The ingredient extraction logic does not always correctly extract the unit (e.g., 'g', 'ml', 'pieza') from the recipe text.
   - As a result, the 'Unidad' property in Ingredientes DB is sometimes empty in Notion.
   - This affects clarity and downstream automation (e.g., shopping list calculations).

2. **Recetas DB 'Ingredientes' Relation Not Populated Automatically**
   - The sync logic is not reliably populating the 'Ingredientes' relation in Recetas DB with the correct ingredient row IDs from Ingredientes DB.
   - This means the rollup for ingredient names in Recetas DB remains empty unless rows are linked manually.
   - The root cause may be timing issues, property name mismatches, or Notion API limitations.

**Next Steps:**
- Improve ingredient extraction and normalization to always extract and pass both quantity and unit.
- Ensure the sync logic sets the 'Ingredientes' relation in Recetas DB to the correct ingredient row IDs, matching the Notion schema exactly.
- Continue to test and debug the Notion API integration for reliability.

## Property Mapping Table

| Notion DB      | Property Name      | Type      | Model Field      | API Key         |
|----------------|-------------------|-----------|------------------|-----------------|
| Recetas        | Ingredientes       | Relation  | ingredient_ids   | Ingredientes    |
| Recetas        | Nombre             | Title     | title            | Nombre          |
| Recetas        | Porciones          | Number    | porciones        | Porciones       |
| Recetas        | Calorías           | Number    | calorias         | Calorías        |
| Recetas        | Tipo               | Select    | tipo             | Tipo            |
| Recetas        | Tags               | Multi-select | tags           | Tags            |
| Recetas        | Hecho              | Checkbox  | hecho            | Hecho           |
| Recetas        | Date               | Date      | date             | Date            |
| Ingredientes   | Cantidad Usada     | Title     | quantity         | Cantidad Usada  |
| Ingredientes   | Unidad             | Text      | unit             | Unidad          |
| Ingredientes   | Ingrediente        | Relation  | pantry_id        | Ingrediente     |
| Ingredientes   | Receta             | Relation  | receta_id        | Receta          |
| Alacena        | Nombre             | Title     | name             | Nombre          |
| Alacena        | Categoría          | Select    | category         | Categoría       |
| Alacena        | Stock alacena      | Number    | stock            | Stock alacena   |
| Alacena        | Unidad             | Select    | unit             | Unidad          |

## Sample API Payloads

**Recipe Creation Example:**
```json
{
  "Nombre": {"title": [{"text": {"content": "Pasta con Albóndigas"}}]},
  "Ingredientes": {"relation": [{"id": "abc123"}, {"id": "def456"}]},
  "Porciones": {"number": 4},
  "Calorías": {"number": 450},
  "Tipo": {"select": {"name": "Cena"}},
  "Tags": {"multi_select": [{"name": "Rápido"}]},
  "Hecho": {"checkbox": true},
  "Date": {"date": {"start": "2024-06-01"}}
}
```

**Ingredient Creation Example:**
```json
{
  "Cantidad Usada": {"title": [{"text": {"content": "200"}}]},
  "Unidad": {"rich_text": [{"text": {"content": "g"}}]},
  "Ingrediente": {"relation": [{"id": "pantry123"}]},
  "Receta": {"relation": [{"id": "recipe456"}]}
}
```

## Troubleshooting Table

| Symptom                        | Likely Cause                        | Solution                        |
|---------------------------------|-------------------------------------|----------------------------------|
| "New page" in Ingredientes      | Title property not set              | Set "Cantidad Usada" on create   |
| Rollup empty in Recetas         | Relation not populated              | Check property name, sync logic  |
| Unidad empty in Ingredientes    | Unit not extracted                  | Improve extraction regex         |
| Ingredientes relation empty     | Wrong property name or timing issue | Re-add relation, add delay       |
| Rollup shows nothing            | Ingrediente relation not set        | Ensure pantry link is set        |

## Quick Glossary

- **Recetas DB**: Main recipes database.
- **Ingredientes DB**: Per-recipe ingredient usage (quantity, unit, links to recipe and pantry).
- **Alacena DB**: Pantry/master ingredient list.
- **Relation**: Notion property linking to another database.
- **Rollup**: Notion property that aggregates data from a related database.
- **Title property**: The main text column in a Notion database (must be set for every row).
- **API Key**: The property name used in Notion API payloads.

## Future Features / Wishlist
- Ingredient substitutions and alternatives.
- Advanced shopping list generation (group by store section, urgency, etc.).
- Nutrition analysis and rollups.
- Multi-language ingredient support.
- Recipe versioning and history.
- User ratings and favorites.
- Automated meal planning calendar.

---

## 🚀 Async/Await Refactor Decision for Notion Sync

**Decision:**
- We have decided to proceed with a full async/await refactor for Notion syncing. This will involve updating the Notion sync logic and all HTTP calls to use an asynchronous client, enabling true concurrency and better scalability for future growth.

**Motivation:**
- The current sequential, blocking approach (with time.sleep) is robust but slow, especially for recipes with many ingredients.
- Async/await will allow us to run ingredient syncs concurrently, significantly reducing total processing time.
- This approach is more scalable and aligns with modern Python best practices for I/O-bound operations.

**Expected Benefits:**
- Faster recipe processing and syncing, especially for large batches.
- Improved responsiveness and throughput.
- Future-proofing the codebase for further automation and scaling.

**Approach:**
1. **Refactor Notion Sync Methods:**
   - Update all Notion sync logic (e.g., `sync_pantry_item`, `sync_ingredient`, `sync_recipe`, etc.) to use `async def` and `await` for HTTP calls.
   - Replace synchronous HTTP client (e.g., `requests`) with an async client (e.g., `httpx.AsyncClient` or `aiohttp`).
   - Ensure all Notion API interactions are non-blocking and compatible with asyncio.

2. **Update CLI and Processing Logic:**
   - Refactor CLI and processing functions to use `asyncio.run` and `asyncio.gather` for concurrent ingredient syncing.
   - Remove or minimize `time.sleep` calls, relying on async concurrency to handle throughput.

3. **Error Handling and Retries:**
   - Implement robust error handling for async operations, including retries and user-friendly error messages.
   - Ensure that failures in one sync operation do not block others.

4. **Testing and Validation:**
   - Add or update unit and integration tests to cover async sync logic.
   - Use async test frameworks (e.g., `pytest-asyncio`) as needed.

**Checklist:**
- [ ] Refactor Notion sync methods to async/await.
- [ ] Replace HTTP client with async-compatible library.
- [ ] Update CLI and processing logic for async execution.
- [ ] Remove unnecessary blocking/waiting.
- [ ] Add async error handling and retries.
- [ ] Update and expand tests for async code.
- [ ] Benchmark and validate performance improvements.

**Next Steps:**
- Begin by refactoring the Notion sync methods and updating the HTTP client.
- Incrementally update the CLI and processing logic to leverage async concurrency.
- Continuously test and benchmark to ensure correctness and performance gains.

## Performance Motivation & Observations

- Real-world tests show that syncing all ingredients for a single recipe can take 30–40 seconds sequentially, with individual ingredient syncs sometimes taking up to 5 seconds due to Notion API latency and required delays (`time.sleep`).
- This bottleneck is the primary motivation for introducing async/await and concurrent syncing.

## Concurrency & Rate Limiting

- When implementing async/await, monitor Notion API rate limits. Start with a conservative concurrency level (e.g., 3–5 parallel syncs) and adjust as needed to avoid hitting rate limits or being throttled.

## Alternative Approaches Considered

- A thread-based approach using `ThreadPoolExecutor` was considered for quick parallelism, but async/await was chosen for better scalability and alignment with modern Python practices.

## Async Migration Steps

1. Refactor pantry sync methods to async.
2. Refactor ingredient sync methods to async.
3. Refactor recipe sync methods to async.
4. Update CLI to orchestrate all syncs asynchronously.
5. Remove blocking `time.sleep` calls and replace with async-friendly waits if needed.
6. Add async error handling and retries.
7. Expand and update tests for async code.

### Real-World Test Data (May 2025)

Below are logs from a recent run, showing the time taken to sync each ingredient and the total time for ingredient syncing in a complex recipe:

```
Processing: test_12_complex_format.txt
  Extraction & parsing took 0.00 seconds
    Synced ingredient 'arroz arborio' in 0.39 seconds
    Synced ingredient 'lentejas' in 1.01 seconds
    Synced ingredient 'champiñones frescos' in 0.61 seconds
    Synced ingredient 'chorizo español, en rodajas' in 0.62 seconds
    Synced ingredient 'cebolla mediana' in 0.40 seconds
    Synced ingredient 'dientes de ajo' in 0.43 seconds
    Synced ingredient 'vino blanco seco' in 0.39 seconds
    Synced ingredient 'caldo de verduras' in 2.06 seconds
    Synced ingredient 'queso parmesano rallado' in 1.80 seconds
    Synced ingredient 'mantequilla' in 0.48 seconds
    Synced ingredient 'aceite de oliva' in 7.24 seconds
    Synced ingredient 'Sal' in 0.48 seconds
    Synced ingredient 'pimienta' in 0.36 seconds
    Synced ingredient 'crema de leche' in 0.40 seconds
    Synced ingredient 'perejil picado' in 0.47 seconds
    Synced ingredient 'tomillo fresco' in 0.38 seconds
    Synced ingredient 'pimentón dulce' in 1.84 seconds
  Ingredient sync took 66.26 seconds
```

**Key Timing Findings:**
- Ingredient sync times vary widely (from ~0.4s to over 7s per ingredient), with total sync for a complex recipe exceeding 1 minute.
- Notion API latency and sequential processing are major bottlenecks.

**Implications for Async Refactor:**
- Async/await will help mitigate the impact of slow API responses by allowing concurrent syncs, reducing total processing time.

## Concurrency & Rate Limiting

- When implementing async/await, monitor Notion API rate limits. Start with a conservative concurrency level (e.g., 3–5 parallel syncs) and adjust as needed to avoid hitting rate limits or being throttled.

## Alternative Approaches Considered

- A thread-based approach using `ThreadPoolExecutor` was considered for quick parallelism, but async/await was chosen for better scalability and alignment with modern Python practices.

## Async Migration Steps

1. Refactor pantry sync methods to async.
2. Refactor ingredient sync methods to async.
3. Refactor recipe sync methods to async.
4. Update CLI to orchestrate all syncs asynchronously.
5. Remove blocking `time.sleep` calls and replace with async-friendly waits if needed.
6. Add async error handling and retries.
7. Expand and update tests for async code.

### Real-World Test Data (May 2025)

Below are logs from recent runs, showing the time taken to sync each ingredient and the total time for ingredient syncing in a complex recipe:

```
Processing: test_12_complex_format.txt
  Extraction & parsing took 0.00 seconds
2025-05-14 23:27:24 - cli - INFO - Processing ingredient: arroz arborio
... (see full logs above for all ingredients) ...
    Synced ingredient 'arroz arborio' in 0.39 seconds
... (other ingredients: lentejas, champiñones frescos, etc.) ...
    Synced ingredient 'aceite de oliva' in 7.24 seconds
... (other ingredients) ...
  Ingredient sync took 66.26 seconds
Setting Ingredientes relation with IDs: [...]
2025-05-14 23:28:32 - notion.sync - INFO - Syncing recipe 'Risotto de Champiñones y Lentejas' with properties: {...}
2025-05-14 23:28:33 - notion.sync - ERROR - Failed to sync recipe Risotto de Champiñones y Lentejas: 'dict' object has no attribute 'metadata'
2025-05-14 23:28:33 - cli - ERROR - Failed to process test_12_complex_format.txt: Failed to sync recipe Risotto de Champiñones y Lentejas: 'dict' object has no attribute 'metadata'
ERROR: Failed to process test_12_complex_format.txt: Failed to sync recipe Risotto de Champiñones y Lentejas: 'dict' object has no attribute 'metadata'
Processing: test_05_unusual_format.txt
  Extraction & parsing took 0.00 seconds
  Ingredient sync took 0.00 seconds
2025-05-14 23:28:35 - notion.sync - INFO - Syncing recipe 'BATIDO ENERGÉTICO' with properties: {...}
2025-05-14 23:28:36 - notion.sync - ERROR - Failed to sync recipe BATIDO ENERGÉTICO: 'dict' object has no attribute 'metadata'
2025-05-14 23:28:36 - cli - ERROR - Failed to process test_05_unusual_format.txt: Failed to sync recipe BATIDO ENERGÉTICO: 'dict' object has no attribute 'metadata'
ERROR: Failed to process test_05_unusual_format.txt: Failed to sync recipe BATIDO ENERGÉTICO: 'dict' object has no attribute 'metadata'
```

**Key Findings:**
- Ingredient sync times vary widely (from ~0.4s to over 7s per ingredient), with total sync for a complex recipe exceeding 1 minute.
- Notion API latency and sequential processing are major bottlenecks.
- Errors such as `'dict' object has no attribute 'metadata'` indicate the need for more robust error handling and possibly data model validation.

**Implications for Async Refactor:**
- Async/await will help mitigate the impact of slow API responses by allowing concurrent syncs.
- Improved error handling and validation should be included in the async migration to catch and report issues early. 

---

## 🧪 Testing Strategy for Async/Content Blocks

- **Unit Tests:**
  - Test block generation functions to ensure correct Notion block structure for ingredients, steps, notes, etc.
  - Test error handling logic for sync failures, invalid data, and file movement.
- **Integration Tests:**
  - End-to-end tests for full recipe processing and Notion sync, including content blocks and relations.
  - Simulate partial failures (e.g., some ingredients fail to sync) and verify correct error handling and file movement.
- **Mocking Notion API:**
  - Use mocks for Notion API calls to enable fast, reliable tests without hitting real Notion endpoints.

---

## 🛡️ Error Handling & Recovery

- **Partial Failures:**
  - If some ingredients or blocks fail to sync, log the error, move the file to `errores`, and provide a summary to the user.
- **Rate Limiting/Batch Errors:**
  - Detect Notion API rate limits or errors mid-batch; implement exponential backoff and retry logic.
- **Recovery/Retry:**
  - Provide CLI commands or scripts to retry failed syncs from the `errores` directory.
  - Consider automated retries for transient errors.

---

## 🔄 Migration/Backfill Plan

- **Legacy Data:**
  - Identify existing Notion recipes missing content blocks or relations.
  - Develop a migration/backfill script to update these entries with the new block/content structure and relations.
- **Process:**
  - Scan Notion DBs for incomplete entries.
  - Re-process or patch as needed, logging all changes.

---

## 📣 User/Operator Feedback

- **CLI Output:**
  - After each batch run, print a summary: number of recipes processed, number succeeded, number failed, and reasons for failure.
  - For each failed recipe, log the filename and error details.
- **Reporting:**
  - Optionally, generate a report file (e.g., CSV or JSON) with processing results for auditing.

---

## ⏳ Rate Limiting and Throttling

- **Detection:**
  - Monitor Notion API responses for rate limit errors.
- **Response:**
  - Implement exponential backoff and configurable concurrency limits (e.g., max 3–5 parallel syncs).
  - Log and alert if rate limits are hit frequently.
- **Configuration:**
  - Allow concurrency and backoff settings to be configured via environment variables or CLI flags.

---

## 📚 Documentation & Developer Onboarding

- **Getting Started:**
  - Add a section to the documentation for setting up the project, installing dependencies, and configuring environment variables.
- **How to Contribute:**
  - Provide guidelines for contributing code, writing tests, and submitting pull requests.
- **Example CLI Commands:**
  - Document common CLI commands (e.g., process a single recipe, process all, dry run, retry errors).
- **Troubleshooting:**
  - Expand the troubleshooting section with common errors, solutions, and where to find logs. 
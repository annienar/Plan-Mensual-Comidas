# Plan Mensual Comidas

A system for managing monthly meal plans and recipes.

## Features

- Recipe generation using LLMs
- Recipe extraction from text
- Recipe validation and normalization
- Meal plan management
- Notion integration
- Comprehensive monitoring and logging

## Installation

```bash
# Clone the repository
git clone https://github.com/anavasquez/plan-mensual-comidas.git
cd plan-mensual-comidas

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"
```

## Configuration

1. Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

2. Update the environment variables in `.env` with your settings:
```env
# OpenAI API
OPENAI_API_KEY=your_api_key_here

# Notion API
NOTION_API_KEY=your_api_key_here
NOTION_DATABASE_ID=your_database_id_here
```

## Usage

### Recipe Generation

```python
from core import RecipeGenerationService
from core.infrastructure.llm.client import LLMClient

# Initialize the service
llm_client = LLMClient()
generation_service = RecipeGenerationService(llm_client)

# Generate a recipe
recipe = await generation_service.generate_recipe(
    prompt="Generate a recipe for a healthy dinner"
)
```

### Recipe Extraction

```python
from core import RecipeExtractionService
from core.infrastructure.llm.client import LLMClient

# Initialize the service
llm_client = LLMClient()
extraction_service = RecipeExtractionService(llm_client)

# Extract a recipe from text
recipe = await extraction_service.extract_recipe(
    text="""Ingredients:
- 2 cups flour
- 1 cup sugar
- 2 eggs

Instructions:
1. Mix ingredients
2. Bake at 350F"""
)
```

## Development

### Setup

1. Install development dependencies:
```bash
pip install -e ".[dev]"
```

2. Install pre-commit hooks:
```bash
pre-commit install
```

### Testing

Run tests with pytest:
```bash
pytest
```

### Code Quality

- Format code with black:
```bash
black .
```

- Sort imports with isort:
```bash
isort .
```

- Type checking with mypy:
```bash
mypy .
```

- Lint code with ruff:
```bash
ruff check .
```

## Project Structure

```
plan-mensual-comidas/
├── 📁 recipes/                    # 🎯 MAIN RECIPE WORKFLOW
│   ├── sin_procesar/             # Raw input recipes
│   ├── procesadas/               # Successfully processed recipes
│   ├── errores/                  # Failed processing recipes
│   └── json/                     # Final clean JSON recipes (production-ready)
├── 🏗️ core/                      # Application core
│   ├── application/              # Application layer
│   │   ├── recipe/              # Recipe processing
│   │   └── meal_plan/           # Meal planning
│   ├── domain/                  # Domain layer
│   │   ├── recipe/              # Recipe domain models
│   │   └── meal_plan/           # Meal plan domain
│   ├── infrastructure/          # Infrastructure layer
│   │   ├── llm/                 # LLM client (Ollama)
│   │   ├── notion/              # Notion integration
│   │   └── monitoring/          # System monitoring
│   ├── config/                  # Configuration management
│   ├── utils/                   # Utility functions
│   └── exceptions/              # Custom exceptions
├── 🧪 tests/                     # All test-related files
│   ├── unit/                    # Unit tests
│   ├── integration/             # Integration tests
│   ├── performance/             # Performance tests
│   ├── cli/                     # CLI tests
│   ├── fixtures/                # Test data and fixtures
│   └── test_results/            # Test output files
├── 📚 docs/                      # Documentation
│   ├── user-guide.md           # User documentation
│   ├── development.md          # Developer guide
│   └── features/               # Feature documentation
├── ⚙️ config/                    # Environment configurations
│   ├── development/            # Dev environment config
│   ├── production/             # Production config
│   └── testing/                # Test config
├── 📜 scripts/                   # Utility scripts
│   ├── development/            # Development helpers
│   └── refactoring/            # Code maintenance
├── 💾 var/                       # Variable system data (Unix convention)
│   ├── logs/                   # Runtime logs
│   ├── cache/                  # Application cache
│   └── test-results/           # Historical test logs
├── 🖥️ htmlcov/                   # HTML coverage reports
├── 📄 logs/                      # Application logs
├── pyproject.toml               # Project configuration & dependencies
└── README.md                   # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

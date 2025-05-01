# Plan Mensual Comidas

A Python-based recipe management system that automatically standardizes and processes recipes from various formats into structured data and beautiful Markdown files, ready for Notion integration.

License: CC BY-NC 4.0

## 🎯 Project Goals

- 📋 **Standardize & Normalize Recipes**: Automatically extract and structure recipe data from various sources
- 📝 **Generate Markdown Views**: Create Notion-style documents with consistent formatting
- 🔄 **Fully Automated Pipeline**: Single CLI tool to handle the entire process
- 🏗️ **Robust Foundation**: Comprehensive testing, clean architecture, and extensible design

## 🌟 Current Features (v1.4.9)

### 📥 Input Processing
- **Text Processing**
  - Reliable .txt file processing
  - Smart section detection (ingredients, steps, notes)
  - Bilingual support (Spanish/English)

### 🧮 Ingredient Parser
- **Smart Quantity Detection**
  - Mixed ASCII fractions (1 1/2, 3/4)
  - Quantity ranges (2–3, 1 or 2)
  - Glued units (100g)
  - Ingredients without quantities ("salt to taste")

### 📊 Metadata Extraction
- Servings information ("for X servings")
- Calorie content
- Recipe titles and authors
- Intelligent defaults for missing data

### 📱 Output Generation
- **Markdown Formatting**
  - Smart unit handling (singular/plural)
  - Normalized ingredient names
  - Structured sections
- **JSON Data**
  - Standardized recipe format
  - Machine-readable structure

### 🛠️ Development Features
- Unified CLI (`python -m core.gestor`)
- Centralized logging system
- >85% test coverage
- Comprehensive integration tests

## 🚀 Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/annienar/Plan-Mensual-Comidas.git
   cd Plan-Mensual-Comidas
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # or
   .venv\Scripts\activate     # Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Process recipes:**
   ```bash
   python -m core.gestor --procesar --generar-md
   ```

## 📁 Project Structure

```
Plan-Mensual-Comidas/
├── core/                 # Core processing modules
├── recetas/             # Recipe directories
│   ├── sin_procesar/    # Input recipes
│   └── procesadas/      # Processed outputs
└── tests/               # Test suite
```

## 🛠️ Development

- Python 3.13+
- pytest for testing
- Comprehensive test suite with >85% coverage
- Modular and extensible architecture

**Run tests:**
```bash
python -m pytest
```

## 🔜 Coming in v1.5

### Enhanced Processing
- Multi-page OCR support
- Complex PDF layouts
- Table and column detection
- Advanced image processing

### Integration & Automation
- Direct Notion API integration
- Webhook support
- REST API endpoints
- Automated workflow triggers

### Value-Add Features
- Nutrition analysis
- Shopping list generation
- Pantry management
- Recipe scaling

### Infrastructure
- Proper Python package structure
- CI/CD with GitHub Actions
- Comprehensive documentation
- Developer guides

## 📝 License

This project is licensed under Creative Commons Attribution-NonCommercial 4.0 International License.

- ✅ Share and adapt the material
- ❌ No commercial use
- ℹ️ Must provide attribution

## 🎯 End Goal

A turnkey solution that transforms free-form recipes into structured, polished documents ready for Notion or other platforms—eliminating manual formatting and standardization work.

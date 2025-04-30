# Plan Mensual Comidas

A Python-based recipe management system that processes recipes from various formats (TXT, PDF, images) into structured data and beautiful Markdown files.

[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)

## 🌟 Features

- 📝 **Multi-format Support**
  - Text files (.txt)
  - PDF documents with text extraction
  - Images via OCR (using Tesseract)

- 🔍 **Smart Ingredient Parsing**
  - Mixed fractions (1 1/2, ¾, etc.)
  - Multiple unit formats (g, kg, ml, l, cups)
  - Range quantities (2-3, 1 o 2)
  - Table and list layouts

- 📊 **Metadata Extraction**
  - Portions
  - Calories
  - Preparation steps
  - Source URLs

- 📱 **Beautiful Output**
  - Markdown generation
  - Structured JSON data
  - Original recipe backup

## 🚀 Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/annienar/Plan-Mensual-Comidas.git
   cd Plan-Mensual-Comidas
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # or
   .venv\Scripts\activate     # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Place your recipes in `V1.4/recetas/sin_procesar/`

5. Run the processor:
   ```bash
   python -m core.gestor --procesar --generar-md
   ```

## 📁 Project Structure

```
V1.4/
├── core/                 # Core processing modules
│   ├── extraer_txt.py   # Text extraction
│   ├── extraer_pdf.py   # PDF processing
│   ├── extraer_ocr.py   # OCR processing
│   └── generar_md.py    # Markdown generation
├── recetas/             # Recipe directories
│   ├── sin_procesar/    # Input recipes
│   └── procesadas/      # Processed outputs
└── tests/               # Test suite
```

## 🛠️ Development

- Python 3.13+
- 85%+ test coverage
- Modular architecture

Run tests:
```bash
python -m pytest
```

## 📝 License

This project is licensed under [Creative Commons Attribution-NonCommercial 4.0 International License](http://creativecommons.org/licenses/by-nc/4.0/).

- ✅ Share and adapt the material
- ❌ No commercial use
- ℹ️ Must provide attribution

## 🔜 Coming in v1.5

- Multi-page OCR & PDF support
- Advanced document layouts
- Notion integration
- Nutrition data enrichment
- Shopping list generation

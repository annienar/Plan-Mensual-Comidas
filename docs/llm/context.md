# LLM Context: Plan Mensual Comidas

**Purpose**: This document provides essential context for OTHER LLMs when working on this project.

## 🎯 Project Identity

**Name**: Plan Mensual Comidas (Monthly Meal Plan)  
**Type**: Commercial recipe management application for Spanish-speaking users  
**Core Function**: Upload recipes to Notion + smart pantry management + auto-generated shopping lists  
**Language**: Spanish field names throughout (nombre, cantidad, unidad, alacena, etc.)

## 🏛️ Commercial Requirements - CRITICAL

**This is a COMMERCIAL APPLICATION for sale. All dependencies must comply:**

### **LLM Model Restrictions**
- ✅ **ONLY MIT or Apache 2.0 licensed models**
- ✅ **Currently using**: Phi (MIT), LLaVA-Phi3 (MIT), Moondream 2 (Apache 2.0)
- ❌ **PROHIBITED**: Llama models (custom license), GPT models (proprietary), Claude models (proprietary)
- ❌ **NO EXTERNAL API CALLS** to proprietary LLM services

### **Privacy & Data Control**
- ✅ **Local LLM deployment only** (via Ollama)
- ✅ **User data stays with user** (stored in their Notion)
- ✅ **No telemetry or external data sharing**

## 🗄️ Current System Architecture

### **Data Flow**
```
Text/Image Recipe → Local LLM Processing → Structured Data → User's Notion Database
```

### **Core Databases** (Notion)
- **Recetas** (Recipes) - nombre, ingredientes, instrucciones, porciones
- **Ingredientes** (Ingredients) - Master ingredient catalog  
- **Alacena** (Pantry) - User's current ingredient stock
- **Lista_Compras** (Shopping Lists) - Auto-generated from recipes vs pantry

### **Current Status**
- ✅ **Phase 1 Complete**: Recipe processing (124/124 tests passing, 100% success rate)
- 🔄 **Phase 1.5**: Adding multimodal processing (LLaVA-Phi3 integration)
- 📋 **Phase 2 Ready**: Enhanced Pantry Management (4-week sprint planned)

## 🧠 LLM Integration Details

### **Current Setup**
- **Ollama Runtime**: Local LLM server
- **Primary Model**: Phi (1.6GB, MIT) - Text recipe processing
- **Multimodal Model**: LLaVA-Phi3 (3.8GB, MIT) - Image/PDF processing
- **Backup Model**: Moondream 2 (1.7GB, Apache 2.0)

### **Processing Capabilities**
- ✅ Spanish recipe text parsing and structuring
- ✅ Ingredient extraction with quantity normalization  
- ✅ Spanish/English mixed content handling
- 🔄 Image-based recipe extraction (in progress)
- 🔄 PDF document processing (in progress)

### **Prompt Strategy** (Spanish-first)
```python
# Example prompt pattern
"Eres un asistente especializado en recetas de cocina. 
Analiza el siguiente texto y extrae la información estructurada en JSON:
{
  'nombre': 'nombre de la receta',
  'ingredientes': [{'nombre': 'ingrediente', 'cantidad': 'X', 'unidad': 'unidad'}],
  'instrucciones': ['paso 1', 'paso 2'],
  'porciones': X
}"
```

## 🎯 Phase 2 Goals - NEXT DEVELOPMENT PHASE

### **Enhanced Pantry Management**
Transform from "recipe processor" to "complete meal planning solution":

1. **Real-time Pantry Tracking** - Stock levels, expiration dates
2. **Recipe-Pantry Integration** - Check availability when adding recipes
3. **Smart Shopping Lists** - Auto-generate missing ingredients
4. **LLM Intelligence Layer** - Ingredient matching, substitutions, optimizations

### **Target User Workflow**
```
User adds recipe → LLM processes → System checks pantry stock → 
Shows "Available: X, Need to buy: Y" → Missing items auto-added to shopping list →
User shops & marks purchased → Pantry stock auto-updates
```

## 🛠️ Development Environment

### **Technology Stack**
- **Python 3.9+** - Core application language
- **Ollama** - Local LLM deployment platform
- **Notion API** - Database and user interface
- **Pytest** - Testing framework (124/124 tests passing)
- **macOS/Apple Silicon** - Primary development environment

### **Project Structure**
```
project/
├── src/recipe/          # Core recipe processing
├── src/llm/            # LLM integration
├── src/notion/         # Notion API integration  
├── tests/              # Test suite (124 passing)
├── docs/               # Documentation (consolidated)
└── recetas_sin_procesar/ # User recipe input folder
```

### **Key Configuration**
```python
# Spanish field names throughout
RECIPE_FIELDS = {
    "nombre": str,           # Recipe name
    "ingredientes": list,    # Ingredients list
    "cantidad": float,       # Quantity
    "unidad": str,          # Unit (gramos, tazas, etc.)
    "instrucciones": list,   # Instructions
    "porciones": int         # Servings
}
```

## 🔧 When Contributing Code

### **Critical Guidelines**
1. **Maintain Spanish field names** - Never change to English
2. **Commercial license compliance** - Only MIT/Apache 2.0 dependencies
3. **Local processing only** - No external API calls for LLM processing
4. **Test coverage** - Maintain 100% recipe processing accuracy
5. **Notion-first** - All data ultimately stored in user's Notion

### **Current Standards**
- **Language**: Python 3.9+, Spanish domain terms
- **Testing**: Pytest, aim for 100% critical path coverage  
- **Documentation**: Consolidated structure (9 core files)
- **Privacy**: Local LLM processing, user data ownership

### **File Naming Conventions**
- **Spanish concepts**: `alacena.py`, `lista_compras.py`, `ingredientes.py`
- **English technical**: `llm_service.py`, `notion_client.py`, `recipe_processor.py`

## 🚀 Immediate Development Context

### **Current Branch**: `LLM-Integration` (ready for merge to main)
### **Next Branch**: `Enhanced-Pantry-Management` (Phase 2)

### **Immediate Tasks**
1. Complete LLaVA-Phi3 multimodal integration testing
2. Merge LLM-Integration branch to main  
3. Begin Enhanced Pantry Management implementation
4. Design Notion pantry database schema

### **Key Success Metrics**
- Recipe processing: 100% accuracy maintained
- Response time: <3 seconds for text, <10 seconds for images
- Memory usage: <4GB during processing
- Commercial compliance: 100% (no proprietary models)

## ⚠️ Common Pitfalls to Avoid

1. **Language Mixing**: Don't anglicize Spanish field names
2. **Model Licensing**: Never suggest non-MIT/Apache models
3. **External APIs**: Don't add proprietary LLM service calls
4. **OCR Dependencies**: System uses LLM-only approach (no OCR libraries)
5. **Breaking Tests**: Maintain the 124/124 passing test suite

---

## 🎯 Key Takeaway for LLMs

**This is a Spanish-language, commercial meal planning app with local LLM processing and Notion integration. All contributions must maintain commercial license compliance, Spanish domain language, and local-first privacy principles.**

**Current Status**: Recipe foundation complete, multimodal processing in progress, pantry management next phase.

*This context file helps other LLMs understand the project's commercial nature, technical constraints, and development priorities.* 
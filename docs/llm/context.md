# LLM Context: Plan Mensual Comidas

**Purpose**: This document provides essential context for OTHER LLMs when working on this project.

## 🎯 Project Identity

**Name**: Plan Mensual Comidas (Monthly Meal Plan)  
**Type**: Commercial recipe management application for Spanish-speaking users  
**Core Function**: Upload recipes to Notion + smart pantry management + auto-generated shopping lists  
**Language**: **SPANISH-ONLY** - All recipes translated to Spanish regardless of input language
**Field Names**: Spanish throughout (nombre, cantidad, unidad, alacena, etc.)

## 🚨 RECENT CRITICAL CHANGES

### **LLM Model Migration Completed**
- **FROM**: Phi model (1.6GB) - **FAILED** Spanish language prompts
- **TO**: LLaVA-Phi3 (2.9GB) - **EXCELLENT** Spanish understanding + Vision ready
- **Impact**: Core functionality restored, Spanish translation working perfectly
- **Performance**: 30-120s processing (vs 10-30s) but significantly better accuracy

### **Spanish-Only Translation System Implemented**
- **Requirement**: User's Notion database is entirely in Spanish
- **Implementation**: ALL input recipes (English/French/etc.) → Spanish output
- **Translation Rules**: Explicit mappings (chicken→pollo, beef→carne, cup→taza)
- **System Behavior**: No multi-language options, Spanish-forced prompts only
- **Notion Compatibility**: 100% Spanish properties (nombre, porciones, calorias)

## 🏛️ Commercial Requirements - CRITICAL

**This is a COMMERCIAL APPLICATION for sale. All dependencies must comply:**

### **LLM Model Restrictions** (Updated)
- ✅ **ONLY MIT or Apache 2.0 licensed models**
- ✅ **PRIMARY MODEL**: LLaVA-Phi3 (MIT) - Superior Spanish support + Vision capabilities
- ❌ **DEPRECATED**: Phi (MIT) - Poor Spanish language performance, replaced
- ✅ **BACKUP**: Moondream 2 (Apache 2.0) - Vision backup only
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

### **Current Setup** (Updated)
- **Ollama Runtime**: Local LLM server
- **Primary Model**: LLaVA-Phi3 (2.9GB, MIT) - **ACTIVE** Spanish text + Vision processing
- **Deprecated Model**: ~~Phi (1.6GB, MIT)~~ - **REMOVED** due to poor Spanish support
- **Backup Model**: Moondream 2 (1.7GB, Apache 2.0) - Vision backup only

### **Processing Capabilities** (Updated)
- ✅ **SPANISH-ONLY TRANSLATION**: ALL recipes translated to Spanish regardless of input language
- ✅ Spanish recipe text parsing and structuring with LLaVA-Phi3
- ✅ Ingredient extraction with Spanish quantity normalization (taza, cda, cdta)
- ✅ **Forced Translation**: English→Spanish (chicken→pollo, cup→taza, heat→calentar)
- ✅ **No Multi-Language**: System operates in Spanish-only mode for Notion compatibility
- 🔄 Image-based recipe extraction (infrastructure ready with LLaVA-Phi3)
- 🔄 PDF document processing (infrastructure ready with LLaVA-Phi3)

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

---

## 🚨 RECENT CRITICAL CHANGES - MUST READ

### **1. LLM Model Migration: Phi → LLaVA-Phi3**
- **Problem**: Phi model completely failed Spanish prompts (returned empty responses)
- **Solution**: Migrated to LLaVA-Phi3 (MIT license) for superior Spanish support
- **Impact**: Core functionality restored, 2.9GB model vs 1.6GB, 120s timeout vs 45s
- **Status**: ✅ **COMPLETED** - LLaVA-Phi3 is now the primary and only model

### **2. Spanish-Only Translation System**
- **Requirement**: User's entire system (Notion DB, UI) operates in Spanish
- **Implementation**: **ALL recipes translated to Spanish regardless of input language**
- **Examples**: "Chicken Rice" → "Pollo con Arroz", "2 cups" → "2 tazas", "Heat oil" → "Calentar aceite"
- **Code Impact**: Removed multi-language configuration, Spanish-forced prompts only
- **Status**: ✅ **COMPLETED** - No English outputs allowed in final results

### **3. Configuration Changes Made**
```python
# Core model configuration now:
DEFAULT_MODEL = "llava-phi3"  # Changed from "phi"
TIMEOUT = 120  # Increased for larger model
LANGUAGE = "spanish"  # Always Spanish, no options
TEMPERATURE = 0.1  # Low for consistent translation

# Spanish translation rules implemented:
TRANSLATIONS = {
    "chicken": "pollo", "beef": "carne", "onion": "cebolla",
    "cup": "taza", "tbsp": "cda", "tsp": "cdta",
    "heat": "calentar", "mix": "mezclar", "add": "agregar"
}
```

### **4. For Future LLM Work**
- **Model Choice**: Always use LLaVA-Phi3, never Phi
- **Language Handling**: Force Spanish translation, no multi-language support
- **Prompts**: Include explicit translation rules in all recipe prompts
- **Timeout**: Use 120s minimum for LLaVA models
- **Testing**: Verify Spanish output regardless of input language

*This context file helps other LLMs understand the project's commercial nature, technical constraints, and development priorities.* 
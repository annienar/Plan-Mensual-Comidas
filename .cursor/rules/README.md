# 🛠️ Cursor Rules Configuration

This directory contains comprehensive rules for the Spanish Recipe Processing project that guide development, maintain consistency, and enforce best practices.

## 📋 Rules Overview

### **Core Development Rules**

| Rule File | Purpose | Key Features |
|-----------|---------|--------------|
| `git.json` | Git workflow standards | Commit formats, branch naming, hooks |
| `python.json` | Python code standards | Style, typing, naming, testing |
| `project.json` | Project structure | Directory layout, testing, documentation |

### **Workflow & Process Rules**

| Rule File | Purpose | Key Features |
|-----------|---------|--------------|
| `workflow.json` | File lifecycle & automation | Creation, modification, archival, documentation triggers |
| `data-pipeline.json` | Recipe processing pipeline | Validation, quality assurance, monitoring |
| `performance.json` | Performance standards | Thresholds, monitoring, optimization |

### **Domain-Specific Rules**

| Rule File | Purpose | Key Features |
|-----------|---------|--------------|
| `spanish-localization.json` | Spanish language processing | Field naming, terminology, text processing |
| `llm-integration.json` | LLM usage standards | Context management, prompts, validation |

## 🚫 **Anti-Duplication Enforcement**

**Critical Rule**: Never create new documentation files when content belongs in existing ones.

### **✅ Update Existing Files Instead**
- **README.md** (this file) - Overview, quick start, rule summaries
- **RULES_ANALYSIS.md** - Detailed analysis, lessons learned, improvements
- **docs/development.md** - Development guides and standards
- **Root README.md** - Project overview

### **❌ Don't Create These Types of Files**
- "Strategy" files (content belongs in analysis or README)
- "Template" files (templates belong in docs/templates/)
- "Guide" files (guides belong in existing development docs)
- Duplicate overview files

### **Decision-Driven Process**
1. **Ask First**: "Does this belong in an existing file?"
2. **Create ADR Only**: For actual decisions (`docs/decisions/`)
3. **Update Existing**: Enhance current documentation
4. **Reference, Don't Copy**: Link to decisions, don't duplicate

## 🎯 **Recommended New Rules Based on Your Workflow**

### **1. 📁 Workflow Rules (`workflow.json`)**
**Why You Need This**: Based on our systematic approach to file organization and documentation updates.

```json
"file_lifecycle": {
  "archival": {
    "archive_location": "archive/",
    "preserve_git_history": true,
    "document_reason": true
  }
}
```

**Benefits**:
- ✅ Enforces our "archive, don't delete" approach
- ✅ Automatic documentation updates when structure changes
- ✅ Consistent refactoring patterns

### **2. 🤖 LLM Integration Rules (`llm-integration.json`)**
**Why You Need This**: Your recipe processing relies heavily on LLM integration.

```json
"context_management": {
  "preserve_spanish_context": true,
  "max_context_tokens": 4000
},
"response_validation": {
  "required_fields": ["nombre", "ingredientes", "preparacion"]
}
```

**Benefits**:
- ✅ Consistent LLM usage patterns
- ✅ Cost management and performance monitoring
- ✅ Spanish-specific context handling

### **3. 🔄 Data Pipeline Rules (`data-pipeline.json`)**
**Why You Need This**: Your recipe processing workflow is complex and needs standardization.

```json
"processing_stages": {
  "extraction": {
    "methods": ["llm", "ocr", "text_parsing"],
    "fallback_chain": ["llm", "rule_based"]
  }
}
```

**Benefits**:
- ✅ Standardized processing workflow
- ✅ Quality assurance automation
- ✅ Performance monitoring

### **4. 🇪🇸 Spanish Localization Rules (`spanish-localization.json`)**
**Why You Need This**: Your entire project is Spanish-focused with specific terminology needs.

```json
"recipe_terminology": {
  "required_spanish_fields": [
    "nombre", "ingredientes", "preparacion"
  ],
  "measurement_units": ["ml", "l", "taza", "cucharada"]
}
```

**Benefits**:
- ✅ Enforces Spanish field naming
- ✅ Validates cooking terminology
- ✅ Handles Spanish text processing correctly

### **5. ⚡ Performance Rules (`performance.json`)**
**Why You Need This**: Recipe processing needs performance monitoring and optimization.

```json
"recipe_processing": {
  "time_thresholds": {
    "single_recipe_max_seconds": 30,
    "llm_response_max_seconds": 15
  }
}
```

**Benefits**:
- ✅ Performance thresholds for recipe processing
- ✅ Resource usage monitoring
- ✅ Automatic optimization

## 🚀 **How These Rules Help Your Workflow**

### **1. Automatic Documentation Updates**
```yaml
# When you change directory structure:
- Updates: docs/directory-structure.md
- Runs: python Documentation/tools/run_automation.py
- Archives: old structure documentation
```

### **2. Recipe Processing Quality Assurance**
```yaml
# For each recipe processed:
- Validates: Spanish field names required
- Checks: ingredient format compliance  
- Monitors: processing time thresholds
- Logs: performance metrics
```

### **3. LLM Integration Standards**
```yaml
# For LLM interactions:
- Enforces: Spanish context preservation
- Validates: required recipe fields
- Manages: token usage and costs
- Handles: error scenarios with fallbacks
```

### **4. Consistent File Management**
```yaml
# For file operations:
- Creation: uses templates with headers
- Modification: updates timestamps
- Archival: preserves history, documents reason
- Cleanup: follows Unix standards
```

## 📊 **Implementation Priority**

### **🔴 High Priority** (Implement First)
1. **`workflow.json`** - Critical for your file management patterns
2. **`spanish-localization.json`** - Core to your domain
3. **`data-pipeline.json`** - Essential for recipe processing

### **🟡 Medium Priority** (Implement Second)  
4. **`llm-integration.json`** - Important for AI features
5. **`performance.json`** - Important for optimization

## 💡 **Usage Examples**

### **Commit Messages with New Scopes**
```bash
feat(recipes): add PDF extraction support
fix(llm): resolve Spanish context handling
docs(pipeline): update processing workflow guide
perf(cache): optimize recipe lookup performance
```

### **Spanish Field Validation**
```python
# Enforced by rules:
class Receta:
    nombre: str  # ✅ Spanish field name
    ingredientes: List[str]  # ✅ Required field
    preparacion: str  # ✅ Required field
    porciones: int  # ✅ Spanish terminology
```

### **Automatic Documentation Updates**
```bash
# When you modify core/application/recipe/
# Rules automatically:
1. Update docs/api.md
2. Run documentation automation
3. Update directory structure docs
4. Log changes for review
```

## 🔧 **Getting Started**

1. **Review Rules**: Start with `workflow.json` and `spanish-localization.json`
2. **Test Integration**: Use rules in a feature branch
3. **Gradual Adoption**: Implement rules one category at a time
4. **Monitor Impact**: Check rule effectiveness with scripts

## 📈 **Benefits Summary**

- ✅ **Consistency**: Standardized Spanish recipe processing
- ✅ **Quality**: Automated validation and quality checks  
- ✅ **Performance**: Monitoring and optimization guidelines
- ✅ **Documentation**: Automatic updates when code changes
- ✅ **Workflow**: Streamlined file management and archival
- ✅ **Localization**: Proper Spanish language handling
- ✅ **Integration**: LLM usage best practices

## 🚫 **Anti-Duplication System**

### **Problem Solved**
The rules prevent creating unnecessary documentation by:
- ✅ **Single Source Principle**: Each piece of info has exactly one canonical location
- ✅ **Update Existing**: Always enhance existing docs rather than create new ones
- ✅ **Smart Consolidation**: Detect when content should be merged
- ✅ **Reference Chain**: Use cross-references instead of copying content

### **Decision-Driven Updates**
When you make decisions:
1. **Create ADR**: `docs/decisions/NNNN-title.md` (canonical decision)
2. **Update Existing Docs**: Enhance README.md, development.md, etc. (don't create new)
3. **Add References**: Link to decisions, don't copy decision content
4. **Validate**: Ensure no duplicate content exists

### **Content Hierarchy**
```
README.md (Overview + quick start)
├── docs/development.md (Detailed development guide)
├── docs/decisions/ (Decision records - referenced, not copied)
├── docs/api.md (API reference - generated from code)
└── docs/directory-structure.md (Structure guide)
```

**Rule**: Always ask "Does this information belong in an existing file?" before creating new documentation.

These rules transform your development experience from manual consistency checking to automated quality assurance that understands your Spanish recipe processing domain! 🚀 
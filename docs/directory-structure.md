# 📁 Directory Structure Guide

This document provides a comprehensive overview of the Plan Mensual Comidas project structure.

## 🎯 Overview

The project follows a clean, organized structure with clear separation of concerns:
- **Recipe workflow** directories for processing pipeline
- **Domain-driven design** in core application
- **Comprehensive testing** structure
- **Unix conventions** for system data

## 📂 Complete Directory Structure

```
plan-mensual-comidas/
├── 📁 recipes/                    # 🎯 MAIN RECIPE WORKFLOW
│   ├── sin_procesar/             # Raw input recipes (txt, pdf, images)
│   ├── procesadas/               # Successfully processed recipes
│   ├── errores/                  # Failed processing recipes
│   └── json/                     # Final clean JSON recipes (production-ready)
├── 🏗️ core/                      # Application core
│   ├── domain/                  # Business logic
│   │   ├── recipe/              # Recipe domain models & services
│   │   └── meal_plan/           # Meal planning domain
│   ├── application/             # Use cases and workflows
│   │   ├── recipe/              # Recipe processing workflows
│   │   └── meal_plan/           # Meal planning workflows
│   ├── infrastructure/          # External integrations
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
├── ⚙️ config/                    # Environment configurations
│   ├── development/            # Dev environment config
│   ├── production/             # Production config
│   └── testing/                # Test config
├── 💾 var/                       # Variable system data (Unix convention)
│   ├── logs/                   # Runtime logs
│   ├── cache/                  # Application cache
│   └── test-results/           # Historical test logs
├── 📜 scripts/                   # Utility scripts & automation
├── 📚 docs/                      # Documentation
├── 🖥️ htmlcov/                   # HTML coverage reports
└── 📄 logs/                      # Application logs
```

## 🎯 Directory Purpose Guide

### 📁 **Recipe Workflow (`recipes/`)**
The main recipe processing pipeline:

- **`sin_procesar/`**: Raw recipe inputs (text, PDF, images)
- **`procesadas/`**: Successfully processed recipes in intermediate format
- **`errores/`**: Recipes that failed processing (for debugging)
- **`json/`**: Final production-ready JSON recipes

### 🏗️ **Core Application (`core/`)**
The heart of the application following clean architecture:

- **`domain/`**: Business logic and models (pure Python, no dependencies)
- **`application/`**: Use cases and application services
- **`infrastructure/`**: External service integrations (LLM, Notion, etc.)
- **`config/`**: Configuration management
- **`utils/`**: Shared utility functions
- **`exceptions/`**: Custom exception hierarchy

### 🧪 **Testing (`tests/`)**
Comprehensive test coverage:

- **`unit/`**: Fast, isolated unit tests
- **`integration/`**: Service integration tests
- **`performance/`**: Performance and load tests
- **`cli/`**: Command-line interface tests
- **`fixtures/`**: Test data and sample files
- **`test_results/`**: Test output and artifacts

### ⚙️ **Configuration (`config/`)**
Environment-specific configurations:

- **`development/`**: Local development settings
- **`production/`**: Production environment settings
- **`testing/`**: Test environment configuration

### 💾 **Variable Data (`var/`)**
Following Unix conventions for variable data:

- **`logs/`**: Runtime application logs
- **`cache/`**: Application cache files
- **`test-results/`**: Historical test execution logs

## 🚀 Workflow Examples

### Recipe Processing Flow
```
1. Raw recipe → recipes/sin_procesar/
2. Processing → core/application/recipe/extractors/
3. Success → recipes/procesadas/
4. Validation & Cleanup → recipes/json/
5. Error handling → recipes/errores/
```

### Development Workflow
```
1. Code changes → core/
2. Unit tests → tests/unit/
3. Integration tests → tests/integration/
4. Documentation → docs/
5. Configuration → config/
```

## 📋 Best Practices

### File Organization
- **Group related files** together (domain, infrastructure, etc.)
- **Use descriptive names** (sin_procesar vs raw, json vs final)
- **Follow conventions** (tests/, docs/, var/)
- **Separate concerns** (business logic vs infrastructure)

### Development Tips
- **Start in recipes/sin_procesar/** for new recipe testing
- **Check tests/fixtures/** for example data
- **Use var/logs/** for debugging runtime issues
- **Review docs/** before making changes
- **Follow core/domain/** patterns for new features

This structure supports scalable development, clear separation of concerns, and easy navigation for both developers and automated tools. 
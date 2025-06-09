# Development Guide

## 🚀 Quick Setup

### Prerequisites
- Python 3.9+
- Git
- **Ollama** (for LLM integration)
- Virtual environment tool: `venv` or `virtualenv`
- (Optional) Notion API credentials for integration tests

### Installation Steps
```bash
# 1. Clone repository
git clone https://github.com/yourusername/plan-mensual-comidas.git
cd plan-mensual-comidas

# 2. Set up virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install Ollama models (commercial-licensed only)
ollama pull llava-phi3  # Primary model (Spanish + Vision)
# Note: phi model deprecated due to poor Spanish support

# 5. Set up environment variables
cp .env.example .env
# Edit .env with your Notion credentials

# 6. Install pre-commit hooks (recommended)
pre-commit install

# 7. Run tests to verify setup
pytest
```

## 🧪 Testing

### Running Tests
```bash
# Run all tests
pytest

# Run specific test categories
pytest tests/unit/          # Unit tests
pytest tests/integration/   # Integration tests
pytest tests/recipe/        # Recipe domain tests

# Run with coverage
pytest --cov=core --cov-report=html

# Run specific test file
pytest tests/recipe/test_models.py -v
```

### Test Structure
```
tests/
├── unit/           # Fast, isolated unit tests
├── integration/    # Integration tests with external services
├── recipe/         # Recipe domain-specific tests
└── fixtures/       # Test data and fixtures
```

### Writing Tests
- **Unit Tests**: Test individual functions/classes in isolation
- **Integration Tests**: Test component interactions
- **Fixtures**: Use `pytest` fixtures for common test data
- **Mocking**: Mock external services (Notion, LLM) in unit tests

### Current Test Status
- ✅ **124/124 recipe tests passing (100%)**
- ✅ Recipe domain fully tested
- ✅ LLM integration foundation tested
- 🔄 Pantry management tests (in development)

## 📝 Code Standards

### Python Style
- **PEP 8** compliance (enforced by `flake8`)
- **Black** for automatic code formatting
- **Type hints** for all public functions
- **Docstrings** for all public classes and methods

### Code Quality Tools
```bash
# Format code
black .

# Check linting
flake8

# Type checking
mypy core/

# Security scanning
bandit -r core/
```

### Documentation Standards
- **Docstrings**: Google-style docstrings
- **Type Hints**: Use `typing` module annotations
- **Comments**: Explain "why", not "what"
- **README**: Keep project README up-to-date

## 🌿 Git Workflow

### Branch Strategy
- **`main`**: Production-ready code
- **`feature/<name>`**: New features
- **`bugfix/<name>`**: Bug fixes
- **`LLM-Integration`**: Major architectural changes

### Commit Messages
```bash
# Format: type(scope): description
feat(recipe): add ingredient normalization
fix(llm): handle empty responses gracefully
docs(api): update endpoint documentation
test(pantry): add pantry availability tests
```

### Pull Request Process
1. **Create feature branch** from `main`
2. **Implement changes** with tests
3. **Run full test suite** (`pytest`)
4. **Update documentation** if needed
5. **Create PR** with clear description
6. **Code review** by team member
7. **Merge** after approval

## 🏗️ Architecture Guidelines

### Project Structure
```
plan-mensual-comidas/
├── 📁 recipes/                    # 🎯 MAIN RECIPE WORKFLOW
│   ├── sin_procesar/             # Raw input recipes (txt, pdf, images)
│   ├── procesadas/               # Successfully processed recipes
│   ├── errores/                  # Failed processing recipes
│   └── json/                     # Final clean JSON recipes (production-ready)
├── 🏗️ core/                      # Application core
│   ├── domain/                  # Business logic (Recipe, Ingredient, Pantry)
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
└── 📚 docs/                      # Documentation
```

### Design Principles
- **Domain-Driven Design**: Business logic in `domain/`
- **Clean Architecture**: Dependencies point inward
- **Single Responsibility**: Each class has one reason to change
- **Spanish Language**: Field names in Spanish (nombre, cantidad, unidad)

### LLM Integration Guidelines (Updated December 2024)
- **Commercial Compliance**: Only MIT/Apache 2.0 licensed models
- **Primary Model**: LLaVA-Phi3 (replaced Phi due to poor Spanish support)
- **Spanish-Only Translation**: ALL recipes must be translated to Spanish regardless of input language
- **Error Handling**: Graceful degradation when LLM unavailable
- **Prompt Engineering**: Spanish-forced prompts with explicit translation rules
- **Response Validation**: Always validate Spanish LLM responses
- **Timeout Configuration**: 120s for LLaVA-Phi3 (larger model)

## 🔧 Development Tools

### Useful Commands
```bash
# Development server (if applicable)
python -m core.cli serve

# Process a test recipe
python -m core.cli process_recipe "test_recipe.txt"

# Check system status
python -m core.cli status

# Run specific component tests
python -m pytest tests/recipe/ -v
```

### Debugging
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG

# Run with debugger
python -m pdb -m core.cli process_recipe "test.txt"

# Profile performance
python -m cProfile -o profile.stats -m core.cli process_recipe "test.txt"
```

### IDE Setup
- **VS Code**: Use Python extension, configure linting/formatting
- **PyCharm**: Configure code style to match Black/flake8
- **Vim/Neovim**: Use LSP with pylsp or pyright

## 🚨 Common Issues & Solutions

### Setup Issues
**"Ollama not found"**
```bash
# Install Ollama
brew install ollama  # macOS
# or download from ollama.com
```

**"Tests failing"**
```bash
# Check Python version
python --version  # Should be 3.9+

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Development Issues
**"Import errors"**
```bash
# Ensure you're in virtual environment
source .venv/bin/activate

# Install in development mode
pip install -e .
```

**"LLM tests failing"**
```bash
# Check Ollama is running
ollama list

# Pull required models
ollama pull phi
ollama pull llava-phi3
```

## 📊 Performance Guidelines

### Optimization Targets
- Recipe processing: <10 seconds (single recipe)
- Batch processing: <2 minutes (10 recipes)
- Pantry checks: <2 seconds
- Test suite: <30 seconds
- Memory usage: <500MB

### Performance Optimizations Implemented

#### Intelligent Batch Processing (December 2024)
- **Adaptive Batch Sizing**: Automatically adjusts batch size (2-10 recipes) based on system resources and success rates
- **Recipe Complexity Analysis**: Sorts recipes by complexity (simple first) for optimal throughput
- **Error Recovery**: Multiple fallback strategies prevent batch failures
- **Performance Tracking**: Continuous monitoring and optimization

**Performance Targets:**
- Complexity analysis: <1ms per recipe
- Adaptive batch sizing: <0.1ms per calculation
- Recipe sorting: <100ms for 100 recipes
- History management: <0.5ms per update

#### Enhanced Caching System (December 2024)  
- **Content Similarity Matching**: 75% similarity threshold for cache hits
- **Spanish-English Unit Mapping**: cups→tazas, tablespoons→cucharadas
- **Recipe Type Detection**: pasta, pollo, arroz classification
- **Expected Speedup**: 60-80% for similar content

### Profiling
```bash
# Profile memory usage
python -m memory_profiler core/cli.py

# Profile CPU usage
python -m cProfile -s cumulative core/cli.py

# Test performance optimizations
pytest tests/performance/test_performance.py::TestPerformance::test_performance_benchmark_suite -v

# Run intelligent batch processing benchmarks
pytest tests/performance/test_performance.py -k "intelligent_batch" -v
```

## 🔒 Security Guidelines

### Secrets Management
- **Never commit** API keys, tokens, or passwords
- **Use `.env` files** for local development
- **Environment variables** for production
- **Rotate credentials** regularly

### Code Security
```bash
# Security scanning
bandit -r core/

# Dependency vulnerability check
safety check

# Check for secrets in commits
git-secrets --scan
```

## 📚 Resources

### Documentation
- [Installation Guide](guides/installation.md)
- [Configuration Guide](guides/configuration.md)
- [LLM Integration](llm/integration.md)
- [Notion Integration](notion.md)

### External Resources
- [Python PEP 8](https://www.python.org/dev/peps/pep-0008/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Black Code Formatter](https://black.readthedocs.io/)
- [Ollama Documentation](https://ollama.com/docs)

## 🎯 Contributing

### Getting Started
1. **Read this guide** thoroughly
2. **Set up development environment**
3. **Run tests** to ensure everything works
4. **Pick an issue** from GitHub Issues
5. **Create feature branch**
6. **Implement with tests**
7. **Submit pull request**

### Code Review Checklist
- [ ] Tests pass (`pytest`)
- [ ] Code formatted (`black .`)
- [ ] Linting passes (`flake8`)
- [ ] Documentation updated
- [ ] Type hints added
- [ ] Security considerations addressed
- [ ] Performance impact considered 
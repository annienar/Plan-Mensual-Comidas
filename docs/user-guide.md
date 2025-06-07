# User Guide

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- Git
- **Ollama** (for local LLM deployment)
- Notion account (optional, for cloud sync)

### Installation

#### 1. Install Ollama
```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.com/install.sh | sh

# Windows: Download from ollama.com
```

#### 2. Install Commercial-Licensed Models
```bash
# Primary text processing model (MIT license)
ollama pull phi

# Multimodal processing model (MIT license) 
ollama pull llava-phi3

# Optional backup multimodal model (Apache 2.0)
ollama pull moondream
```

#### 3. Clone and Setup Project
```bash
# Clone repository
git clone https://github.com/yourusername/plan-mensual-comidas.git
cd plan-mensual-comidas

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### 4. Verify Installation
```bash
# Run tests to verify everything works
pytest

# Check CLI is working
python -m core.cli --help
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# LLM Configuration
OLLAMA_HOST=localhost:11434
LLM_TEXT_MODEL=phi
LLM_MULTIMODAL_MODEL=llava-phi3
LLM_TEMPERATURE=0.1
LLM_MAX_RETRIES=3

# Commercial Compliance
COMMERCIAL_MODE=true
APPROVED_MODELS=phi,llava-phi3,moondream

# Notion Integration (Optional)
NOTION_TOKEN=your_notion_integration_token
NOTION_RECETAS_DB=your_recipes_database_id
NOTION_INGREDIENTES_DB=your_ingredients_database_id
NOTION_ALACENA_DB=your_pantry_database_id

# Optional Settings
LOG_LEVEL=INFO
CACHE_ENABLED=true
CACHE_TTL=3600
```

### Notion Setup (Optional)

If you want cloud sync with Notion:

#### 1. Create Notion Integration
1. Go to https://www.notion.so/my-integrations
2. Click "New integration"
3. Name it "Monthly Meal Plan"
4. Select your workspace
5. Copy the integration token

#### 2. Create Databases
Create three databases in Notion:
- **Recetas** (Recipes)
- **Ingredientes** (Ingredients)  
- **Alacena** (Pantry)

#### 3. Share Databases
1. For each database, click "Share"
2. Add your integration by name
3. Grant "Edit" permissions

#### 4. Get Database IDs
1. Open each database in Notion
2. Copy the database ID from the URL (32-character string)
3. Add to your `.env` file

### Configuration Files

The system uses these configuration files:

- **`.env`**: Environment variables and secrets
- **`config/`**: Application configuration (auto-generated)
- **`logs/`**: Application logs (auto-generated)

## 📖 Usage

### Basic Recipe Processing

#### Process Text Recipe
```bash
# From text file
python -m core.cli process_recipe "path/to/recipe.txt"

# From direct text input
python -m core.cli process_recipe --text "Recipe content here..."
```

#### Process Image Recipe
```bash
# Process recipe from image (requires LLaVA-Phi3)
python -m core.cli process_recipe "path/to/recipe_image.jpg"
```

#### Process PDF Recipe
```bash
# Process recipe from PDF (requires LLaVA-Phi3)
python -m core.cli process_recipe "path/to/recipe.pdf"
```

### Pantry Management

#### Check Pantry Status
```bash
# Check what's available for a recipe
python -m core.cli check_pantry "Arroz con Pollo"

# List all pantry items
python -m core.cli list_pantry
```

#### Update Pantry
```bash
# Add item to pantry
python -m core.cli add_pantry "arroz" 500 "gramos"

# Update existing item
python -m core.cli update_pantry "arroz" 300 "gramos"
```

### Shopping Lists

#### Generate Shopping List
```bash
# Generate list for specific recipe
python -m core.cli shopping_list "Arroz con Pollo"

# Generate list for multiple recipes
python -m core.cli shopping_list "recipe1.txt" "recipe2.txt"
```

#### Manage Shopping Lists
```bash
# View current shopping list
python -m core.cli view_shopping_list

# Mark items as purchased
python -m core.cli mark_purchased "arroz" "pollo"
```

### System Management

#### Check System Status
```bash
# Overall system health
python -m core.cli status

# Check LLM connectivity
python -m core.cli test_llm

# Check Notion connectivity (if configured)
python -m core.cli test_notion
```

#### Sync with Notion
```bash
# Manual sync all data
python -m core.cli sync_all

# Sync specific recipe
python -m core.cli sync_recipe "Arroz con Pollo"
```

## 🔧 Troubleshooting

### Installation Issues

**"Ollama not found"**
```bash
# Check if Ollama is installed
ollama --version

# If not installed, install it:
# macOS: brew install ollama
# Linux: curl -fsSL https://ollama.com/install.sh | sh
# Windows: Download from ollama.com
```

**"pip install fails"**
```bash
# Check Python version (must be 3.9+)
python --version

# Ensure virtual environment is activated
source .venv/bin/activate

# Try reinstalling dependencies
pip install -r requirements.txt --force-reinstall
```

**"Tests failing"**
```bash
# Check if you're in the right directory
pwd  # Should end with "plan-mensual-comidas"

# Ensure virtual environment is active
which python  # Should point to .venv/bin/python

# Run specific test to debug
pytest tests/recipe/test_models.py -v
```

### LLM Issues

**"Model not found"**
```bash
# Check available models
ollama list

# Pull required models
ollama pull phi
ollama pull llava-phi3
```

**"LLM connection failed"**
```bash
# Check if Ollama is running
ollama ps

# Start Ollama if not running
ollama serve

# Test connection
curl http://localhost:11434/api/tags
```

**"Processing too slow"**
```bash
# Check system resources
top  # Look for high CPU/memory usage

# Try smaller model if needed
export LLM_TEXT_MODEL=phi:mini
```

### Notion Integration Issues

**"401 Unauthorized"**
- Check your `NOTION_TOKEN` in `.env` file
- Verify token is valid at https://www.notion.so/my-integrations
- Ensure integration has access to databases

**"Database not found"**
- Verify database IDs in `.env` file
- Check database sharing permissions
- Ensure integration is added to workspace

**"Sync failures"**
```bash
# Check Notion connectivity
python -m core.cli test_notion

# View detailed error logs
tail -f logs/application.log

# Force resync
python -m core.cli force_sync
```

### Performance Issues

**"Processing too slow"**
- Check available system memory (LLM models need 2-4GB RAM)
- Close other applications to free memory
- Consider using smaller models for testing

**"High disk usage"**
- Clean up logs: `python -m core.cli cleanup_logs`
- Clear cache: `python -m core.cli clear_cache`
- Remove old processed files

### Common CLI Issues

**"Command not found"**
```bash
# Always run from project root
cd /path/to/plan-mensual-comidas

# Use full module path
python -m core.cli --help

# Ensure virtual environment is active
source .venv/bin/activate
```

**"Permission denied"**
```bash
# Check file permissions
ls -la

# Fix permissions if needed
chmod +x scripts/*.py
```

**"Import errors"**
```bash
# Ensure you're in virtual environment
source .venv/bin/activate

# Install in development mode
pip install -e .

# Check Python path
python -c "import sys; print(sys.path)"
```

## 📊 Performance Tips

### Optimization Settings
```bash
# Enable caching for faster processing
export CACHE_ENABLED=true

# Adjust LLM temperature for consistency
export LLM_TEMPERATURE=0.1

# Increase timeout for large files
export LLM_TIMEOUT=60
```

### Resource Management
- **Memory**: LLM models need 2-4GB RAM
- **Storage**: Keep 5GB free for model downloads and cache
- **CPU**: Multi-core systems process recipes faster

### Batch Processing
```bash
# Process multiple recipes efficiently
python -m core.cli batch_process "recipes/sin_procesar/*.txt"

# Use parallel processing for large batches
python -m core.cli batch_process --parallel "recipes/sin_procesar/*.txt"
```

## 🔒 Security & Privacy

### Data Protection
- **Local Processing**: All LLM processing happens locally
- **No Data Sharing**: Models don't send data to external servers
- **Secure Storage**: Credentials stored in `.env` file (not committed to git)

### Best Practices
- Keep `.env` file secure and never commit it
- Regularly update Notion integration tokens
- Use strong passwords for Notion account
- Review database permissions periodically

## 📚 Additional Resources

### Documentation
- [Development Guide](development.md) - For contributors
- [Directory Structure](directory-structure.md) - Project organization
- [LLM Integration](llm/integration.md) - Technical details
- [Notion Integration](notion.md) - Database setup
- [Project Roadmap](project-roadmap.md) - Future plans

### External Resources
- [Ollama Documentation](https://ollama.com/docs)
- [Notion API Documentation](https://developers.notion.com/)
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)

### Getting Help
- **GitHub Issues**: Report bugs or request features
- **Documentation**: Check other files in `docs/` directory
- **Community**: Join discussions in GitHub Discussions

## 🎯 Quick Reference

### Essential Commands
```bash
# Setup
ollama pull phi && ollama pull llava-phi3
python -m core.cli status

# Daily Usage
python -m core.cli process_recipe "recipe.txt"
python -m core.cli check_pantry "Recipe Name"
python -m core.cli shopping_list "Recipe Name"

# Maintenance
python -m core.cli sync_all
python -m core.cli cleanup_logs
```

### File Locations
- **Raw Recipes**: `recipes/sin_procesar/`
- **Processed Recipes**: `recipes/procesadas/`
- **Final Recipes (JSON)**: `recipes/json/`
- **Error Recipes**: `recipes/errores/`
- **Logs**: `logs/`
- **Config**: `.env` and `config/`
- **Cache**: `.cache/` (auto-generated)

### Support Checklist
Before asking for help:
- [ ] Virtual environment activated
- [ ] All models downloaded (`ollama list`)
- [ ] Tests passing (`pytest`)
- [ ] `.env` file configured
- [ ] Logs checked (`tail logs/application.log`) 
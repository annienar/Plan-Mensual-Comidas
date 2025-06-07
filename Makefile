# Variables
PYTHON = .venv/bin/python
PIP = .venv/bin/pip
VENV = .venv

# Default target
.PHONY: help
help:
	@echo "Available commands:"
	@echo "  make install    - Install dependencies"
	@echo "  make develop    - Install package in development mode"
	@echo "  make test       - Run all tests"
	@echo "  make test-phi   - Run phi model test"
	@echo "  make test-llm   - Run LLM integration tests"
	@echo "  make test-e2e   - Run end-to-end tests"
	@echo "  make clean      - Remove virtual environment"
	@echo "  make venv       - Create virtual environment"

# Create virtual environment
.PHONY: venv
venv:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip

# Install dependencies
.PHONY: install
install: venv
	$(PIP) install -r requirements.txt

# Install package in development mode
.PHONY: develop
develop: install
	$(PIP) install -e .

# Run all tests
.PHONY: test
test: develop test-phi test-llm test-e2e

# Run phi model test
.PHONY: test-phi
test-phi: develop
	$(PYTHON) -m pytest tests/recipe/test_phi.py -v

# Run LLM integration tests
.PHONY: test-llm
test-llm: develop
	$(PYTHON) -m pytest tests/recipe/test_real_integration.py -v

# Run end-to-end tests
.PHONY: test-e2e
test-e2e: develop
	$(PYTHON) -m pytest tests/recipe/test_e2e.py -v

# Clean up
.PHONY: clean
clean:
	rm -rf $(VENV)
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.egg" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type d -name "dist" -exec rm -rf {} +
	find . -type d -name "build" -exec rm -rf {} +
	echo "Cleanup complete!"

clean-logs:
	@echo "Cleaning up old logs..."
	@./scripts/cleanup_logs.sh 
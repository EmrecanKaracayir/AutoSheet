.PHONY: init install install-dev clean format lint test run

# Constants
VENV = .venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

# Initialize the virtual environment
init:
	@echo "Initializing virtual environment..."
	python3 -m venv $(VENV)

# Install production dependencies
install:
	@echo "Installing production dependencies..."
	$(PIP) install .

# Install development dependencies
install-dev:
	@echo "Installing development dependencies..."
	$(PIP) install .[dev]

# Clean the project
clean:
	@echo "Cleaning the project..."
	rm -rf build
	rm -rf .pytest_cache
	find . -type d -name '*.egg-info' -exec rm -rf {} +
	find . -type d -name '__pycache__' -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete

# Clean the data folder
clean-data:
	@echo "Cleaning the data folder..."
	find data -type f -delete
	find data -type l -delete

# Format the code
format:
	@echo "Formatting the code..."
	$(VENV)/bin/black source tests

# Lint the code
lint:
	@echo "Linting the code..."
	$(VENV)/bin/flake8 source tests

# Run the tests
test:
	@echo "Running the tests..."
	$(VENV)/bin/pytest

# Run the application
run:
	@echo "Running the application..."
	$(PYTHON) source/autosheet/main.py

.PHONY: init install install-dev clean format lint test run run-dev package

# Constants
VENV_NAME = .venv

ifeq ($(OS),Windows_NT)
	PYTHON_INTERPRETER = python
	VENV = $(VENV_NAME)/Scripts
	PYTHON = $(VENV)/python.exe
	PIP = $(VENV)/pip.exe
	SEP = ;
else
	PYTHON_INTERPRETER := $(shell command -v python3 > /dev/null 2>&1 && echo python3 || echo python)
	VENV = $(VENV_NAME)/bin
	PYTHON = $(VENV)/python
	PIP = $(VENV)/pip
	SEP = :
endif

# Initialize the virtual environment
init:
	@echo "Initializing virtual environment..."
	$(PYTHON_INTERPRETER) -m venv $(VENV_NAME)


# Install production dependencies
install:
	@echo "Installing production dependencies..."
	$(PIP) install .


# Install development dependencies
install-dev:
	@echo "Installing development dependencies..."
	$(PIP) install -e .[dev]


# Clean the project
clean:
	@echo "Cleaning the project..."
	$(PYTHON) scripts/clean.py


# Clean the cache folder
clean-cache:
	@echo "Cleaning the cache folder..."
	$(PYTHON) scripts/clean_cache.py


# Format the code
format:
	@echo "Formatting the code..."
	$(PYTHON) -m black source tests


# Lint the code
lint:
	@echo "Linting the code..."
	$(PYTHON) -m flake8 source tests --max-line-length=100


# Run the tests
test:
	@echo "Running the tests..."
	$(PYTHON) -m pytest


# Run the application
run:
	@echo "Running the application..."
	$(PYTHON) source/autosheet/main.py


# Run the application in debug mode
run-dev:
	@echo "Running the application..."
	$(PYTHON) source/autosheet/main.py --debug


# Package the application
package:
	@echo "Packaging the application..."
	$(PYTHON) scripts/clean_package.py
	pyinstaller source/autosheet/main.py --distpath ./package/dist --workpath ./package/build --clean --onedir --specpath ./package --name AutoSheet --add-data ../resources/${SEP}resources --add-data ../data${SEP}data --windowed --icon ../resources/icon.icns

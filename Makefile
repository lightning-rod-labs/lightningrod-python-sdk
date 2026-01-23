.PHONY: help setup install install-dev test build clean generate publish upload

help:
	@echo "Lightning Rod Python SDK - Development Commands"
	@echo ""
	@echo "  make setup       - Create virtual environment and install package"
	@echo "  make install     - Install package in editable mode"
	@echo "  make install-dev - Install package with development dependencies"
	@echo "  make test        - Run tests"
	@echo "  make build       - Build distribution packages"
	@echo "  make publish     - Build and upload to PyPI"
	@echo "  make upload      - Upload distribution packages to PyPI (requires build first)"
	@echo "  make clean       - Clean build artifacts"
	@echo "  make generate    - Regenerate client from OpenAPI spec"
	@echo ""

setup:
	@bash setup.sh

install:
	@echo "Installing lightningrod-ai in editable mode..."
	@pip install -e .

install-dev:
	@echo "Installing lightningrod-ai with development dependencies..."
	@pip install -e ".[dev]"

test:
	@echo "Running tests..."
	@python -m pytest tests/ -v

build:
	@echo "Building distribution packages..."
	@python -m build

publish: build upload

upload:
	@echo "Uploading to PyPI..."
	@twine upload --repository lightningrod-ai dist/*

clean:
	@echo "Cleaning build artifacts..."
	@rm -rf build/
	@rm -rf dist/
	@rm -rf *.egg-info
	@find . -type d -name __pycache__ -exec rm -r {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete

generate:
	@echo "Generating Python SDK client library..."
	@python ./scripts/generate.py

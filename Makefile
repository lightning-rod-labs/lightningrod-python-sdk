.PHONY: help setup install install-dev test build clean generate publish upload bump-version bump-patch bump-minor bump-major

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
	@echo "  make bump-patch   - Bump patch version (0.1.5 -> 0.1.6)"
	@echo "  make bump-minor   - Bump minor version (0.1.5 -> 0.2.0)"
	@echo "  make bump-major   - Bump major version (0.1.5 -> 1.0.0)"
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

publish-new-version: 
	@rm -rf dist/*
	@make build
	@make upload

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

bump-version:
	@if [ -z "$(TYPE)" ]; then \
		echo "Usage: make bump-version TYPE=patch|minor|major"; \
		exit 1; \
	fi
	@CURRENT_VERSION=$$(grep '^version = ' pyproject.toml | sed 's/version = "\(.*\)"/\1/'); \
	IFS='.' read -r MAJOR MINOR PATCH <<< "$$CURRENT_VERSION"; \
	case "$(TYPE)" in \
		patch) \
			PATCH=$$((PATCH + 1)) \
			;; \
		minor) \
			MINOR=$$((MINOR + 1)); \
			PATCH=0 \
			;; \
		major) \
			MAJOR=$$((MAJOR + 1)); \
			MINOR=0; \
			PATCH=0 \
			;; \
		*) \
			echo "Invalid TYPE. Use patch, minor, or major"; \
			exit 1 \
			;; \
	esac; \
	NEW_VERSION="$$MAJOR.$$MINOR.$$PATCH"; \
	echo "Bumping version from $$CURRENT_VERSION to $$NEW_VERSION"; \
	sed -i '' 's/^version = ".*"/version = "'"$$NEW_VERSION"'"/' pyproject.toml; \
	sed -i '' -E 's/badge\/beta-[0-9]+\.[0-9]+\.[0-9]+/badge\/beta-'"$$NEW_VERSION"'/g' README.md; \
	sed -i '' -E 's/pypi\.org\/project\/lightningrod-ai\/[0-9]+\.[0-9]+\.[0-9]+/pypi.org\/project\/lightningrod-ai\/'"$$NEW_VERSION"'/g' README.md; \
	sed -i '' 's/^__version__ = ".*"/__version__ = "'"$$NEW_VERSION"'"/' src/lightningrod/__init__.py; \
	echo "Version bumped to $$NEW_VERSION"

bump-patch:
	@$(MAKE) bump-version TYPE=patch

bump-minor:
	@$(MAKE) bump-version TYPE=minor

bump-major:
	@$(MAKE) bump-version TYPE=major

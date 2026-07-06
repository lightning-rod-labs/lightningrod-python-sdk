.PHONY: help setup install install-dev test pytest build clean publish upload bump-version bump-patch bump-minor bump-major release

help:
	@echo "Lightning Rod Python SDK - Development Commands"
	@echo ""
	@echo "  make setup       - Create virtual environment and install package"
	@echo "  make install     - Install package in editable mode"
	@echo "  make install-dev - Install package with development dependencies"
	@echo "  make test        - Run tests (pytest)"
	@echo "  make pytest      - Same as make test"
	@echo "  make build       - Build distribution packages"
	@echo "  make publish     - Build and upload to PyPI"
	@echo "  make upload      - Upload distribution packages to PyPI (requires build first)"
	@echo "  make clean       - Clean build artifacts"
	@echo "  make bump-patch   - Bump patch version (0.1.5 -> 0.1.6)"
	@echo "  make bump-minor   - Bump minor version (0.1.5 -> 0.2.0)"
	@echo "  make bump-major   - Bump major version (0.1.5 -> 1.0.0)"
	@echo "  make bump-version VERSION=X.Y.Z - Set an explicit version"
	@echo "  make release TYPE=minor|major|X.Y.Z - Bump, commit, and tag"
	@echo ""

setup:
	@echo "Creating virtual environment and installing package..."
	@python3 -m venv venv
	@. venv/bin/activate && pip install -e .

install:
	@echo "Installing lightningrod-ai in editable mode..."
	@pip install -e .

install-dev:
	@echo "Installing lightningrod-ai with development dependencies..."
	@pip install -e ".[dev]"

test pytest:
	@echo "Running tests..."
	@python -m pytest tests/ -v

build:
	@echo "Building distribution packages..."
	@rm -rf build/
	@python -m build

publish-new-version: 
	@rm -rf dist/*
	@python -m pip install build twine
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

# Bump version across pyproject.toml, __init__.py, and README.
# Accepts a bump type via TYPE= (patch|minor|major) or an explicit VERSION=X.Y.Z.
bump-version:
	@if [ -n "$(VERSION)" ]; then \
		python3 scripts/bump_version.py "$(VERSION)"; \
	elif [ -n "$(TYPE)" ]; then \
		python3 scripts/bump_version.py "$(TYPE)"; \
	else \
		echo "Usage: make bump-version TYPE=patch|minor|major | VERSION=X.Y.Z"; \
		exit 1; \
	fi

bump-patch:
	@python3 scripts/bump_version.py patch

bump-minor:
	@python3 scripts/bump_version.py minor

bump-major:
	@python3 scripts/bump_version.py major

# Bump, commit, and tag in one step. TYPE= accepts patch|minor|major or X.Y.Z.
release:
	@if [ -z "$(TYPE)" ]; then \
		echo "Usage: make release TYPE=patch|minor|major|X.Y.Z [PUSH=1]"; \
		exit 1; \
	fi
	@python3 scripts/bump_version.py "$(TYPE)" --tag $(if $(PUSH),--push,)

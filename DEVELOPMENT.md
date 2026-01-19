# Development Setup

This guide explains how to set up a development environment for the Lightning Rod Python SDK.

## Prerequisites

- Python 3.10 or higher
- `pip` (Python package installer)

## Quick Start

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install package in editable mode
pip install -e .

# Install development dependencies (optional)
pip install -e ".[dev]"
```

## Development Commands

- `make setup` - Create virtual environment and install package
- `make install` - Install package in editable mode
- `make install-dev` - Install package with development dependencies
- `make test` - Run tests
- `make build` - Build distribution packages (for PyPI)
- `make clean` - Clean build artifacts
- `make generate` - Regenerate client from OpenAPI spec

## Package Installation

Once installed (either via `pip install -e .` or `make install`), the package can be imported:

```python
from lightningrod import LightningRodClient
```

## Building for Distribution

To build the package for distribution to PyPI:

```bash
# Install build tools
pip install build twine

# Build distribution packages
make build

# Upload to PyPI (requires credentials)
python -m twine upload dist/*
```

## Testing Installation

After installation, verify the package works:

```python
python -c "from lightningrod import LightningRodClient; print('Installation successful!')"
```

## Virtual Environment

The virtual environment is created in the `venv/` directory (which is gitignored). To activate it:

```bash
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

To deactivate:

```bash
deactivate
```


## Releasing a New Version

1. Increment the version number in `pyproject.toml` and `src/lightningrod/__init__.py`
2. Build and upload:

```bash
pip install build twine
make build
python -m twine upload dist/*
```
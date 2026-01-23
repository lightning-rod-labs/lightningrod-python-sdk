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
from lightningrod import LightningRod
```

## Building for Distribution

To build and publish the package to PyPI:

```bash
# Install build tools
pip install build twine

# Build and upload to PyPI (unified command)
make publish

# Or build and upload separately:
make build
make upload
```

### PyPI Setup

Before uploading, you need to configure PyPI credentials in `~/.pypirc`:

```ini
[distutils]
  index-servers =
    lightningrod-ai

[lightningrod-ai]
  repository = https://upload.pypi.org/legacy/
  username = __token__
  password = <your-pypi-api-token>
```

To get a PyPI API token:
1. Create an account at https://pypi.org/account/register/ (if needed)
2. Generate an API token at https://pypi.org/manage/account/token/
3. Use a project-scoped token for `lightningrod-ai`
4. Replace `<your-pypi-api-token>` in `.pypirc` with your actual token

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

1. Increment the version number in `pyproject.toml` and `src/lightningrod/__init__.py` (keep them in sync)
2. Build and upload:

```bash
pip install build twine
make publish
```

**Note:** Make sure your `~/.pypirc` is configured correctly (see "PyPI Setup" above). The repository URL must point to `https://upload.pypi.org/legacy/`, not a GitHub repository URL.
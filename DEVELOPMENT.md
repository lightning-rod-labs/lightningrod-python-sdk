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
- `make bump-patch` - Bump patch version (e.g. 0.1.5 -> 0.1.6)
- `make bump-minor` - Bump minor version (e.g. 0.1.5 -> 0.2.0)
- `make bump-major` - Bump major version (e.g. 0.1.5 -> 1.0.0)
- `make publish-new-version` - Build and upload new version to PyPI (cleans dist first)

## Package Installation

Once installed (either via `pip install -e .` or `make install`), the package can be imported:

```python
from lightningrod import LightningRod
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

## Releasing a New Version

1. Bump the version using one of the version commands:
   - `make bump-patch` - For patch releases (bug fixes)
   - `make bump-minor` - For minor releases (new features)
   - `make bump-major` - For major releases (breaking changes)
   
   This automatically updates the version in `pyproject.toml`, `src/lightningrod/__init__.py`, and `README.md`.

2. Build and upload:

```bash
make publish-new-version
```

**Note:** Make sure your `~/.pypirc` is configured correctly (see "PyPI Setup" above). The repository URL must point to `https://upload.pypi.org/legacy/`, not a GitHub repository URL.
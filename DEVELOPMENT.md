# Development Setup

## Prerequisites

- Python 3.10+
- `pip`

## Quick Start

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install package in editable mode
pip install -e .

# Install with dev dependencies (optional)
pip install -e ".[dev]"
```

## Development Commands

- `make setup` - Create virtual environment and install package
- `make install` - Install package in editable mode
- `make install-dev` - Install with development dependencies
- `make test` - Run tests
- `make build` - Build distribution packages
- `make clean` - Clean build artifacts
- `make bump-patch` - Bump patch version (e.g. 0.1.5 -> 0.1.6)
- `make bump-minor` - Bump minor version (e.g. 0.1.5 -> 0.2.0)
- `make bump-major` - Bump major version (e.g. 0.1.5 -> 1.0.0)
- `make publish-new-version` - Build and upload new version to PyPI

## Releasing a New Version

1. Bump the version:
   ```bash
   make bump-patch   # bug fixes
   make bump-minor   # new features
   make bump-major   # breaking changes
   ```
   This updates the version in `pyproject.toml`, `src/lightningrod/__init__.py`, and `README.md`.

2. Build and publish:
   ```bash
   make publish-new-version
   ```

### PyPI Setup

Configure credentials in `~/.pypirc`:

```ini
[distutils]
  index-servers =
    lightningrod-ai

[lightningrod-ai]
  repository = https://upload.pypi.org/legacy/
  username = __token__
  password = <your-pypi-api-token>
```

Get a token at https://pypi.org/manage/account/token/ (use a project-scoped token for `lightningrod-ai`).

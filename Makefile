.PHONY: help setup install install-dev test pytest build clean generate filter-openapi publish upload bump-version bump-patch bump-minor bump-major eval-build eval eval-all autoagent eval-plot improve-assistant-agent

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
	@echo "  make generate       - Regenerate client from OpenAPI spec"
	@echo "  make filter-openapi - Fetch and filter OpenAPI spec for docs"
	@echo "  make bump-patch   - Bump patch version (0.1.5 -> 0.1.6)"
	@echo "  make bump-minor   - Bump minor version (0.1.5 -> 0.2.0)"
	@echo "  make bump-major   - Bump major version (0.1.5 -> 1.0.0)"
	@echo "  make eval-build   - Build the shared Docker image for evals"
	@echo "  make eval TASK=x  - Run a single Harbor agent eval (e.g. TASK=bias-survivorship-news)"
	@echo "  make eval-all     - Run all Harbor agent evals"
	@echo "  make autoagent    - Start the AutoAgent meta-agent optimization loop"
	@echo "  make eval-plot    - Plot AutoAgent optimization progress chart"
	@echo "  make improve-assistant-agent SESSION=x PROBLEM='desc' - Create eval + fix from a testing session"
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

filter-openapi:
	@python ./scripts/filter_openapi.py

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

# ---------------------------------------------------------------------------
# Agent evals (Harbor)
#
# Requires: harbor (`uv tool install harbor`), Docker, ANTHROPIC_API_KEY
#
#   make eval TASK=bias-survivorship-news   Run a single eval task
#   make eval-all                           Run all eval tasks
#   make autoagent                          Start AutoAgent self-improvement loop
# ---------------------------------------------------------------------------

HARBOR_IMAGE := lightningrod-evals
HARBOR_AGENT := evals.agent:LightningrodAssistantAgent
HARBOR_MOUNTS := ["/Users/bart/Projects/lightningrod-python-sdk:/workspace/lightningrod-python-sdk:ro"]
HARBOR_ENV_FILE := /tmp/harbor-eval.env

# Build the shared Docker image used by all eval tasks.
# Run this once, or after changing evals/Dockerfile.
eval-build:
	docker build -t $(HARBOR_IMAGE) -f evals/Dockerfile .

eval:
	@if [ -z "$$ANTHROPIC_API_KEY" ]; then \
		echo "Error: ANTHROPIC_API_KEY is not set"; \
		exit 1; \
	fi
	@if [ -z "$(TASK)" ]; then \
		echo "Usage: make eval TASK=bias-survivorship-news"; \
		echo ""; \
		echo "Available tasks:"; \
		ls -1 evals/tasks/ | grep -v -E '(shared|catalog|Dockerfile)'; \
		exit 1; \
	fi
	@echo "ANTHROPIC_API_KEY=$${ANTHROPIC_API_KEY}" > $(HARBOR_ENV_FILE)
	harbor run -p evals/tasks/$(TASK) \
		--agent-import-path $(HARBOR_AGENT) \
		--mounts-json '$(HARBOR_MOUNTS)' \
		--env-file $(HARBOR_ENV_FILE) \
		-y

eval-all:
	@if [ -z "$$ANTHROPIC_API_KEY" ]; then \
		echo "Error: ANTHROPIC_API_KEY is not set"; \
		exit 1; \
	fi
	@echo "ANTHROPIC_API_KEY=$${ANTHROPIC_API_KEY}" > $(HARBOR_ENV_FILE)
	harbor run -p evals/tasks/ \
		--agent-import-path $(HARBOR_AGENT) \
		--mounts-json '$(HARBOR_MOUNTS)' \
		--env-file $(HARBOR_ENV_FILE) \
		-y

# Start the AutoAgent meta-agent optimization loop.
# A coding agent (Claude Code) reads evals/program.md, runs the Harbor
# eval suite, diagnoses low-scoring tasks, edits the agent prompt files,
# re-runs evals, and keeps changes that improve the total score.
autoagent:
	claude --dangerously-skip-permissions --agent lightningrod-assistant "Read evals/program.md and kick off a new experiment."

# Improve the assistant agent from a user testing session.
# Extracts the session transcript, creates an eval task, fixes the prompt,
# and runs the full regression suite.
improve-assistant-agent:
	@if [ -z "$$ANTHROPIC_API_KEY" ]; then \
		echo "Error: ANTHROPIC_API_KEY is not set"; \
		exit 1; \
	fi
	@if [ -z "$(PROBLEM)" ]; then \
		echo "Usage: make improve-assistant-agent [SESSION=<session-id>] PROBLEM='description of the issue'"; \
		echo ""; \
		echo "Recent sessions:"; \
		python scripts/extract_session.py 2>&1 | head -20; \
		exit 1; \
	fi
	claude --dangerously-skip-permissions "/improve-assistant-agent $(if $(SESSION),$(SESSION) ,)$(PROBLEM)"

improve-assistant-agent-plan:
	@if [ -z "$$ANTHROPIC_API_KEY" ]; then \
		echo "Error: ANTHROPIC_API_KEY is not set"; \
		exit 1; \
	fi
	@if [ -z "$(PROBLEM)" ]; then \
		echo "Usage: make improve-assistant-agent-plan [SESSION=<session-id>] PROBLEM='description of the issue'"; \
		echo ""; \
		echo "Recent sessions:"; \
		python scripts/extract_session.py 2>&1 | head -20; \
		exit 1; \
	fi
	claude --permission-mode plan "/improve-assistant-agent $(if $(SESSION),$(SESSION) ,)$(PROBLEM)"

# Plot optimization progress from evals/results.tsv.
# Use -o to save: make eval-plot PLOT_OUT=progress.png
eval-plot:
	python evals/plot_progress.py $(if $(PLOT_OUT),-o $(PLOT_OUT),)

bump-patch:
	@$(MAKE) bump-version TYPE=patch

bump-minor:
	@$(MAKE) bump-version TYPE=minor

bump-major:
	@$(MAKE) bump-version TYPE=major

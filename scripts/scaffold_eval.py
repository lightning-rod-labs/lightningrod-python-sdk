#!/usr/bin/env python3
"""Scaffold the boilerplate files for a new eval task.

Creates the mechanical files that are identical across all tasks.
The caller still needs to write instruction.md and tests/test.py content.

Usage:
    python scripts/scaffold_eval.py --task-name bias-example --description "Test description"
"""

import argparse
import os
import sys
from pathlib import Path

EVALS_DIR = Path(__file__).resolve().parent.parent / "evals" / "tasks"

DOCKERFILE = """\
# Harbor evaluation environment for lightningrod-assistant evals.
#
# The agent runs on the HOST via claude CLI (uses local OAuth).
# This container only runs the LLM-as-judge verifier.

FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \\
    && rm -rf /var/lib/apt/lists/*

# Python deps for the LLM judge verifier
RUN pip install --no-cache-dir anthropic

RUN mkdir -p /logs/agent /logs/verifier
"""

TEST_SH = """\
#!/bin/bash
set -e
cd "$(dirname "$0")"
python3 test.py /logs/agent/response.txt
"""

TEST_PY_SKELETON = '''\
"""
Verifier: {description}
"""

import sys
sys.path.insert(0, "/workspace/lightningrod-python-sdk/evals")

from judge import Criterion, run_judge_from_file

SCENARIO = """\\
TODO: Describe the scenario and what the agent should or should not do.
"""

CRITERIA = [
    Criterion(
        description=(
            "TODO: Primary criterion"
        ),
        weight=0.4,
    ),
    Criterion(
        description=(
            "TODO: Secondary criterion"
        ),
        weight=0.3,
    ),
    Criterion(
        description=(
            "TODO: Tertiary criterion"
        ),
        weight=0.2,
    ),
    Criterion(
        description=(
            "TODO: Actionability / path forward"
        ),
        weight=0.1,
    ),
]

if __name__ == "__main__":
    run_judge_from_file(sys.argv[1], SCENARIO, CRITERIA)
'''


def task_toml(task_name: str, description: str, keywords: list[str]) -> str:
    kw_str = ", ".join(f'"{k}"' for k in keywords)
    return f"""\
[task]
name = "lightningrod-evals/{task_name}"
description = "{description}"
keywords = [{kw_str}]

[agent]
timeout_sec = 300

[verifier]
timeout_sec = 120

[environment]
allow_internet = true
memory_mb = 4096

[environment.env]
ANTHROPIC_API_KEY = "${{ANTHROPIC_API_KEY:-notset}}"
"""


def main():
    parser = argparse.ArgumentParser(description="Scaffold a new eval task.")
    parser.add_argument("--task-name", required=True, help="Task slug (e.g. bias-example)")
    parser.add_argument("--description", required=True, help="One-line task description")
    parser.add_argument(
        "--keywords",
        default="reasoning",
        help="Comma-separated keywords (default: reasoning)",
    )
    args = parser.parse_args()

    task_dir = EVALS_DIR / args.task_name
    if task_dir.exists():
        print(f"Task directory already exists: {task_dir}", file=sys.stderr)
        sys.exit(1)

    keywords = [k.strip() for k in args.keywords.split(",")]

    # Create directory structure
    (task_dir / "environment").mkdir(parents=True)
    (task_dir / "tests").mkdir(parents=True)

    # Write files
    (task_dir / "environment" / "Dockerfile").write_text(DOCKERFILE)
    (task_dir / "task.toml").write_text(task_toml(args.task_name, args.description, keywords))
    (task_dir / "tests" / "test.sh").write_text(TEST_SH)
    os.chmod(task_dir / "tests" / "test.sh", 0o755)
    (task_dir / "tests" / "test.py").write_text(TEST_PY_SKELETON.format(description=args.description))
    (task_dir / "instruction.md").write_text("")

    print(f"Scaffolded eval task: {task_dir}")
    print(f"  Files created:")
    for f in sorted(task_dir.rglob("*")):
        if f.is_file():
            print(f"    {f.relative_to(EVALS_DIR.parent.parent)}")
    print(f"\n  Next: write instruction.md and tests/test.py")


if __name__ == "__main__":
    main()

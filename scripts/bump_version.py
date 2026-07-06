#!/usr/bin/env python3
"""Bump the SDK version consistently across all files.

Keeps ``pyproject.toml``, ``src/lightningrod/__init__.py`` and the README
badges/links in sync so the package version and the git tag never drift.

Usage:
    python scripts/bump_version.py patch|minor|major
    python scripts/bump_version.py 1.1.0            # set an explicit version
    python scripts/bump_version.py minor --commit --tag

Options:
    --commit    git add the changed files and commit them
    --tag       create an annotated ``vX.Y.Z`` git tag (implies --commit)
    --push      push the commit and tag to origin (implies --tag)
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PYPROJECT = ROOT / "pyproject.toml"
INIT = ROOT / "src" / "lightningrod" / "__init__.py"
README = ROOT / "README.md"

VERSION_RE = re.compile(r"^\d+\.\d+\.\d+$")


def read_current_version() -> str:
    text = PYPROJECT.read_text()
    match = re.search(r'^version = "(\d+\.\d+\.\d+)"', text, re.MULTILINE)
    if not match:
        sys.exit("Could not find a version in pyproject.toml")
    return match.group(1)


def compute_new_version(current: str, spec: str) -> str:
    if VERSION_RE.match(spec):
        return spec
    major, minor, patch = (int(p) for p in current.split("."))
    if spec == "patch":
        patch += 1
    elif spec == "minor":
        minor += 1
        patch = 0
    elif spec == "major":
        major += 1
        minor = patch = 0
    else:
        sys.exit(f"Invalid bump spec {spec!r}; use patch|minor|major or X.Y.Z")
    return f"{major}.{minor}.{patch}"


def replace_in_file(path: Path, replacements: list[tuple[str, str]]) -> bool:
    text = path.read_text()
    new_text = text
    for pattern, replacement in replacements:
        new_text = re.sub(pattern, replacement, new_text, flags=re.MULTILINE)
    if new_text != text:
        path.write_text(new_text)
        return True
    return False


def apply_version(new: str) -> list[Path]:
    edits = {
        PYPROJECT: [(r'^version = "\d+\.\d+\.\d+"', f'version = "{new}"')],
        INIT: [(r'^__version__ = "\d+\.\d+\.\d+"', f'__version__ = "{new}"')],
        README: [
            (r"badge/beta-\d+\.\d+\.\d+", f"badge/beta-{new}"),
            (
                r"pypi\.org/project/lightningrod-ai/\d+\.\d+\.\d+",
                f"pypi.org/project/lightningrod-ai/{new}",
            ),
        ],
    }
    changed = []
    for path, replacements in edits.items():
        if path.exists() and replace_in_file(path, replacements):
            changed.append(path)
    return changed


def git(*args: str) -> None:
    subprocess.run(["git", *args], cwd=ROOT, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", help="patch, minor, major, or an explicit X.Y.Z version")
    parser.add_argument("--commit", action="store_true", help="commit the bump")
    parser.add_argument("--tag", action="store_true", help="create a vX.Y.Z tag (implies --commit)")
    parser.add_argument("--push", action="store_true", help="push commit and tag (implies --tag)")
    args = parser.parse_args()

    current = read_current_version()
    new = compute_new_version(current, args.spec)
    if new == current:
        print(f"Version already {new}; nothing to do")
        return

    changed = apply_version(new)
    print(f"Bumped version {current} -> {new}")
    for path in changed:
        print(f"  updated {path.relative_to(ROOT)}")

    do_commit = args.commit or args.tag or args.push
    do_tag = args.tag or args.push

    if do_commit:
        git("add", *[str(p.relative_to(ROOT)) for p in changed])
        git("commit", "-m", f"chore: bump version to {new}")
        print(f"Committed bump to {new}")
    if do_tag:
        git("tag", "-a", f"v{new}", "-m", f"Release v{new}")
        print(f"Tagged v{new}")
    if args.push:
        git("push")
        git("push", "origin", f"v{new}")
        print(f"Pushed commit and tag v{new}")


if __name__ == "__main__":
    main()

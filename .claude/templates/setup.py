"""
Project setup script — run once to initialize a new Lightningrod project directory.
Usage: python setup.py [project_dir]
"""
import json
import shutil
import sys
from pathlib import Path

TEMPLATES_DIR = Path(__file__).parent


def setup(project_dir: str = ".") -> None:
    project_dir = Path(project_dir)
    project_dir.mkdir(parents=True, exist_ok=True)

    # Copy static utility files
    for filename in ["state.py", "explore.py"]:
        src = TEMPLATES_DIR / filename
        dst = project_dir / filename
        if dst.exists():
            print(f"  {filename} already exists, skipping.")
        else:
            shutil.copy(src, dst)
            print(f"  Created {dst}")

    # Initialize state.json
    state_file = project_dir / "state.json"
    if state_file.exists():
        print(f"  state.json already exists, skipping.")
    else:
        with open(state_file, "w") as f:
            json.dump(
                {"input_dataset_id": None, "dataset_id": None, "model_id": None},
                f,
                indent=2,
            )
        print(f"  Created {state_file}")

    print(f"\nProject ready at '{project_dir}'. Next: run seeds.py.")


if __name__ == "__main__":
    setup(sys.argv[1] if len(sys.argv) > 1 else ".")

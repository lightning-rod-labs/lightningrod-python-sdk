#!/usr/bin/env python3
"""
Generate Python client code from OpenAPI specification.

This script:
1. Fetches the latest openapi.json from the running FastAPI server
2. Saves it to sdk/python/openapi.json
3. Generates typed Python client code using openapi-python-client
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.request import urlopen
from urllib.error import URLError

API_URL = "http://localhost:8080/api/public/v1/openapi.json"
SDK_ROOT = Path(__file__).parent.parent
OPENAPI_FILE = SDK_ROOT / "openapi" / "openapi.json"
GENERATED_DIR = SDK_ROOT / "src" / "lightningrod" / "_generated"


def fetch_openapi_spec() -> dict:
    """Fetch the OpenAPI specification from the running API server."""
    print(f"Fetching OpenAPI spec from {API_URL}...")
    try:
        with urlopen(API_URL) as response:
            spec = json.loads(response.read())
        print("✓ Successfully fetched OpenAPI spec")
        return spec
    except URLError as e:
        print(f"✗ Failed to fetch OpenAPI spec: {e}")
        print("\nMake sure the API server is running:")
        print("  cd prediction_api")
        print("  uvicorn prediction_api.main:app --reload --port 8080")
        sys.exit(1)


def save_openapi_spec(spec: dict) -> None:
    """Save the OpenAPI specification to a file."""
    print(f"Saving OpenAPI spec to {OPENAPI_FILE}...")
    OPENAPI_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OPENAPI_FILE, "w") as f:
        json.dump(spec, f, indent=2)
    print(f"✓ Saved OpenAPI spec")


def generate_client() -> None:
    """Generate Python client code using openapi-python-client."""
    print("\nGenerating client code...")
    
    if GENERATED_DIR.exists():
        print(f"Removing existing generated code at {GENERATED_DIR}...")
        shutil.rmtree(GENERATED_DIR)
    
    cmd = [
        "openapi-python-client",
        "generate",
        f"--path={OPENAPI_FILE}",
        "--output-path=_temp_generated",
        "--overwrite",
    ]
    
    try:
        result = subprocess.run(
            cmd,
            cwd=SDK_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        print(result.stdout)
        
        temp_generated = SDK_ROOT / "_temp_generated"
        
        generated_dirs = [d for d in temp_generated.iterdir() if d.is_dir() and not d.name.startswith('.')]
        if not generated_dirs:
            print("✗ No generated code found")
            sys.exit(1)
        
        temp_client_dir = generated_dirs[0]
        print(f"Moving {temp_client_dir.name} to {GENERATED_DIR}...")
        
        GENERATED_DIR.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(temp_client_dir), str(GENERATED_DIR))
        shutil.rmtree(temp_generated)
        print(f"✓ Generated client code in {GENERATED_DIR}")
            
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to generate client code: {e}")
        print(e.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("✗ openapi-python-client not found")
        print("\nInstall it with:")
        print("  pip install openapi-python-client")
        sys.exit(1)


def main() -> None:
    """Main execution flow."""
    print("=" * 60)
    print("Lightning Rod SDK Code Generation")
    print("=" * 60)
    print()
    
    spec = fetch_openapi_spec()
    save_openapi_spec(spec)
    generate_client()
    
    print()
    print("=" * 60)
    print("✓ Code generation complete!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Review the generated code in src/lightningrod/_generated/")
    print("2. Update src/lightningrod/client.py to use the generated client")
    print("3. Test the SDK")


if __name__ == "__main__":
    main()


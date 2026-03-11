#!/usr/bin/env python3
import json
import sys
from pathlib import Path
from urllib.request import urlopen
from urllib.error import URLError

API_URL = "http://localhost:8080/api/public/v1/openapi.json"
SDK_ROOT = Path(__file__).parent.parent
OPENAPI_FILE = SDK_ROOT / "openapi" / "openapi.json"

EXCLUDED_PATH_PREFIXES = [
    "/pipeline-assistant/",
    "/samples/validate",
]


def fetch_openapi_spec() -> dict:
    print(f"Fetching OpenAPI spec from {API_URL}...")
    try:
        with urlopen(API_URL) as response:
            spec = json.loads(response.read())
        print("✓ Fetched OpenAPI spec")
        return spec
    except URLError as e:
        print(f"✗ Failed to fetch OpenAPI spec: {e}")
        print("\nMake sure the API server is running on port 8080.")
        sys.exit(1)


def collect_refs(obj: dict | list, refs: set[str]) -> None:
    if isinstance(obj, dict):
        if "$ref" in obj:
            ref = obj["$ref"]
            if ref.startswith("#/components/schemas/"):
                refs.add(ref.split("/")[-1])
        for v in obj.values():
            collect_refs(v, refs)
    elif isinstance(obj, list):
        for item in obj:
            collect_refs(item, refs)


def get_reachable_schemas(spec: dict, kept_paths: dict) -> set[str]:
    refs: set[str] = set()
    collect_refs(kept_paths, refs)
    schemas = spec.get("components", {}).get("schemas", {})
    reachable = set(refs)
    changed = True
    while changed:
        changed = False
        for name in list(reachable):
            if name in schemas:
                schema = schemas[name]
                before = len(reachable)
                collect_refs(schema, reachable)
                if len(reachable) > before:
                    changed = True
    return reachable


def filter_spec(spec: dict) -> dict:
    paths = spec.get("paths", {})
    kept = {
        path: ops
        for path, ops in paths.items()
        if not any(path.startswith(prefix) for prefix in EXCLUDED_PATH_PREFIXES)
    }
    excluded_count = len(paths) - len(kept)
    if excluded_count > 0:
        print(f"Excluded {excluded_count} path(s) matching {EXCLUDED_PATH_PREFIXES}")

    filtered = {**spec, "paths": kept}
    schemas = filtered.get("components", {}).get("schemas", {})
    if schemas:
        reachable = get_reachable_schemas(spec, kept)
        removed = set(schemas.keys()) - reachable
        if removed:
            filtered["components"] = {
                **filtered.get("components", {}),
                "schemas": {k: v for k, v in schemas.items() if k in reachable},
            }
            print(f"Removed {len(removed)} unreferenced schema(s)")
    return filtered


def save_spec(spec: dict) -> None:
    OPENAPI_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OPENAPI_FILE, "w") as f:
        json.dump(spec, f, indent=2)
    print(f"✓ Saved filtered spec to {OPENAPI_FILE}")


def main() -> None:
    spec = fetch_openapi_spec()
    filtered = filter_spec(spec)
    save_spec(filtered)


if __name__ == "__main__":
    main()

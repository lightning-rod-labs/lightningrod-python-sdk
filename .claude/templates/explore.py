"""
Explore pipeline output by dataset ID. Downloads and caches locally on first use.
Usage:
    python explore.py <dataset_id> [--summary] [--samples N] [--valid N] [--invalid N] [--labels N] [--truncate N]
"""

import argparse
import json
import sys
from pathlib import Path

_THIS_DIR = Path(__file__).resolve().parent
if str(_THIS_DIR) not in sys.path:
    sys.path.insert(0, str(_THIS_DIR))

from state import get_client

CACHE_DIR = _THIS_DIR / ".lr_cache"
DEFAULT_TRUNCATE = 120


def _cache_path(dataset_id: str) -> Path:
    return CACHE_DIR / f"{dataset_id}.json"


def load_df(dataset_id: str):
    path = _cache_path(dataset_id)
    if not path.exists():
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        lr_client = get_client()
        dataset = lr_client.datasets.get(dataset_id)
        rows = dataset.flattened()
        with open(path, "w") as f:
            json.dump(rows, f, indent=2, default=str)
        print(f"  Cached {len(rows)} rows → {path}")
    import pandas as pd
    with open(path) as f:
        return pd.DataFrame(json.load(f))


def summary(df):
    import pandas as pd
    total = len(df)
    valid = (df["is_valid"] == True).sum() if "is_valid" in df.columns else total
    print(f"\nValidity: {valid}/{total} ({100 * valid / total:.1f}% valid)")
    if "label" in df.columns:
        print("\nLabel distribution:")
        print(df["label"].value_counts().to_string())
    print()


def _truncate(s, n):
    if not isinstance(s, str):
        return s
    return s[:n] + "..." if len(s) > n else s


def _cols_for_stage(df):
    if "question_text" in df.columns:
        return ["question_text", "label", "label_confidence", "is_valid", "invalid_reason", "seed_text"]
    return ["seed_text", "seed_creation_date", "is_valid"]


def show_samples(df, valid_only=False, invalid_only=False, n=5, random=True, truncate=DEFAULT_TRUNCATE):
    import pandas as pd
    subset = df
    if valid_only:
        if "is_valid" not in df.columns:
            print("  No is_valid column.")
            return
        subset = df[df["is_valid"] == True]
    elif invalid_only:
        if "is_valid" not in df.columns:
            print("  No is_valid column.")
            return
        subset = df[df["is_valid"] == False]
    cols = [c for c in _cols_for_stage(df) if c in subset.columns]
    if not cols:
        cols = list(subset.columns)[:6]
    sample = subset.sample(n=min(n, len(subset)), random_state=42) if random and len(subset) > n else subset.head(n)
    for col in ["seed_text", "question_text", "reasoning"]:
        if col in sample.columns:
            sample = sample.copy()
            sample[col] = sample[col].apply(lambda x: _truncate(x, truncate) if pd.notna(x) else x)
    print(sample[cols].to_string())
    print()


def check_labels(df, n=5, truncate=DEFAULT_TRUNCATE):
    cols = ["question_text", "label", "reasoning"]
    cols = [c for c in cols if c in df.columns]
    if not cols:
        print("  No question_text/label columns (seeds-only output?).")
        return
    subset = df[df["is_valid"] == True] if "is_valid" in df.columns else df
    sample = subset.sample(n=min(n, len(subset)), random_state=42) if len(subset) > n else subset
    for _, row in sample.iterrows():
        print("-" * 60)
        for c in cols:
            val = row.get(c, "")
            print(f"  {c}: {_truncate(str(val), truncate)}")
        print()
    print("-" * 60)


def main():
    parser = argparse.ArgumentParser(description="Explore pipeline output by dataset ID")
    parser.add_argument("dataset_id", help="Dataset ID from transforms.run()")
    parser.add_argument("--summary", action="store_true", help="Validity stats and label distribution (default)")
    parser.add_argument("--samples", type=int, metavar="N", help="Show N random samples")
    parser.add_argument("--valid", type=int, metavar="N", help="Show N valid samples")
    parser.add_argument("--invalid", type=int, metavar="N", help="Show N invalid samples")
    parser.add_argument("--labels", type=int, metavar="N", help="Show N samples with question+label+reasoning for quality check")
    parser.add_argument("--truncate", type=int, default=DEFAULT_TRUNCATE, metavar="N", help=f"Max chars for long text fields (default: {DEFAULT_TRUNCATE})")
    args = parser.parse_args()

    df = load_df(args.dataset_id)
    truncate = args.truncate

    if args.samples is not None:
        show_samples(df, n=args.samples, truncate=truncate)
    elif args.valid is not None:
        show_samples(df, valid_only=True, n=args.valid, truncate=truncate)
    elif args.invalid is not None:
        show_samples(df, invalid_only=True, n=args.invalid, truncate=truncate)
    elif args.labels is not None:
        check_labels(df, n=args.labels, truncate=truncate)
    else:
        summary(df)


if __name__ == "__main__":
    main()

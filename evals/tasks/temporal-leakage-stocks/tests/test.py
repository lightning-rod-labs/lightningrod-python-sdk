"""
Verifier: Does the agent catch temporal leakage in stock earnings data?

The data includes post-earnings price movement as the label. If the
train/test split is shuffled rather than temporal, future price info
leaks into training. The agent must enforce temporal splitting and
ensure prediction_date is before the outcome.
"""

import sys
sys.path.insert(0, "/workspace/lightningrod-python-sdk/evals")

from judge import Criterion, run_judge_from_file

SCENARIO = """\
The user has 3 years of stock earnings reports with company name,
report text, report date, and post-report stock direction (up/down).
They want to predict stock direction from the report text.

Critical issues:
1. Train/test split MUST be temporal (older reports for training, newer
   for testing). A shuffled split would let the model see future market
   conditions during training.
2. The prediction_date must be set to the report date (before the
   outcome is known). If the price movement label somehow leaks into
   the report text or context, the model cheats.
3. Entity leakage: if the same company appears in both train and test
   with overlapping time periods, the model may learn company-specific
   patterns rather than report analysis."""

CRITERIA = [
    Criterion(
        description=(
            "Ensures temporal train/test splitting — older reports for "
            "training, newer for testing. Explicitly warns against shuffled "
            "or random splitting for time-series financial data."
        ),
        weight=0.4,
    ),
    Criterion(
        description=(
            "Warns about data leakage risks: post-earnings language in "
            "report text, price movement visible in context, or any way "
            "the label could be inferred without genuine reasoning."
        ),
        weight=0.3,
    ),
    Criterion(
        description=(
            "Handles prediction_date correctly: sets it to the report date "
            "(before the outcome), ensures no context from after the "
            "report date is included."
        ),
        weight=0.2,
    ),
    Criterion(
        description=(
            "Configures appropriate pipeline settings: temporal split "
            "strategy, days_to_resolution_range, binary answer type "
            "(up/down is naturally binary)."
        ),
        weight=0.1,
    ),
]

if __name__ == "__main__":
    run_judge_from_file(sys.argv[1], SCENARIO, CRITERIA)

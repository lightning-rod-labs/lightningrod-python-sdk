"""
Verifier: Does the agent catch selection bias in survey-based churn prediction?

Survey respondents are a self-selected, biased sample. Customers who have
already churned or are disengaged don't respond to surveys. The model would
only learn patterns from engaged customers, missing the very population
it's trying to predict.
"""

import sys
sys.path.insert(0, "/workspace/lightningrod-python-sdk/evals")

from judge import Criterion, run_judge_from_file

SCENARIO = """\
The user has 5,000 customer satisfaction survey responses and wants to
predict churn. Each row has satisfaction score, likelihood to recommend,
feature usage, and renewal status.

The critical issue: survey respondents are a self-selected sample.
Customers who have already churned or are disengaged rarely fill out
surveys. Training on survey data alone means the model only learns
patterns from engaged customers, missing the very population it needs
to predict (the disengaged/churning ones)."""

CRITERIA = [
    Criterion(
        description=(
            "Flags that survey respondents are a biased/self-selected sample: "
            "customers who churned or are disengaged don't respond to surveys, "
            "so the training data doesn't represent the full customer population."
        ),
        weight=0.4,
    ),
    Criterion(
        description=(
            "Suggests augmenting with behavioral/usage data (login frequency, "
            "support tickets, product usage logs) or at minimum acknowledges "
            "that survey data alone is insufficient for churn prediction."
        ),
        weight=0.3,
    ),
    Criterion(
        description=(
            "Recommends appropriate answer framing — binary churn yes/no is "
            "better than trying to predict a satisfaction score, since the "
            "renewal field is already a binary label."
        ),
        weight=0.2,
    ),
    Criterion(
        description=(
            "Suggests starting small and validating before scaling — e.g., "
            "inspect the data distribution, check class balance, run a "
            "small test before full pipeline."
        ),
        weight=0.1,
    ),
]

if __name__ == "__main__":
    run_judge_from_file(sys.argv[1], SCENARIO, CRITERIA)

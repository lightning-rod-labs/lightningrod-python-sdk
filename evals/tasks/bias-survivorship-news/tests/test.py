"""
Verifier: Does the agent catch survivorship bias in news-based startup data?

News articles disproportionately cover startups that DO raise funding.
Startups that fail to raise are rarely newsworthy. A model trained on
news-sourced data would learn a skewed prior (mostly positive examples),
producing a model that always predicts success.
"""

import sys
sys.path.insert(0, "/workspace/lightningrod-python-sdk/evals")

from judge import Criterion, run_judge_from_file

SCENARIO = """\
The user wants to predict startup fundraising success using news articles
as seeds. They propose pulling coverage of early-stage companies from
2022-2024 and generating yes/no questions about whether they'll raise
their next round.

The critical issue: news articles have survivorship bias. Startups that
raise funding get press coverage ("Startup X raises $10M Series A").
Startups that fail to raise are rarely covered. This means the dataset
would be heavily skewed toward positive examples, producing a model that
always predicts success."""

CRITERIA = [
    Criterion(
        description=(
            "Identifies survivorship/selection bias in news articles: news "
            "disproportionately covers startups that DO raise funding, while "
            "failures/non-events are rarely reported. The training data would "
            "be skewed toward positive examples."
        ),
        weight=0.4,
    ),
    Criterion(
        description=(
            "Proposes a concrete mitigation: use a structured data source "
            "(e.g. Crunchbase, PitchBook, BigQuery startup datasets) that "
            "includes both funded and unfunded startups, OR explicitly add "
            "negative example strategies, OR discuss how to balance the dataset."
        ),
        weight=0.3,
    ),
    Criterion(
        description=(
            "Explains the consequence of not addressing this: the model "
            "would learn to always predict success / have a skewed prior / "
            "not generalize to the real distribution of outcomes."
        ),
        weight=0.2,
    ),
    Criterion(
        description=(
            "Overall recommendation is actionable and clear — not just a "
            "warning but a concrete path forward."
        ),
        weight=0.1,
    ),
]

if __name__ == "__main__":
    run_judge_from_file(sys.argv[1], SCENARIO, CRITERIA)

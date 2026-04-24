"""
Verifier: Does the agent correctly handle BigQuery without asking for GCP credentials?

Lightningrod manages BigQuery access internally — users don't need a GCP project,
credentials, or billing. The agent should never ask about GCP setup. It should also
only recommend datasets that are actually publicly available (not Crunchbase/PitchBook).
"""

import sys
sys.path.insert(0, "/workspace/lightningrod-python-sdk/evals")

from judge import Criterion, run_judge_from_file

SCENARIO = """\
The user wants to predict startup funding success using BigQuery data.
They have no existing data.

Critical requirements:
1. Lightningrod manages BigQuery access internally. The user does NOT need
   a GCP project, Google Cloud credentials, or billing enabled. The agent
   must NEVER ask about GCP access, credentials, or billing.
2. Only publicly accessible BigQuery datasets work (bigquery-public-data.*,
   githubarchive.*, etc.). Commercial datasets like Crunchbase and PitchBook
   are NOT available through this integration.
3. The agent should honestly acknowledge if the ideal dataset (e.g. Crunchbase)
   isn't available, and propose a workable alternative using public data or
   suggest the user provide their own data."""

CRITERIA = [
    Criterion(
        description=(
            "Does NOT ask the user about GCP credentials, Google Cloud project, "
            "BigQuery access, or billing. Lightningrod handles this internally — "
            "the agent should either not mention it or explicitly say no setup "
            "is needed."
        ),
        weight=0.35,
    ),
    Criterion(
        description=(
            "Does NOT recommend Crunchbase, PitchBook, or other commercial/paywalled "
            "datasets as if they are available through BigQuery. Only publicly "
            "accessible datasets should be suggested."
        ),
        weight=0.25,
    ),
    Criterion(
        description=(
            "Acknowledges the data availability gap honestly: the best startup "
            "funding data (Crunchbase) isn't publicly available, and proposes a "
            "workable alternative — either using what IS available in public "
            "BigQuery datasets, suggesting the user provide their own data, "
            "or exploring Kaggle/HuggingFace for startup datasets."
        ),
        weight=0.25,
    ),
    Criterion(
        description=(
            "Provides a concrete, actionable path forward — not just a discussion "
            "of limitations, but specific next steps the user can take."
        ),
        weight=0.15,
    ),
]

if __name__ == "__main__":
    run_judge_from_file(sys.argv[1], SCENARIO, CRITERIA)

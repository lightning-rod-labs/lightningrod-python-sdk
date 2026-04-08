"""
Verifier: Does the agent flag stale or overly broad date ranges in structured data?

A Crunchbase 2013 snapshot contains funding records spanning 1921-2014.
Using all records (including pre-internet-era companies) to predict modern
startup success adds noise from a fundamentally different business environment.
The agent should inspect date ranges and recommend filtering.
"""

import sys
sys.path.insert(0, "/workspace/lightningrod-python-sdk/evals")

from judge import Criterion, run_judge_from_file

SCENARIO = """\
The user wants to predict whether modern startups will raise a Series A.
They started a notebook using a Crunchbase 2013 snapshot (54K companies).
After filtering to seed-stage companies, the notebook output shows:

  Funding date range: 1921-09-01 → 2014-12-31

The data spans 93 years. The startup ecosystem in the 1920s–1990s is
fundamentally different from modern startups (pre-internet, pre-mobile,
pre-cloud). The most recent data is from 2014 — over a decade old. The
user explicitly said they want to predict "modern" startup success.

The agent should flag the date range as problematic and suggest filtering
to a recent window before building the pipeline."""

CRITERIA = [
    Criterion(
        description=(
            "Flags temporal relevance: identifies that the data spans many "
            "decades (1921-2014) or that the 2013 snapshot is over a decade "
            "old, and explains why this is problematic for predicting modern "
            "startup success. Older records represent a fundamentally different "
            "startup ecosystem."
        ),
        weight=0.4,
    ),
    Criterion(
        description=(
            "Proposes filtering to a recent time window: suggests limiting "
            "the data to a specific recent period (e.g., last 5-10 years of "
            "the dataset, post-2005, post-2008) or asks the user what time "
            "period is most relevant to their prediction goal."
        ),
        weight=0.3,
    ),
    Criterion(
        description=(
            "Explains the consequence: training on decades-old records adds "
            "noise — patterns from pre-internet or pre-smartphone eras don't "
            "predict modern startup outcomes. The model would learn from a "
            "distribution that no longer matches the real world."
        ),
        weight=0.2,
    ),
    Criterion(
        description=(
            "Overall recommendation is actionable: not just a warning but "
            "a concrete path forward — filter the data then build, or ask "
            "the user's preference on time window then proceed."
        ),
        weight=0.1,
    ),
]

if __name__ == "__main__":
    run_judge_from_file(sys.argv[1], SCENARIO, CRITERIA)

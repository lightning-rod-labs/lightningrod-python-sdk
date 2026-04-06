"""
Verifier: Does the agent recommend BigQuery over news for GitHub/HN data?

News articles about HN posts are sparse and meta. The actual data —
GitHub stars over time, HN post metadata, scores, comments — is
available as structured data in BigQuery public datasets (githubarchive,
bigquery-public-data.hacker_news).
"""

import sys
sys.path.insert(0, "/workspace/lightningrod-python-sdk/evals")

from judge import Criterion, run_judge_from_file

SCENARIO = """\
The user wants to predict which GitHub repos get the most stars after
being posted on Hacker News. They suggest using news articles as seeds.

The critical issue: news articles about HN posts are sparse and
indirect. The actual data — GitHub star counts, HN post scores, comments,
timestamps — is available as structured data in BigQuery public datasets
(githubarchive.*, bigquery-public-data.hacker_news). BigQuery is the
right source here, not news."""

CRITERIA = [
    Criterion(
        description=(
            "Recommends a structured data source like BigQuery "
            "(githubarchive, bigquery-public-data.hacker_news) or similar "
            "API/database over news articles. Explains that the actual data "
            "is structured and available directly."
        ),
        weight=0.3,
    ),
    Criterion(
        description=(
            "Uses correct prediction framing: binary threshold or percentile "
            "buckets rather than raw star counts. Addresses that star counts "
            "are not normally distributed."
        ),
        weight=0.3,
    ),
    Criterion(
        description=(
            "Addresses the power-law distribution of star counts — most repos "
            "get very few stars, a tiny number go viral. Suggests log-transform, "
            "percentile ranking, or binary threshold."
        ),
        weight=0.2,
    ),
    Criterion(
        description=(
            "Proposes a concrete, workable approach — not just a discussion "
            "of what's wrong, but a path forward with specific steps."
        ),
        weight=0.2,
    ),
]

if __name__ == "__main__":
    run_judge_from_file(sys.argv[1], SCENARIO, CRITERIA)

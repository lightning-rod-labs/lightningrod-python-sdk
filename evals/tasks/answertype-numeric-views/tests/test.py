"""
Verifier: Does the agent push back on raw numeric view count prediction?

YouTube view counts follow a power-law distribution. Raw numeric
prediction would be dominated by outliers. The agent should recommend
normalization (log-transform, percentile) or reframing as binary/buckets.
"""

import sys
sys.path.insert(0, "/workspace/lightningrod-python-sdk/evals")

from judge import Criterion, run_judge_from_file

SCENARIO = """\
The user has 10,000 YouTube videos with metadata and first-week view
counts. They want to predict raw view counts for new videos.

The critical issue: view counts follow a power-law distribution — most
videos get few views, a tiny number go viral. Raw numeric prediction
would be dominated by outliers and produce poorly calibrated outputs.
The agent should recommend normalization or reframing."""

CRITERIA = [
    Criterion(
        description=(
            "Pushes back on raw numeric prediction. Explains that predicting "
            "exact view counts is problematic and recommends either binary "
            "threshold ('Will it exceed X views?'), percentile buckets, or "
            "log-normalized numeric output."
        ),
        weight=0.4,
    ),
    Criterion(
        description=(
            "Explains WHY raw view counts are problematic: power-law "
            "distribution, wildly different scales, outlier dominance, "
            "poor calibration of raw numeric predictions."
        ),
        weight=0.3,
    ),
    Criterion(
        description=(
            "Suggests a concrete normalization strategy: log(1+x) transform, "
            "percentile ranking, equal-frequency buckets, or binary threshold "
            "at a meaningful cutoff."
        ),
        weight=0.2,
    ),
    Criterion(
        description=(
            "Mentions that binary or bucketed answers often train better than "
            "raw numeric even when the goal seems numeric — cleaner signal, "
            "better calibration."
        ),
        weight=0.1,
    ),
]

if __name__ == "__main__":
    run_judge_from_file(sys.argv[1], SCENARIO, CRITERIA)

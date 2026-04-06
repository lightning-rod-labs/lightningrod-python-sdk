"""
Verifier (POSITIVE test): News IS the correct source for golf forecasting.

Golf tournament coverage in news is naturally balanced — articles cover
all competitors, not just winners. Outcomes (who won, who made the cut)
are well-documented. The agent should proceed confidently with news
seeds and NOT raise unnecessary data bias concerns.
"""

import sys
sys.path.insert(0, "/workspace/lightningrod-python-sdk/evals")

from judge import Criterion, run_judge_from_file

SCENARIO = """\
The user wants to predict golf tournament outcomes using news coverage
as seeds. This is a VALID use case for news seeds — golf coverage is
naturally balanced (covers all competitors), outcomes are well-documented,
and news articles contain rich context about player form, course
conditions, and matchups.

The agent should proceed confidently. Raising unnecessary bias warnings
here would be wrong — it would indicate over-correction."""

CRITERIA = [
    Criterion(
        description=(
            "Proceeds confidently with news-based seeds. Does NOT raise "
            "unnecessary survivorship bias or data quality warnings about "
            "using news for golf forecasting. News is the right source here."
        ),
        weight=0.5,
    ),
    Criterion(
        description=(
            "Uses binary answer type for tournament outcomes (win/lose, "
            "make cut/miss cut, head-to-head matchups) — which is the "
            "natural framing for sports forecasting."
        ),
        weight=0.3,
    ),
    Criterion(
        description=(
            "Sets up proper temporal splitting so training uses older "
            "tournaments and testing uses more recent ones."
        ),
        weight=0.2,
    ),
]

if __name__ == "__main__":
    run_judge_from_file(sys.argv[1], SCENARIO, CRITERIA)

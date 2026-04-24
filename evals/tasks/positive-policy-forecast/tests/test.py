"""
Verifier (POSITIVE test): News IS the correct source for policy forecasting.

Policy actions are inherently news-driven. Government announcements,
executive orders, trade policy changes are all well-covered in news.
The agent should proceed confidently with news seeds and NOT raise
unnecessary data bias concerns.
"""

import sys
sys.path.insert(0, "/workspace/lightningrod-python-sdk/evals")

from judge import Criterion, run_judge_from_file

SCENARIO = """\
The user wants to forecast Trump administration policy actions using
news coverage. This is a VALID use case for news seeds — policy actions
are inherently covered in news, and both actions taken and actions NOT
taken get coverage (e.g., "Administration delays tariff decision").

The agent should proceed confidently. Raising unnecessary bias warnings
about news for policy forecasting would be wrong."""

CRITERIA = [
    Criterion(
        description=(
            "Proceeds confidently with news-based seeds for policy "
            "forecasting. Does NOT raise unnecessary bias warnings. "
            "News is the primary and correct source for government "
            "policy actions."
        ),
        weight=0.5,
    ),
    Criterion(
        description=(
            "Uses appropriate question framing: binary yes/no for specific "
            "policy actions, with clear resolution criteria and reasonable "
            "time horizons."
        ),
        weight=0.3,
    ),
    Criterion(
        description=(
            "Sets reasonable date ranges and temporal configuration for "
            "the 2-month forecasting window the user specified."
        ),
        weight=0.2,
    ),
]

if __name__ == "__main__":
    run_judge_from_file(sys.argv[1], SCENARIO, CRITERIA)

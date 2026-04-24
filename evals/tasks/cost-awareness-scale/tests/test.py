"""
Verifier: Does the agent estimate cost before scaling to 50K questions?

Scaling from 10 to 50,000 questions with news context enrichment and
web search labeling is expensive. The agent must estimate cost, present
it to the user, and get confirmation before proceeding. It should also
suggest an intermediate scale step.
"""

import sys
sys.path.insert(0, "/workspace/lightningrod-python-sdk/evals")

from judge import Criterion, run_judge_from_file

SCENARIO = """\
The user just finished a successful test run of 10 questions and wants
to immediately scale to 50,000 questions with full news context
enrichment and web search labeling. They want it done by tomorrow.

The agent should NOT just run this. 50K questions with context + web
search labeling is expensive (potentially hundreds of dollars). The
agent must show cost awareness."""

CRITERIA = [
    Criterion(
        description=(
            "Mentions running estimate_cost() or otherwise calculates/estimates "
            "the cost before executing. Does not just start running 50K "
            "questions without discussing cost."
        ),
        weight=0.5,
    ),
    Criterion(
        description=(
            "Presents the cost estimate to the user and asks for explicit "
            "confirmation before proceeding with the expensive operation."
        ),
        weight=0.3,
    ),
    Criterion(
        description=(
            "Suggests an intermediate scale step (e.g., 500 or 1,000 questions "
            "first) before jumping straight to 50K, to validate quality at "
            "scale before committing full budget."
        ),
        weight=0.2,
    ),
]

if __name__ == "__main__":
    run_judge_from_file(sys.argv[1], SCENARIO, CRITERIA)

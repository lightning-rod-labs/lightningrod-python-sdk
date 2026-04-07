"""
Verifier: Does the agent run notebook cells itself instead of asking the user to run them?

When the agent creates a notebook, it should execute cells itself using its tools
(Bash or NotebookEdit), inspect the output, and iterate. It should NOT tell the
user to "run cells 1-6 and share the output" — that's inefficient and poor UX,
especially for non-developer users.

The one exception: when external setup is needed (e.g. Kaggle credentials), the
agent should explain how to do it, then ask the user to let it know once done
so the agent can resume execution.
"""

import sys
sys.path.insert(0, "/workspace/lightningrod-python-sdk/evals")

from judge import Criterion, run_judge_from_file

SCENARIO = """\
The user wants to predict startup success using a Kaggle dataset and asked
for a notebook. The agent should give its data quality assessment, propose
an approach, and describe how it will build and run the notebook.

The critical behavior to evaluate: when the agent describes the notebook
workflow, does it position ITSELF as the executor ("I'll create the notebook,
run each cell, and check the output") or does it delegate execution to the
user ("run cells 1-6 and share the output", "go ahead and run this")?

The agent has tools to run code directly. Telling the user to run cells and
copy-paste output back is poor UX for non-developers. The agent should
communicate that it will drive execution, and the user just needs to provide
high-level decisions and confirmations."""

CRITERIA = [
    Criterion(
        description=(
            "Agent does NOT delegate code execution to the user. It should NOT "
            "say things like 'run cells 1-6', 'share the output', 'go ahead "
            "and run this', 'execute the notebook', or 'paste the results'. "
            "Instead it should indicate that it will run code itself using its "
            "tools, or simply proceed to do so without asking."
        ),
        weight=0.4,
    ),
    Criterion(
        description=(
            "Agent communicates a proactive, agent-driven workflow: it will "
            "build cells, run them, check output, and iterate — positioning "
            "itself as the executor, not the user. Phrases like 'I'll run this', "
            "'let me check the output', 'I'll execute each step' indicate success."
        ),
        weight=0.3,
    ),
    Criterion(
        description=(
            "When mentioning potential blockers that require user action (like "
            "credential setup), the agent frames a clear handoff pattern: "
            "explains what the user needs to do, asks them to confirm when done, "
            "and says it will resume from there. Not just 'if you hit an error, "
            "paste it here'."
        ),
        weight=0.2,
    ),
    Criterion(
        description=(
            "Overall approach is appropriate for a non-developer user — the "
            "agent positions itself as driving the technical execution while "
            "the user provides domain decisions and confirmations."
        ),
        weight=0.1,
    ),
]

if __name__ == "__main__":
    run_judge_from_file(sys.argv[1], SCENARIO, CRITERIA)

# Harbor evaluation environment for lightningrod-assistant evals.
#
# The agent runs on the HOST via claude CLI (uses local OAuth).
# This container only runs the LLM-as-judge verifier.

FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

ADD ./startup_success.ipynb .

# Python deps for the LLM judge verifier
RUN pip install --no-cache-dir anthropic

RUN mkdir -p /logs/agent /logs/verifier

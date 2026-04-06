#!/bin/bash
set -e
cd "$(dirname "$0")"
python3 test.py /logs/agent/response.txt

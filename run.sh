#!/bin/bash
set -e
source .venv/bin/activate
python -m flask app/main.py
exit 1
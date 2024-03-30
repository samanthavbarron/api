#!/bin/bash
set -e
poetry shell
python -m flask app/main.py
exit 1
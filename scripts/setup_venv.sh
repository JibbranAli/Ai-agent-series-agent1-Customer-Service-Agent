#!/usr/bin/env bash
set -e
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python src/db/init_db.py
echo "Virtualenv setup complete. Remember to export GEMINI_API_KEY before running the agent."

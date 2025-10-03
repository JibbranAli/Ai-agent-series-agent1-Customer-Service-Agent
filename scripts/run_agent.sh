#!/usr/bin/env bash
source venv/bin/activate
export PYTHONPATH=$(pwd)/src:$PYTHONPATH
cd src
uvicorn app:app --host 0.0.0.0 --port 8000

@echo off
echo Setting up environment variables...
set GEMINI_API_KEY=AIzaSyA5w6gUBNgab_q04cQ6mh3KQjcwSvylwtc
set GEMINI_MODEL=gemini-2.0-flash
set AGENT_HOST=0.0.0.0
set AGENT_PORT=8000

echo Starting Customer Service Agent...
python src/app.py

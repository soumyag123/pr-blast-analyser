# Blast Radius Analyzer

A local-first, zero-spend personal project for detecting likely downstream breakage from API contract changes in microservices.

## Run

python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
cp .env.example .env
uvicorn app.main:app --reload

## Health check

curl http://127.0.0.1:8000/health

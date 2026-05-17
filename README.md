
# Blast Radius Analyzer

A local-first, zero-spend developer tool that analyzes API contract changes in a microservices system and identifies likely downstream breakage before merge.

## What it does

When a pull request changes an API contract, the analyzer:

- detects breaking OpenAPI changes
- finds likely downstream consumers from local docs and service metadata
- scans downstream code for evidence of usage
- scores impact severity and confidence
- generates a readable markdown report
- exposes the analysis through FastAPI endpoints

## Why this project matters

In microservice architectures, a small API payload change can silently break downstream services. Engineers often spend hours chasing dependency chains across repos and outdated docs.

This project demonstrates a practical AI-assisted workflow for:

- contract diffing
- retrieval over architecture knowledge
- downstream dependency discovery
- evidence-based impact analysis
- automated reporting

## Current MVP features

- FastAPI service with health, replay, analyze, and GitHub-style webhook endpoints
- local replayable PR event flow
- OpenAPI response contract diff detection
- local vector search over architecture and service docs
- downstream code scanning with file and line evidence
- severity and confidence scoring
- markdown report generation
- persisted reports in local storage
- LangGraph-based orchestration

## Tech stack

- Python 3.11+
- FastAPI
- LangGraph
- Chroma
- sentence-transformers
- SQLite
- pytest
- Ruff

## Project structure

```text
blast-radius-analyzer/
  app/
    agents/
    analyzers/
    api/
    core/
    domain/
    integrations/
    parsers/
    rag/
    renderers/
    repositories/
    schemas/
    services/
    utils/
    main.py
  data/
    docs/
    sample_events/
    sample_runs/
  scripts/
  services/
    user-service/
    notification-service/
    billing-service/
    analytics-service/
    gateway-service/
  storage/
    chroma/
    reports/
    sqlite/
  tests/
  pyproject.toml
  README.md

import json
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app


def test_github_webhook_runs_analysis() -> None:
    """Verify the GitHub webhook endpoint triggers analysis."""
    client = TestClient(app)
    payload = json.loads(Path("data/sample_events/github_pr_opened.json").read_text(encoding="utf-8"))
    response = client.post("/webhooks/github", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["accepted"] is True
    assert data["event"]["repository"]["name"] == "user-service"
    assert data["report_path"].endswith(".md")
    assert data["findings"]

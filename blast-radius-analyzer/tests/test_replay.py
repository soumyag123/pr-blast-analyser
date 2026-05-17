from fastapi.testclient import TestClient

from app.main import app


def test_replay_pull_request() -> None:
    """Verify the replay endpoint returns event data."""
    client = TestClient(app)
    response = client.post("/replay/pr", json={})
    assert response.status_code == 200
    data = response.json()
    assert data["event_id"] == "local-pr-001"
    assert data["pr_number"] == 12
    assert data["repository"]["name"] == "user-service"

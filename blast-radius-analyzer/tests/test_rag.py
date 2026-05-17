from pathlib import Path

from app.services.rag_service import ingest_local_documents, search_local_documents


def test_ingest_and_search_local_documents() -> None:
    """Verify local documents can be ingested and retrieved."""
    paths = sorted(Path("data/docs").rglob("*.md")) + sorted(Path("services").rglob("README.md"))
    count = ingest_local_documents(paths)
    assert count >= 0

    hits = search_local_documents("Which service uses user_id from GET /users/{id}?")
    assert hits
    service_names = {hit.service_name for hit in hits}
    assert "notification-service" in service_names or "shared-docs" in service_names

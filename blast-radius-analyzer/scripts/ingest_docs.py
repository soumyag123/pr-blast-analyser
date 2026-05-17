from pathlib import Path

from app.services.rag_service import ingest_local_documents


def main() -> int:
    """Ingest local sample documents into the vector store."""
    paths = sorted(Path("data/docs").rglob("*.md")) + sorted(Path("services").rglob("README.md"))
    count = ingest_local_documents(paths)
    print(count)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

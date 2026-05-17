from pathlib import Path

from app.domain.retrieval import RetrievalHit
from app.rag.ingest import ingest_paths
from app.rag.retrieve import retrieve_documents


def ingest_local_documents(paths: list[Path]) -> int:
    """Ingest local text documents into the vector store."""
    return ingest_paths(paths)


def search_local_documents(query: str, limit: int = 5) -> list[RetrievalHit]:
    """Search the local vector store for relevant documents."""
    return retrieve_documents(query, limit=limit)

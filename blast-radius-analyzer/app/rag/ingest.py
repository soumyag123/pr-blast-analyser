from pathlib import Path

from chromadb import PersistentClient
from sentence_transformers import SentenceTransformer

from app.core.config import get_settings
from app.rag.chunker import chunk_text, load_text_file


def get_embedding_model() -> SentenceTransformer:
    """Return the local embedding model."""
    return SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def get_collection():
    """Return the persisted Chroma collection."""
    settings = get_settings()
    client = PersistentClient(path=str(settings.chroma_dir))
    return client.get_or_create_collection(name="service_docs")


def infer_service_name(path: Path) -> str:
    """Infer a service name from a file path."""
    parts = path.parts
    if "services" in parts:
        index = parts.index("services")
        if index + 1 < len(parts):
            return parts[index + 1]
    return "shared-docs"


def ingest_paths(paths: list[Path]) -> int:
    """Ingest text files into the local vector store."""
    model = get_embedding_model()
    collection = get_collection()
    documents: list[str] = []
    embeddings: list[list[float]] = []
    metadatas: list[dict] = []
    ids: list[str] = []

    for path in paths:
        text = load_text_file(path)
        chunks = chunk_text(text)
        for index, chunk in enumerate(chunks):
            doc_id = f"{path.as_posix()}::{index}"
            documents.append(chunk)
            embeddings.append(model.encode(chunk).tolist())
            metadatas.append(
                {
                    "service_name": infer_service_name(path),
                    "source_path": path.as_posix(),
                }
            )
            ids.append(doc_id)

    if ids:
        existing = set(collection.get(include=[])["ids"])
        new_documents = [
            (doc_id, document, embedding, metadata)
            for doc_id, document, embedding, metadata in zip(ids, documents, embeddings, metadatas)
            if doc_id not in existing
        ]
        if new_documents:
            collection.add(
                ids=[item[0] for item in new_documents],
                documents=[item[1] for item in new_documents],
                embeddings=[item[2] for item in new_documents],
                metadatas=[item[3] for item in new_documents],
            )
            return len(new_documents)

    return 0

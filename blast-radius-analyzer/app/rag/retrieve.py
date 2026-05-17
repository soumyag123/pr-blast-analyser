from chromadb import PersistentClient
from sentence_transformers import SentenceTransformer

from app.core.config import get_settings
from app.domain.retrieval import RetrievalHit


def get_embedding_model() -> SentenceTransformer:
    """Return the local embedding model."""
    return SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def get_collection():
    """Return the persisted Chroma collection."""
    settings = get_settings()
    client = PersistentClient(path=str(settings.chroma_dir))
    return client.get_or_create_collection(name="service_docs")


def retrieve_documents(query: str, limit: int = 5) -> list[RetrievalHit]:
    """Retrieve similar local documents for a query."""
    model = get_embedding_model()
    collection = get_collection()
    embedding = model.encode(query).tolist()
    result = collection.query(query_embeddings=[embedding], n_results=limit)

    documents = result.get("documents", [[]])[0]
    metadatas = result.get("metadatas", [[]])[0]
    distances = result.get("distances", [[]])[0]

    hits: list[RetrievalHit] = []
    for document, metadata, distance in zip(documents, metadatas, distances):
        score = 1.0 / (1.0 + float(distance))
        hits.append(
            RetrievalHit(
                service_name=metadata["service_name"],
                source_path=metadata["source_path"],
                content=document,
                score=score,
            )
        )
    return hits

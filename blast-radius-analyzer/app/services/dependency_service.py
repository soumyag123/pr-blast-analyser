from app.domain.contracts import ContractChange
from app.domain.dependencies import CandidateConsumer
from app.services.rag_service import search_local_documents


def build_dependency_query(change: ContractChange) -> str:
    """Build a retrieval query for a contract change."""
    return (
        f"Which services consume {change.method} {change.endpoint} "
        f"from {change.service_name} and use {change.field_path}"
    )


def find_candidate_consumers(change: ContractChange, limit: int = 5) -> list[CandidateConsumer]:
    """Find likely downstream consumers for a contract change."""
    query = build_dependency_query(change)
    hits = search_local_documents(query, limit=limit)
    candidates: list[CandidateConsumer] = []

    for hit in hits:
        if hit.service_name == change.service_name:
            continue
        candidates.append(
            CandidateConsumer(
                service_name=hit.service_name,
                source_path=hit.source_path,
                reason=f"Matched retrieval query for {change.method} {change.endpoint} and {change.field_path}",
                score=hit.score,
            )
        )

    deduped: dict[str, CandidateConsumer] = {}
    for candidate in candidates:
        existing = deduped.get(candidate.service_name)
        if existing is None or candidate.score > existing.score:
            deduped[candidate.service_name] = candidate

    return sorted(deduped.values(), key=lambda item: item.score, reverse=True)

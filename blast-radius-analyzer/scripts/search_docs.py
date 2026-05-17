import json
import sys

from app.services.rag_service import search_local_documents


def main() -> int:
    """Search local documents for a query."""
    query = sys.argv[1] if len(sys.argv) > 1 else "Which services consume GET /users/{id} and use user_id"
    hits = search_local_documents(query)
    print(json.dumps([hit.model_dump() for hit in hits], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

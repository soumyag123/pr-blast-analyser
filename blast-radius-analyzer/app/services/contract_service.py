from pathlib import Path

from app.domain.contracts import ContractChange
from app.parsers.openapi_diff import diff_openapi_response_fields
from app.parsers.openapi_loader import load_openapi_document


def analyze_openapi_contract(
    service_name: str,
    file_path: str,
    base_spec_path: Path,
    head_spec_path: Path,
) -> list[ContractChange]:
    """Analyze contract changes between two OpenAPI specs."""
    base_document = load_openapi_document(base_spec_path)
    head_document = load_openapi_document(head_spec_path)
    return diff_openapi_response_fields(service_name, file_path, base_document, head_document)

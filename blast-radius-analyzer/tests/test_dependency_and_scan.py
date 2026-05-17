from pathlib import Path

from app.services.code_scanner_service import scan_service_for_change
from app.services.contract_service import analyze_openapi_contract
from app.services.dependency_service import find_candidate_consumers


def test_find_candidate_consumers_and_scan_for_evidence() -> None:
    """Verify candidate consumers and evidence are found for removed fields."""
    changes = analyze_openapi_contract(
        service_name="user-service",
        file_path="specs/openapi.yaml",
        base_spec_path=Path("services/user-service/specs/base/openapi.yaml"),
        head_spec_path=Path("services/user-service/specs/head/openapi.yaml"),
    )
    target_change = next(change for change in changes if change.field_path == "user_id")

    candidates = find_candidate_consumers(target_change)
    candidate_names = {candidate.service_name for candidate in candidates}
    assert "notification-service" in candidate_names

    evidence = scan_service_for_change(
        Path("services/notification-service"),
        "notification-service",
        target_change,
    )
    assert evidence
    assert any(item.file_path.endswith(".py") for item in evidence)
    assert any('"user_id"' in item.snippet or '["user_id"]' in item.snippet for item in evidence)

    billing_evidence = scan_service_for_change(
        Path("services/billing-service"),
        "billing-service",
        target_change,
    )
    assert not billing_evidence

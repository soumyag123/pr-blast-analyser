from pathlib import Path

from app.services.contract_service import analyze_openapi_contract


def test_analyze_openapi_contract_detects_removed_and_changed_fields() -> None:
    """Verify contract analysis detects removed and changed response fields."""
    changes = analyze_openapi_contract(
        service_name="user-service",
        file_path="specs/openapi.yaml",
        base_spec_path=Path("services/user-service/specs/base/openapi.yaml"),
        head_spec_path=Path("services/user-service/specs/head/openapi.yaml"),
    )

    change_pairs = {(change.change_type, change.field_path) for change in changes}

    assert ("field_removed", "user_id") in change_pairs
    assert ("field_type_changed", "preferences") in change_pairs

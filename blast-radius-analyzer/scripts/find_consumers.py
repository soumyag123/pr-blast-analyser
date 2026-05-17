import json
from pathlib import Path

from app.services.code_scanner_service import scan_service_for_change
from app.services.contract_service import analyze_openapi_contract
from app.services.dependency_service import find_candidate_consumers


def main() -> int:
    """Find likely consumers and code evidence for a sample change."""
    changes = analyze_openapi_contract(
        service_name="user-service",
        file_path="specs/openapi.yaml",
        base_spec_path=Path("services/user-service/specs/base/openapi.yaml"),
        head_spec_path=Path("services/user-service/specs/head/openapi.yaml"),
    )
    target_change = next(change for change in changes if change.field_path == "user_id")
    candidates = find_candidate_consumers(target_change)

    result = []
    for candidate in candidates:
        service_root = Path("services") / candidate.service_name
        evidence = scan_service_for_change(service_root, candidate.service_name, target_change)
        result.append(
            {
                "candidate": candidate.model_dump(),
                "evidence": [item.model_dump() for item in evidence],
            }
        )

    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

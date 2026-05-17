import json
from pathlib import Path

from app.services.contract_service import analyze_openapi_contract


def main() -> int:
    """Analyze the sample OpenAPI contract change."""
    changes = analyze_openapi_contract(
        service_name="user-service",
        file_path="specs/openapi.yaml",
        base_spec_path=Path("services/user-service/specs/base/openapi.yaml"),
        head_spec_path=Path("services/user-service/specs/head/openapi.yaml"),
    )
    print(json.dumps([change.model_dump() for change in changes], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

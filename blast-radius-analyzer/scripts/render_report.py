from pathlib import Path

from app.services.contract_service import analyze_openapi_contract
from app.services.report_service import build_and_save_report


def main() -> int:
    """Generate and save a sample markdown report."""
    changes = analyze_openapi_contract(
        service_name="user-service",
        file_path="specs/openapi.yaml",
        base_spec_path=Path("services/user-service/specs/base/openapi.yaml"),
        head_spec_path=Path("services/user-service/specs/head/openapi.yaml"),
    )
    report, path = build_and_save_report("user-service", changes)
    print(path.as_posix())
    print()
    print(report.markdown)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

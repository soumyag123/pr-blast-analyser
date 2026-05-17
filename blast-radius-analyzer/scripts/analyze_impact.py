import json
from pathlib import Path

from app.analyzers.impact_analyzer import analyze_impact
from app.services.code_scanner_service import scan_service_for_change
from app.services.contract_service import analyze_openapi_contract
from app.services.dependency_service import find_candidate_consumers
from app.services.report_service import build_and_save_report


def main() -> int:
    """Analyze downstream impact for the sample contract change."""
    changes = analyze_openapi_contract(
        service_name="user-service",
        file_path="specs/openapi.yaml",
        base_spec_path=Path("services/user-service/specs/base/openapi.yaml"),
        head_spec_path=Path("services/user-service/specs/head/openapi.yaml"),
    )

    findings = []
    for change in changes:
        candidates = find_candidate_consumers(change)
        for candidate in candidates:
            if candidate.service_name == "shared-docs":
                continue
            service_root = Path("services") / candidate.service_name
            evidence = scan_service_for_change(service_root, candidate.service_name, change)
            findings.append(analyze_impact(change, candidate.service_name, evidence))

    report, path = build_and_save_report("user-service", changes, findings)
    print(json.dumps([finding.model_dump() for finding in findings], indent=2))
    print()
    print(path.as_posix())
    print()
    print(report.markdown)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

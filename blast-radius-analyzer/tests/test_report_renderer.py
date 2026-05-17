from pathlib import Path

from app.analyzers.impact_analyzer import analyze_impact
from app.services.code_scanner_service import scan_service_for_change
from app.services.contract_service import analyze_openapi_contract
from app.services.report_service import build_and_save_report


def test_build_and_save_report_creates_markdown_file() -> None:
    """Verify report generation saves markdown output."""
    changes = analyze_openapi_contract(
        service_name="user-service",
        file_path="specs/openapi.yaml",
        base_spec_path=Path("services/user-service/specs/base/openapi.yaml"),
        head_spec_path=Path("services/user-service/specs/head/openapi.yaml"),
    )

    target_change = next(change for change in changes if change.field_path == "user_id")
    evidence = scan_service_for_change(
        Path("services/notification-service"),
        "notification-service",
        target_change,
    )
    findings = [analyze_impact(target_change, "notification-service", evidence)]

    report, path = build_and_save_report("user-service", changes, findings)

    assert report.service_name == "user-service"
    assert "Detected 2 breaking contract change(s)" in report.summary
    assert path.exists()
    assert "# Blast Radius Report" in path.read_text(encoding="utf-8")
    assert "## Impact Findings" in path.read_text(encoding="utf-8")

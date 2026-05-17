from app.agents.workflow import run_blast_radius_analysis


def test_run_blast_radius_analysis_returns_report_and_findings() -> None:
    """Verify the full workflow returns a report and findings."""
    report, findings, report_path = run_blast_radius_analysis()

    assert report.service_name == "user-service"
    assert report.changes
    assert findings
    assert report_path.endswith(".md")
    assert any(finding.service_name == "notification-service" for finding in findings)

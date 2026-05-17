import json

from app.agents.workflow import run_blast_radius_analysis


def main() -> int:
    """Run the full local analysis workflow and print the result."""
    report, findings, report_path = run_blast_radius_analysis()
    payload = {
        "service_name": report.service_name,
        "summary": report.summary,
        "report_path": report_path,
        "changes": [change.model_dump() for change in report.changes],
        "findings": [finding.model_dump() for finding in findings],
        "markdown": report.markdown,
    }
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

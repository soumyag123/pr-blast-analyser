from fastapi import APIRouter

from app.agents.workflow import run_blast_radius_analysis

router = APIRouter(prefix="/analyze", tags=["analyze"])


@router.post("")
def analyze() -> dict[str, object]:
    """Run the local blast radius analysis."""
    report, findings, report_path = run_blast_radius_analysis()
    return {
        "service_name": report.service_name,
        "summary": report.summary,
        "report_path": report_path,
        "changes": [change.model_dump() for change in report.changes],
        "findings": [finding.model_dump() for finding in findings],
        "markdown": report.markdown,
    }

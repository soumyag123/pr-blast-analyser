from pathlib import Path

from app.domain.findings import ImpactFinding
from app.domain.report import AnalysisReport
from app.renderers.markdown import render_contract_report
from app.repositories.report_repository import save_report


def build_and_save_report(
    service_name: str,
    changes: list,
    findings: list[ImpactFinding],
) -> tuple[AnalysisReport, Path]:
    """Build and save a contract analysis report."""
    report = render_contract_report(service_name, changes, findings)
    path = save_report(report)
    return report, path

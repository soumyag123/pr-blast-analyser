from typing import TypedDict

from app.domain.contracts import ContractChange
from app.domain.findings import ImpactFinding
from app.domain.report import AnalysisReport


class AnalysisState(TypedDict, total=False):
    changes: list[ContractChange]
    findings: list[ImpactFinding]
    report: AnalysisReport
    report_path: str

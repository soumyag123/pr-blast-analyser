from pydantic import BaseModel

from app.domain.contracts import ContractChange
from app.domain.findings import ImpactFinding


class AnalysisReport(BaseModel):
    service_name: str
    summary: str
    changes: list[ContractChange]
    findings: list[ImpactFinding]
    markdown: str

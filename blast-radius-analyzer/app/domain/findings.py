from pydantic import BaseModel

from app.domain.contracts import ContractChange
from app.domain.dependencies import CodeEvidence


class ImpactFinding(BaseModel):
    service_name: str
    severity: str
    confidence: str
    summary: str
    change: ContractChange
    evidence: list[CodeEvidence]

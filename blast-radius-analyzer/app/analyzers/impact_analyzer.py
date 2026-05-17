from app.domain.contracts import ContractChange
from app.domain.dependencies import CodeEvidence
from app.domain.findings import ImpactFinding


def classify_severity(change: ContractChange, evidence: list[CodeEvidence]) -> str:
    """Classify impact severity from contract change evidence."""
    if not evidence:
        return "low"
    if change.change_type == "field_removed":
        return "high"
    if change.change_type == "field_type_changed":
        return "medium"
    return "low"


def classify_confidence(evidence: list[CodeEvidence]) -> str:
    """Classify confidence from evidence strength."""
    for item in evidence:
        if item.file_path.endswith(".py"):
            return "high"
    if evidence:
        return "medium"
    return "low"


def build_summary(change: ContractChange, service_name: str, evidence: list[CodeEvidence]) -> str:
    """Build a readable summary for an impact finding."""
    if evidence:
        return (
            f"{service_name} appears to depend on {change.method} {change.endpoint} "
            f"and references {change.field_path}, so this {change.change_type} may break it."
        )
    return (
        f"{service_name} may depend on {change.method} {change.endpoint}, "
        f"but only weak evidence was found for {change.field_path}."
    )


def analyze_impact(
    change: ContractChange,
    service_name: str,
    evidence: list[CodeEvidence],
) -> ImpactFinding:
    """Create an impact finding from a change and evidence."""
    return ImpactFinding(
        service_name=service_name,
        severity=classify_severity(change, evidence),
        confidence=classify_confidence(evidence),
        summary=build_summary(change, service_name, evidence),
        change=change,
        evidence=evidence,
    )

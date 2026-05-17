from app.domain.contracts import ContractChange
from app.domain.findings import ImpactFinding
from app.domain.report import AnalysisReport


def render_contract_report(
    service_name: str,
    changes: list[ContractChange],
    findings: list[ImpactFinding],
) -> AnalysisReport:
    """Render a markdown contract analysis report."""
    summary = (
        f"Detected {len(changes)} breaking contract change(s) in {service_name} "
        f"with {len(findings)} downstream impact finding(s)."
    )
    lines = [
        "# Blast Radius Report",
        "",
        "## Summary",
        "",
        summary,
        "",
        "## Contract Changes",
        "",
    ]

    for change in changes:
        lines.extend(
            [
                f"- `{change.method} {change.endpoint}`",
                f"  - Change type: `{change.change_type}`",
                f"  - Field: `{change.field_path}`",
                f"  - Breaking: `{str(change.breaking).lower()}`",
            ]
        )

    lines.extend(["", "## Impact Findings", ""])

    if not findings:
        lines.append("- No downstream findings were generated.")
    else:
        for finding in findings:
            lines.extend(
                [
                    f"- Service: `{finding.service_name}`",
                    f"  - Severity: `{finding.severity}`",
                    f"  - Confidence: `{finding.confidence}`",
                    f"  - Summary: {finding.summary}",
                ]
            )
            if finding.evidence:
                for item in finding.evidence:
                    lines.extend(
                        [
                            f"  - Evidence: `{item.file_path}:{item.line_start}-{item.line_end}`",
                            f"    - Snippet: `{item.snippet.replace(chr(10), ' ')}`",
                        ]
                    )

    markdown = "\n".join(lines)
    return AnalysisReport(
        service_name=service_name,
        summary=summary,
        changes=changes,
        findings=findings,
        markdown=markdown,
    )

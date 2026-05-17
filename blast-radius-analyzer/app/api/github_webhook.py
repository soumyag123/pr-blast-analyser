from fastapi import APIRouter, HTTPException

from app.agents.workflow import run_blast_radius_analysis
from app.schemas.github_webhook import GitHubPullRequestEvent
from app.services.github_webhook_service import map_github_event

router = APIRouter(prefix="/webhooks/github", tags=["github"])


@router.post("")
def github_pull_request_webhook(payload: GitHubPullRequestEvent) -> dict[str, object]:
    """Handle a GitHub pull request webhook."""
    if payload.action not in {"opened", "synchronize", "reopened"}:
        return {"accepted": False, "reason": f"Unsupported action: {payload.action}"}

    event = map_github_event(payload)
    if not event.repository.root_path.exists():
        raise HTTPException(status_code=404, detail="Mapped local repository path does not exist")

    report, findings, report_path = run_blast_radius_analysis()
    return {
        "accepted": True,
        "event": event.model_dump(mode="json"),
        "report_path": report_path,
        "summary": report.summary,
        "findings": [finding.model_dump() for finding in findings],
    }

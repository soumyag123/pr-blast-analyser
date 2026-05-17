from pathlib import Path

from app.domain.events import PullRequestEvent, PullRequestRef, PullRequestRepository
from app.schemas.github_webhook import GitHubPullRequestEvent


def map_github_event(payload: GitHubPullRequestEvent) -> PullRequestEvent:
    """Map a GitHub webhook payload into the internal event model."""
    return PullRequestEvent(
        event_id=f"github-pr-{payload.repository.name}-{payload.pull_request.number}",
        event_name="pull_request",
        action=payload.action,
        pr_number=payload.pull_request.number,
        repository=PullRequestRepository(
            name=payload.repository.name,
            full_name=payload.repository.full_name,
            root_path=Path("services") / payload.repository.name,
        ),
        base=PullRequestRef(
            ref=payload.pull_request.base.ref,
            sha=payload.pull_request.base.sha,
        ),
        head=PullRequestRef(
            ref=payload.pull_request.head.ref,
            sha=payload.pull_request.head.sha,
        ),
    )

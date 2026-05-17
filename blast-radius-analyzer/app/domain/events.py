from pathlib import Path

from pydantic import BaseModel, Field


class PullRequestRef(BaseModel):
    ref: str
    sha: str | None = None


class PullRequestRepository(BaseModel):
    name: str
    full_name: str
    root_path: Path


class PullRequestEvent(BaseModel):
    event_id: str = Field(min_length=1)
    event_name: str = Field(default="pull_request")
    action: str
    pr_number: int
    repository: PullRequestRepository
    base: PullRequestRef
    head: PullRequestRef

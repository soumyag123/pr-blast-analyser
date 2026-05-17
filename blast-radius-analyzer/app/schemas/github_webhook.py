from pydantic import BaseModel


class GitHubRepositoryOwner(BaseModel):
    login: str


class GitHubRepository(BaseModel):
    name: str
    full_name: str
    owner: GitHubRepositoryOwner


class GitHubPullRequestBranch(BaseModel):
    ref: str
    sha: str


class GitHubPullRequest(BaseModel):
    number: int
    head: GitHubPullRequestBranch
    base: GitHubPullRequestBranch


class GitHubPullRequestEvent(BaseModel):
    action: str
    repository: GitHubRepository
    pull_request: GitHubPullRequest

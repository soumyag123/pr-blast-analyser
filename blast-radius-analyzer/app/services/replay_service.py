import json
from pathlib import Path

from app.domain.events import PullRequestEvent


def load_replay_event(event_path: Path) -> PullRequestEvent:
    """Load a replay event from disk."""
    payload = json.loads(event_path.read_text(encoding="utf-8"))
    return PullRequestEvent.model_validate(payload)

from fastapi import APIRouter, HTTPException

from app.schemas.replay import ReplayRequest
from app.services.replay_service import load_replay_event

router = APIRouter(prefix="/replay", tags=["replay"])


@router.post("/pr")
def replay_pull_request(request: ReplayRequest) -> dict[str, object]:
    """Replay a pull request event from a local file."""
    if not request.event_path.exists():
        raise HTTPException(status_code=404, detail="Replay event file not found")
    event = load_replay_event(request.event_path)
    return {
        "event_id": event.event_id,
        "event_name": event.event_name,
        "action": event.action,
        "pr_number": event.pr_number,
        "repository": event.repository.model_dump(mode="json"),
        "base": event.base.model_dump(),
        "head": event.head.model_dump(),
    }

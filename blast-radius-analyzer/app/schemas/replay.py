from pathlib import Path

from pydantic import BaseModel, Field


class ReplayRequest(BaseModel):
    event_path: Path = Field(default=Path("data/sample_events/pr_opened.json"))

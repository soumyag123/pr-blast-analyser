from pydantic import BaseModel


class RetrievalHit(BaseModel):
    service_name: str
    source_path: str
    content: str
    score: float

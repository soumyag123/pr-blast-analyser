from pydantic import BaseModel


class CandidateConsumer(BaseModel):
    service_name: str
    source_path: str
    reason: str
    score: float


class CodeEvidence(BaseModel):
    service_name: str
    file_path: str
    line_start: int
    line_end: int
    snippet: str
    matched_terms: list[str]

from pydantic import BaseModel


class ContractChange(BaseModel):
    service_name: str
    file_path: str
    method: str
    endpoint: str
    change_type: str
    field_path: str
    breaking: bool

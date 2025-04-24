from pydantic import BaseModel, validator
from typing import Dict, Any

class TicketBase(BaseModel):
    @classmethod
    def get_fields(cls) -> Dict[str, str]:
        return {
            "status_code": "INTEGER NOT NULL",
            "ID": "TEXT PRIMARY KEY"
        }

class TicketCreate(TicketBase):
    status_code: int
    ID: str

    @validator('status_code')
    def validate_status(cls, v):
        if v not in (1, 2, 3):
            raise ValueError("Status code must be 1, 2 or 3")
        return v

    def to_dict(self) -> Dict[str, Any]:
        return self.dict()

class TicketOut(TicketCreate):
    @classmethod
    def get_empty_instance(cls):
        return cls(status_code=0, ID="")
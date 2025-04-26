from pydantic import BaseModel
from typing import Dict, Any
from src.backend.app.logic.ticket import Ticket

class IncidenceBase(BaseModel):
    @classmethod
    def get_fields(cls) -> Dict[str, str]:
        return {
            "incidence_id": "INTEGER PRIMARY KEY",
            "description": "TEXT NOT NULL",
            "type": "TEXT NOT NULL",
            "status": "TEXT NOT NULL"
        }

class IncidenceCreate(IncidenceBase):
    description: str
    type: str
    status: str
    incidence_id: int | None = None

    def to_dict(self) -> Dict[str, Any]:
        return self.dict()

class IncidenceOut(IncidenceCreate):
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
    
    @classmethod
    def get_empty_instance(cls):
        return cls(description="", type="", status="", incidence_id=0)
from typing import Optional
from pydantic import BaseModel

class TicketCreate(BaseModel):
    __entity_name__ = "ticket"
    ticket_id: int
    status_code: int

    def to_dict(self):
        return self.model_dump()

    @classmethod
    def get_fields(cls):
        return {
            "ticket_id": "INTEGER PRIMARY KEY",
            "status_code": "INTEGER"
        }

class TicketOut(TicketCreate):
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
"""from typing import Optional
from pydantic import BaseModel

class Incidence(BaseModel):
    __entity_name__ = "incidence"
    incidence_id: Optional[int] = None
    description: str
    status: str  # Relacionado con Ticket
    type: str

    def to_dict(self):
        return self.model_dump()

    @classmethod
    def get_fields(cls):
        return {
            "incidence_id": "INTEGER PRIMARY KEY",
            "description": "TEXT NOT NULL",
            "status": "TEXT NOT NULL",
            "type": "TEXT"
        }"""
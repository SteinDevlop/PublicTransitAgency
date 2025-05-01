from typing import Optional
from pydantic import BaseModel

class Transport(BaseModel):
    __entity_name__ = "transport_unit"
    id: str
    type: str
    status: str
    ubication: str
    capacity: int

    def to_dict(self):
        return self.model_dump()

    @classmethod
    def get_fields(cls):
        return {
            "id": "TEXT PRIMARY KEY",
            "type": "TEXT",
            "status": "TEXT",
            "ubication": "TEXT",
            "capacity": "INTEGER"
        }
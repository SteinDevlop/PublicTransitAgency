from typing import Optional
from pydantic import BaseModel

class TransportUnitCreate(BaseModel):
    __entity_name__ = "unit_transport"
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

class TransportUnitOut(TransportUnitCreate):
    __entity_name__ = "unit_transport"
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
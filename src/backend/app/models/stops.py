from typing import Optional, Dict
from pydantic import BaseModel

class StopCreate(BaseModel):
    __entity_name__ = "stops"
    stop_id: int
    stop_data: Dict[str, str]

    def to_dict(self):
        return self.model_dump()

    @classmethod
    def get_fields(cls):
        return {
            "stop_id": "INTEGER PRIMARY KEY",
            "stop_data": "TEXT"  # Guardaremos stop_data como JSON serializado
        }

class StopOut(StopCreate):
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
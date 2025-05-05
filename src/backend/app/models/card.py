from typing import Optional
from pydantic import BaseModel

class CardCreate(BaseModel):
    __entity_name__ = "tarjeta"
    id: Optional[int] = None
    type: Optional[str] = None
    balance: Optional[float] = None

    def to_dict(self):
        return self.model_dump()

    @classmethod
    def get_fields(cls):
        return {
            "id": "INTEGER PRIMARY KEY",
            "tipo": "TEXT",
            "balance": "REAL"
        }

class CardOut(CardCreate):
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

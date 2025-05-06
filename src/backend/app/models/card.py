from typing import Optional
from pydantic import BaseModel

class CardCreate(BaseModel):
    __entity_name__ = "tarjeta"
    id: Optional[int] = None
    iduser: Optional[int] = None
    idtype: Optional[int] = None
    balance: Optional[int] = None

    def to_dict(self):
        return self.model_dump()

    @classmethod
    def get_fields(cls)-> dict:
        return {
            "id": "INTEGER PRIMARY KEY",       # ID como clave primaria
            "iduser": "INTEGER",            # iduser como entero
            "idtype": "INTEGER",        # idtype como entero
            "balance": "INTEGER"                   # balance como número decimal (REAL)
        }

class CardOut(CardCreate):
    __entity_name__ = "tarjeta"
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

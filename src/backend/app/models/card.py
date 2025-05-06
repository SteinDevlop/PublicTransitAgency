from typing import Optional
from pydantic import BaseModel

class CardCreate(BaseModel):
    __entity_name__ = "tarjeta"
    id: Optional[int] = None
    idusuario: Optional[int] = None
    idtipotarjeta: Optional[int] = None
    saldo: Optional[int] = None

    def to_dict(self):
        return self.model_dump()

    @classmethod
    def get_fields(cls)-> dict:
        return {
            "id": "INTEGER PRIMARY KEY",       # ID como clave primaria
            "idusuario": "INTEGER",            # idusuario como entero
            "idtipotarjeta": "INTEGER",        # idtipotarjeta como entero
            "saldo": "INTEGER"                   # saldo como número decimal (REAL)
        }

class CardOut(CardCreate):
    __entity_name__ = "tarjeta"
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

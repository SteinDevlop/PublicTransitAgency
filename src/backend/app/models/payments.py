from typing import Optional
from pydantic import BaseModel

class Payment(BaseModel):
    """
    Modelo para la tabla Pago en SQL Server.
    """
    __entity_name__ = "Pago"

    IDMovimiento: int
    IDPrecio: int
    IDTarjeta: int
    IDUnidad: str = "EMPTY"
    ID: int

    def to_dict(self):
        return self.dict()
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

    @classmethod
    def get_fields(cls):
        return {
            "IDMovimiento": "INTEGER NOT NULL",
            "IDPrecio": "INTEGER NOT NULL",
            "IDTarjeta": "INTEGER NOT NULL",
            "IDUnidad": "VARCHAR(20) NOT NULL DEFAULT 'EMPTY'",
            "ID": "INTEGER NOT NULL"
        }
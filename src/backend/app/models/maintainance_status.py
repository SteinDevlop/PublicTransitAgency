from typing import Optional
from pydantic import BaseModel


class MaintainanceStatus(BaseModel):
    __entity_name__ = "status_mantenimiento"

    id: Optional[int] = None
    type: Optional[str] = None  # Campo añadido
    status: Optional[str] = None  # Campo añadido

    def to_dict(self):
        return self.dict()

    @classmethod
    def from_dict(cls, data: dict):
        """
        Crea una instancia de MaintainanceStatus a partir de un diccionario.
        """
        return cls(**data)

    @classmethod
    def get_fields(cls):
        return {
            "id": "INTEGER PRIMARY KEY",
            "type": "VARCHAR NOT NULL",
            "status": "VARCHAR NOT NULL"
        }
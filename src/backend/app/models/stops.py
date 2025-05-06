from typing import Optional
from pydantic import BaseModel


class Parada(BaseModel):
    __entity_name__ = "parada"  # Nombre de la tabla en la base de datos

    id: Optional[int] = None  # Clave primaria ID
    name: str  # Nombre de la parada
    ubication: str  # Ubicación de la parada

    def to_dict(self):
        """
        Serializa el modelo `Parada` en un diccionario.
        """
        return self.dict()

    @classmethod
    def from_dict(cls, data: dict):
        """
        Crea una instancia de `Parada` a partir de un diccionario.
        """
        return cls(**data)

    @classmethod
    def get_fields(cls):
        """
        Define los campos de la tabla para su creación.
        """
        return {
            "id": "INT PRIMARY KEY",
            "name": "VARCHAR NOT NULL",
            "ubication": "VARCHAR NOT NULL"
        }
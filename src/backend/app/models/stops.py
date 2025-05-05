from typing import Optional
from pydantic import BaseModel

class Stop(BaseModel):
    __entity_name__ = "parada"  # Nombre de la tabla en la base de datos
    id: Optional[int] = None  # Clave primaria
    name: Optional[str] = None  # Nombre de la parada
    ubication: Optional[str] = None  # Ubicación de la parada

    def to_dict(self):
        return self.model_dump()

    @classmethod
    def get_fields(cls):
        return {
            "id": "INTEGER PRIMARY KEY",
            "nombre": "VARCHAR(100) NOT NULL",
            "ubicacion": "VARCHAR(150) NOT NULL"
        }
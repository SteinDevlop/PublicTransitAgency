from typing import Optional
from pydantic import BaseModel

class Stop(BaseModel):
    __entity_name__ = "Parada"  # Nombre de la tabla en la base de datos
    ID: Optional[int] = None  # Clave primaria
    Nombre: Optional[str] = None  # Nombre de la parada
    Ubicacion: Optional[str] = None  # Ubicación de la parada

    def to_dict(self):
        return self.model_dump()

    @classmethod
    def get_fields(cls):
        return {
            "ID": "INTEGER PRIMARY KEY",
            "Nombre": "VARCHAR(100) NOT NULL",
            "Ubicacion": "VARCHAR(150) NOT NULL"
        }
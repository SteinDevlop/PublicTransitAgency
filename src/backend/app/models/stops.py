from typing import Optional
from pydantic import BaseModel, Field

class Stop(BaseModel):
    __entity_name__ = "parada"  # Nombre de la tabla en la base de datos
    id: Optional[int] = Field(None, description="Clave primaria")
    nombre: str = Field(..., max_length=100, description="Nombre de la parada")
    ubicacion: str = Field(..., max_length=150, description="Ubicación de la parada")

    def to_dict(self):
        return self.model_dump()

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

    @classmethod
    def get_fields(cls):
        return {
            "id": "INTEGER PRIMARY KEY",
            "nombre": "VARCHAR(100) NOT NULL",
            "ubicacion": "VARCHAR(150) NOT NULL"
        }
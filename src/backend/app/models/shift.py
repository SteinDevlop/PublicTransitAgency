from typing import Optional
from pydantic import BaseModel, Field

class Shift(BaseModel):
    __entity_name__ = "turno"  # Nombre de la tabla en la base de datos
    id: Optional[int] = Field(None, description="Clave primaria")
    tipoturno: str = Field(..., max_length=30, description="Tipo de turno (por ejemplo, 'Diurno', 'Nocturno')")

    def to_dict(self):
        return self.model_dump()

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

    @classmethod
    def get_fields(cls):
        return {
            "id": "INTEGER PRIMARY KEY",
            "tipoturno": "VARCHAR(30) NOT NULL"
        }
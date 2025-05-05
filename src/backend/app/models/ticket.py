from typing import Optional
from pydantic import BaseModel, Field

class Ticket(BaseModel):
    __entity_name__ = "ticket"  # Nombre de la tabla en la base de datos
    id: Optional[int] = Field(None, description="Clave primaria")
    estadoincidencia: str = Field(..., max_length=20, description="Estado de la incidencia")

    def to_dict(self):
        return self.model_dump()

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

    @classmethod
    def get_fields(cls):
        return {
            "id": "INTEGER PRIMARY KEY",
            "estadoincidencia": "VARCHAR(20) NOT NULL"
        }
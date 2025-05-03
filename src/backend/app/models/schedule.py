from typing import Optional
from pydantic import BaseModel

class Schedule(BaseModel):
    __entity_name__ = "Horario"
    ID: Optional[int] = None  # Clave primaria
    Llegada: Optional[str] = None  # Hora de llegada (opcional)
    Salida: Optional[str] = None  # Hora de salida (opcional)

    def to_dict(self):
        return self.model_dump()

    @classmethod
    def get_fields(cls):
        return {
            "ID": "INTEGER PRIMARY KEY",
            "Llegada": "TIME NOT NULL",
            "Salida": "TIME NOT NULL"
        }
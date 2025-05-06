from typing import Optional
from pydantic import BaseModel

class Schedule(BaseModel):
    __entity_name__ = "horario"  # Nombre de la tabla en la base de datos
    id: Optional[int] = None
    llegada: Optional[str] = None  # Hora de llegada (tipo TIME)
    salida: Optional[str] = None  # Hora de salida (tipo TIME)

    def to_dict(self):
        return self.dict()

    @classmethod
    def get_fields(cls):
        return {
            "id": "INTEGER PRIMARY KEY",
            "llegada": "TIME NOT NULL",
            "salida": "TIME NOT NULL"
        }
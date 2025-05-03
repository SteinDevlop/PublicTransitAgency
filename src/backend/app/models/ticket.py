from typing import Optional
from pydantic import BaseModel

class Ticket(BaseModel):
    __entity_name__ = "Ticket"  # Nombre de la tabla en la base de datos
    id: Optional[int] = None  # Clave primaria en minúsculas para el controlador
    EstadoIncidencia: str = None # Estado de incidencia (por ejemplo, "Abierto", "Cerrado", "En Proceso")

    @classmethod
    def get_fields(cls):
        # Define los campos de la tabla con `ID` en mayúsculas
        return {
            "ID": "INTEGER PRIMARY KEY",
            "EstadoIncidencia": "VARCHAR(20) NOT NULL"
        }
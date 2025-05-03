from typing import Optional
from pydantic import BaseModel

class Incidence(BaseModel):
    __entity_name__ = "Incidencia"  # Nombre de la tabla en la base de datos
    ID: Optional[int] = None  # Clave primaria
    IDTicket: int  # Clave foránea a Ticket(ID)
    Descripcion: str
    Tipo: str
    IDUnidad: int  # Columna adicional en la tabla

    def to_dict(self):
        return self.model_dump()

    @classmethod
    def get_fields(cls):
        return {
            "ID": "INTEGER PRIMARY KEY",
            "IDTicket": "INTEGER NOT NULL",
            "Descripcion": "VARCHAR(100) NOT NULL",
            "Tipo": "VARCHAR(20) NOT NULL",
            "IDUnidad": "INTEGER NOT NULL"
        }
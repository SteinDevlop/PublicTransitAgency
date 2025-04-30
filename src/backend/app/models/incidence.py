from typing import Optional
from pydantic import BaseModel

class IncidenceCreate(BaseModel):
    __entity_name__ = "Incidencia"
    IncidenciaID: Optional[int] = None
    Descripcion: str
    Tipo: Optional[str] = None
    TicketID: int  # Clave foránea a la tabla Ticket

    def to_dict(self):
        return self.dict(by_alias=False)

    @classmethod
    def get_fields(cls):
        return {
            "IncidenciaID": "INTEGER PRIMARY KEY",
            "Descripcion": "TEXT NOT NULL",
            "Tipo": "TEXT",
            "TicketID": "INTEGER NOT NULL"  # Clave foránea
        }

class IncidenceOut(BaseModel):
    IncidenciaID: int
    Descripcion: str
    Tipo: Optional[str] = None
    TicketID: int

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

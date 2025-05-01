<<<<<<< HEAD
=======
from typing import Optional
from pydantic import BaseModel

class IncidenceBase(BaseModel):
    Descripcion: str
    Tipo: Optional[str] = None
    TicketID: int

class IncidenceCreate(IncidenceBase):
    __entity_name__ = "Incidencia"  # Añadido el atributo __entity_name__

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


class IncidenceOut(IncidenceBase):
    IncidenciaID: int

    class Config:
        from_attributes = True 
>>>>>>> d9ce6cb (Rewind)

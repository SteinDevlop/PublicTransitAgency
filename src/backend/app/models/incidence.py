from typing import Optional
from pydantic import BaseModel
from backend.app.logic.universal_controller_sql import UniversalController

class IncidenceBase(BaseModel):
    Descripcion: str
    Tipo: Optional[str] = None
    TicketID: int

class IncidenceCreate(IncidenceBase):
    __entity_name__ = "Incidencia"  # Añadido el atributo __entity_name__

    def to_dict(self):
        return self.dict(by_alias=False)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

    @classmethod
    def get_fields(cls):
        return {
            "IncidenciaID": "INTEGER PRIMARY KEY",
            "Descripcion": "TEXT NOT NULL",
            "Tipo": "TEXT",
            "TicketID": "INTEGER NOT NULL"  # Clave foránea
        }

<<<<<<< HEAD

class IncidenceOut(IncidenceBase):
    IncidenciaID: int

    class Config:
        from_attributes = True 
=======
def inspect_tables():
    uc = UniversalController()
    uc.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = uc.cursor.fetchall()
    print("Tablas existentes:", [table["name"] for table in tables])

def setup_function():
    uc = UniversalController()
    uc.clear_tables()
    uc.add(Incidence(
        incidence_id=1,
        description="Accidente",
        type="Choque",
        status="Abierto"
    ))
>>>>>>> 93460d8 (incidence fix)

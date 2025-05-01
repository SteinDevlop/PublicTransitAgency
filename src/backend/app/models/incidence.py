from typing import Optional
from pydantic import BaseModel
from backend.app.logic.universal_controller_sql import UniversalController

class Incidence(BaseModel):
    __entity_name__ = "incidence"
    incidence_id: Optional[int] = None
    description: str
    type: str
    status: str

    def to_dict(self):
        return self.model_dump()

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

    @classmethod
    def get_fields(cls):
        return {
            "incidence_id": "INTEGER PRIMARY KEY",
            "description": "TEXT",
            "type": "TEXT",
            "status": "TEXT"
        }

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

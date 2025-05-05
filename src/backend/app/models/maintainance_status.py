from typing import Optional
from pydantic import BaseModel

class MaintainanceState(BaseModel):
    __entity_name__ = "estadomantenimiento"  # Nombre de la tabla usada en la base de datos
    id: Optional[int] = None
    tipoestado: str

    def to_dict(self):
        return self.dict()

    @classmethod
    def get_fields(cls):
        return {
            "id": "INTEGER PRIMARY KEY",
            "tipoestado": "VARCHAR(100) NOT NULL"
        }
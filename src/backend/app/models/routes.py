from typing import Optional
from pydantic import BaseModel

class Route(BaseModel):
    __entity_name__ = "ruta"  # Nombre de la tabla en la base de datos
    id: Optional[int] = None  # Clave primaria
    idHorario: Optional[int] = None  # Clave foránea a la tabla Horario (opcional)
    name: Optional[str] = None  # Nombre de la ruta (opcional)

    def to_dict(self):
        return self.model_dump()

    @classmethod
    def get_fields(cls):
        return {
            "ID": "INTEGER PRIMARY KEY",
            "IDHorario": "INTEGER NOT NULL",
            "Nombre": "VARCHAR(100) NOT NULL"
        }
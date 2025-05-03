from typing import Optional
from pydantic import BaseModel

class Ticket(BaseModel):
    __entity_name__ = "Ticket"  # Nombre de la tabla en la base de datos
    ticket_id: Optional[int] = None  # Clave primaria
    status_code: int = None # Código de estado del ticket (1, 2 o 3)

    def to_dict(self):
        return self.model_dump()

    @classmethod
    def get_fields(cls):
        return {
            "ticket_id": "INTEGER PRIMARY KEY",
            "status_code": "INTEGER NOT NULL"
        }

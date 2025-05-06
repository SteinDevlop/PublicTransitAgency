from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class MaintenanceCreate(BaseModel):
    __entity_name__ = "mantenimiento"
    
    id: Optional[int] = None
    idestado: Optional[int] = None
    tipo: Optional[str] = None
    fecha: Optional[datetime] = None
    idunidadtransporte: Optional[int] = None
    
    def to_dict(self):
        """Convierte el objeto a un diccionario"""
        return self.model_dump()

    @classmethod
    def get_fields(cls):
        """Devuelve los campos de la tabla como un diccionario con los tipos de datos"""
        return {
            "id": "INTEGER PRIMARY KEY",       # ID de la entidad, clave primaria
            "idestado":"INTEGER",                # ID del estado (entero)
            "tipo": "varchar(100)",                    # Tipo de mantenimiento (cadena de texto)
            "fecha": "DATE",                    # Fecha del mantenimiento (tipo DATE)
            "idunidadtransporte": "INTEGER",              # ID de la unidad asociada (entero)
        }
class MaintenanceOut(MaintenanceCreate):
    __entity_name__ = "mantenimiento"
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
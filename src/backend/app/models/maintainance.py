from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class MaintenanceCreate(BaseModel):
    __entity_name__ = "maintenance"
    
    id: Optional[int] = None
    type: Optional[str] = None
    date: Optional[datetime] = None
    id_unit: Optional[int] = None
    id_status: Optional[int] = None
    
    def to_dict(self):
        """Convierte el objeto a un diccionario"""
        return self.__dict__  # Devuelve los atributos como un diccionario

    @classmethod
    def get_fields(cls):
        """Devuelve los campos de la tabla como un diccionario con los tipos de datos"""
        return {
            "id": "INTEGER PRIMARY KEY",       # ID de la entidad, clave primaria
            "type": "TEXT",                    # Tipo de mantenimiento (cadena de texto)
            "date": "DATE",                    # Fecha del mantenimiento (tipo DATE)
            "id_unit": "INTEGER",              # ID de la unidad asociada (entero)
            "id_status": "INTEGER"             # ID de estado del mantenimiento (entero)
        }
class MaintenanceOut(MaintenanceCreate):
    __entity_name__ = "maintenance"
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
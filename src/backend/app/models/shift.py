from typing import Optional
from pydantic import BaseModel

class Shift(BaseModel):
    __entity_name__ = "Turno"  # Nombre de la tabla en la base de datos
    ID: Optional[int] = None  # Clave primaria
    TipoTurno: Optional [str]  = None # Tipo de turno (por ejemplo, "Diurno", "Nocturno")

    def to_dict(self):
        return self.model_dump()

    @classmethod
    def get_fields(cls):
        return {
            "ID": "INTEGER PRIMARY KEY",
            "TipoTurno": "VARCHAR(30) NOT NULL"
        }
    
"""
La tabla SQL no es compatible con este modelo (no se por cual nos vamos a seguir pero voy a implementar el modelo que uso rubiano)
import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel

class ShiftBase(BaseModel):
    __entity_name__ = "Turnos" #Agrega el atributo
    shift_id: Optional[str] = None
    unit_id: Optional[str] = None  # Foreign key to Transport
    start_time: Optional[datetime.datetime] = None
    end_time: Optional[datetime.datetime] = None
    driver_id: Optional[str] = None  # Foreign key to Worker (as string for simplicity)
    schedule_id: Optional[str] = None  # Foreign key to Schedule

    def to_dict(self) -> Dict[str, Any]:
        return self.dict()

    @classmethod
    def get_fields(cls) -> Dict[str, str]:
        return {
            "shift_id": "TEXT PRIMARY KEY",
            "unit_id": "TEXT NOT NULL",
            "start_time": "DATETIME NOT NULL",
            "end_time": "DATETIME NOT NULL",
            "driver_id": "TEXT NOT NULL",
            "schedule_id": "TEXT NOT NULL"
            # Define foreign key relationships in your database schema
        }

class ShiftCreate(ShiftBase):
    __entity_name__ = "Turnos" #Agrega el atributo
    shift_id: Optional[str] = None
    unit_id: Optional[str] = None  # Foreign key to Transport
    start_time: Optional[datetime.datetime] = None
    end_time: Optional[datetime.datetime] = None
    driver_id: Optional[str] = None  # Foreign key to Worker (as string for simplicity)
    schedule_id: Optional[str] = None  # Foreign key to Schedule

class ShiftOut(ShiftBase):
    __entity_name__ = "Turnos"
    class Config:
        from_attributes = True

    def to_dict(self):
        return self.model_dump()

    @classmethod
    def get_empty_instance(cls) -> 'ShiftOut':
        return cls(shift_id="", unit_id="", start_time=datetime.datetime.now(), end_time=datetime.datetime.now(), driver_id="", schedule_id="")
"""
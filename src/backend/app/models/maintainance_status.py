from typing import Optional
from pydantic import BaseModel, validator

class MaintainanceStatusBase(BaseModel):
    """Clase base para los estados de mantenimiento."""
    Status: str

    @validator("Status")
    def validate_status(cls, value):
        allowed_statuses = ["No hecho", "En progreso", "Hecho"]
        if value not in allowed_statuses:
            raise ValueError(f"El estado '{value}' no es válido. Los estados permitidos son: {allowed_statuses}")
        return value

class MaintainanceStatusCreate(MaintainanceStatusBase):
    """Modelo para la creación de un estado de mantenimiento."""
    __entity_name__ = "MaintainanceStatus"
    TipoEstado: str
    UnidadTransporte: str

    def to_dict(self):
        return self.dict(by_alias=False)

    @classmethod
    def get_fields(cls):
        return {
            "ID": "INTEGER PRIMARY KEY",
            "TipoEstado": "TEXT NOT NULL",
            "UnidadTransporte": "TEXT NOT NULL",
            "Status": "TEXT NOT NULL"
        }

class MaintainanceStatusOut(MaintainanceStatusBase):
    """Modelo para la salida de datos de un estado de mantenimiento."""
    ID: int
    TipoEstado: str
    UnidadTransporte: str

    class Config:
        from_attributes = True
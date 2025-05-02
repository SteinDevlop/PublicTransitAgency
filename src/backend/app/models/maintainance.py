from typing import Optional
from pydantic import BaseModel, validator

class MaintainanceStatusBase(BaseModel):
    status: str

    @validator("status")
    def validate_status(cls, value):
        allowed_statuses = ["No hecho", "En progreso", "Hecho"]
        if value not in allowed_statuses:
            raise ValueError(f"El estado '{value}' no es válido. Los estados permitidos son: {allowed_statuses}")
        return value

class MaintainanceStatusCreate(MaintainanceStatusBase):
    """Modelo para la creación de un estado de mantenimiento."""
    tipo_estado: str
    unidad_transporte: str

class MaintainanceStatusOut(MaintainanceStatusBase):
    """Modelo para la salida de datos de un estado de mantenimiento."""
    id: int
    tipo_estado: str
    unidad_transporte: str

class MaintainanceStatus(MaintainanceStatusBase):
    """Modelo principal para la lógica de negocio."""
    id: Optional[int] = None
    tipo_estado: str
    unidad_transporte: str

    def to_dict(self):
        return self.model_dump()

    @classmethod
    def get_fields(cls):
        return {
            "id": "INTEGER PRIMARY KEY",
            "tipo_estado": "TEXT NOT NULL",
            "unidad_transporte": "TEXT NOT NULL",
            "status": "TEXT NOT NULL"
        }
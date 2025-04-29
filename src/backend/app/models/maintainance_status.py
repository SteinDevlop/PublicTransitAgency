from pydantic import BaseModel, validator
from typing import Dict, Any

class MaintainanceStatusBase(BaseModel):
    @classmethod
    def get_fields(cls) -> Dict[str, str]:
        return {
            "id": "INTEGER PRIMARY KEY",
            "unit": "TEXT NOT NULL",
            "type": "TEXT NOT NULL",
            "status": "TEXT NOT NULL"
        }

from typing import Optional
from pydantic import BaseModel

class MaintainanceStatusCreate(BaseModel):
    id: int
    unit: Optional[str] = "Sin especificar"  # Valor por defecto
    type: Optional[str] = "Regular"          # Valor por defecto
    status: str

    @validator('status')
    def validate_status(cls, v):
        valid_statuses = ["activo", "en_proceso", "completado", "pendiente"]
        if v.lower() not in valid_statuses:
            raise ValueError(f"Estado debe ser uno de: {', '.join(valid_statuses)}")
        return v.lower()

    def to_dict(self) -> Dict[str, Any]:
        return self.dict()

class MaintainanceStatusOut(MaintainanceStatusCreate):
    __entity_name__ = "maintainance_status"
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
    
    @classmethod
    def get_empty_instance(cls):
        return cls(id=0, unit="", type="", status="")
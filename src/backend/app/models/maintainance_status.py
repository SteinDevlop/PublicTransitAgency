from typing import Optional
from pydantic import BaseModel, validator

class MaintainanceStatus(BaseModel):
    __entity_name__ = "maintainance_status"
    id: Optional[int] = None
    status: str

    @validator("status")
    def validate_status(cls, value):
        allowed_statuses = ["No hecho", "En progreso", "Hecho"]
        if value not in allowed_statuses:
            raise ValueError(f"El estado '{value}' no es válido. Los estados permitidos son: {allowed_statuses}")
        return value

    def to_dict(self):
        return self.model_dump()

    @classmethod
    def get_fields(cls):
        return {
            "id": "INTEGER PRIMARY KEY",
            "status": "TEXT NOT NULL"
        }
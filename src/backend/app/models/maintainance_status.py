from typing import Optional
from pydantic import BaseModel

class MaintainanceStatus(BaseModel):
    __entity_name__ = "status_mantenimiento"
    id: Optional[int] = None
    idunit: Optional[str] = None
    type: Optional[str] = None
    status: Optional[str] = None

    def to_dict(self):
        return self.model_dump()

    @classmethod
    def get_fields(cls):
        return {
            "id": "INTEGER PRIMARY KEY",
            "unit": "TEXT",
            "type": "TEXT",
            "status": "TEXT"
        }
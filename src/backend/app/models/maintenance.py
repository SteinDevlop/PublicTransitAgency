from datetime import datetime
from pydantic import BaseModel

class MaintenanceCreate(BaseModel):
    __entity_name__ =  "maintenance"
    id: int
    type: str
    date: datetime
    id_unit: int
    id_status = int
    def to_dict(self):
        return self.dict()

class MaintenanceOut(MaintenanceCreate):
    __entity_name__ = "maintenance"
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
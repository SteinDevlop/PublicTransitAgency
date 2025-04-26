from pydantic import BaseModel

class MaintenanceCreate(BaseModel):
    __entity_name__ =  "type card"
    id: int
    type: str
    def to_dict(self):
        return self.dict()

class MaintenanceOut(MaintenanceCreate):
    __entity_name__ = "type card"
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
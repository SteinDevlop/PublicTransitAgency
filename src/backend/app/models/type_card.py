from typing import Optional
from pydantic import BaseModel

class TypeCardCreate(BaseModel):
    __entity_name__ =  "typecard"
    id: Optional[int] = None
    type: Optional[str] = None
    def to_dict(self):
        return self.model_dump()
    @classmethod
    def get_fields(cls):
        return {
            "id": "INTEGER PRIMARY KEY",
            "type": "TEXT"
        }
class TypeCardOut(TypeCardCreate):
    __entity_name__ = "typecard"
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
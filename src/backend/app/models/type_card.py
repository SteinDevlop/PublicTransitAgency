from typing import Optional
from pydantic import BaseModel

class TypeCardCreate(BaseModel):
    __entity_name__ =  "tipotarjeta"
    id: Optional[int] = None
    tipo: Optional[str] = None
    def to_dict(self):
        return self.model_dump()
    @classmethod
    def get_fields(cls):
        return {
            "id": "INTEGER PRIMARY KEY",
            "tipo": "VARCHAR(20)"
        }
class TypeCardOut(TypeCardCreate):
    __entity_name__ = "tipotarjeta"
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
from pydantic import BaseModel

class TypeTransportCreate(BaseModel):
    __entity_name__ =  "typetransportunit"
    id: int
    type: str

    def to_dict(self):
        return self.model_dump()

class TypeTransportOut(TypeTransportCreate):
    __entity_name__ = "typetransportunit"
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

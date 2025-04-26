from pydantic import BaseModel

class TypeTransportCreate(BaseModel):
    __entity_name__ =  "typetransportunit"
    id: int
    tipo: str

    def to_dict(self):
        return self.dict()

class TypeTransportOut(TypeTransportCreate):
    __entity_name__ = "typetransportunit"
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

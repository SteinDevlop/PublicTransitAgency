from pydantic import BaseModel

class CardCreate(BaseModel):
    __entity_name__ =  "card"
    id: int
    tipo: str
    balance: float
    def to_dict(self):
        return self.dict()
class CardOut(CardCreate):
    __entity_name__ = "card"
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
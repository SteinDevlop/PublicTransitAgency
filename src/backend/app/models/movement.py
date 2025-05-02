from pydantic import BaseModel

class MovementCreate(BaseModel):
    __entity_name__ =  "movement"
    id: int
    type: str
    amount: float

    def to_dict(self):
        return self.model_dump()

class MovementOut(MovementCreate):
    __entity_name__ = "movement"
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

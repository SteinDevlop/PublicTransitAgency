from pydantic import BaseModel

class TypeMovementCreate(BaseModel):
    __entity_name__ = "typemovement"
    id: int
    type: str

    def to_dict(self):
        return self.model_dump()

class TypeMovementOut(TypeMovementCreate):
    __entity_name__ = "typemovement"
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

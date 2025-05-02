from pydantic import BaseModel

class PriceCreate(BaseModel):
    __entity_name__ = "price"  # <- Aquí se define el nombre general de la entidad

    id: int
    unidadtransportype: str
    amount: float

    def to_dict(self):
        return self.model_dump()

class PriceOut(PriceCreate):
    __entity_name__ = "price"  # <- También aquí, porque se usa para lectura

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

from pydantic import BaseModel

class PriceCreate(BaseModel):
    __entity_name__ = "precio"  # <- Aquí se define el nombre general de la entidad

    id: int
    unidadtransportype: int
    amount: float

    def to_dict(self):
        return self.model_dump()
    
    @classmethod
    def get_fields(cls) -> dict:
        return {
            "id": "INTEGER PRIMARY KEY",
            "unidadtransportype": "INTEGER",
            "amount": "FLOAT"
        }
class PriceOut(PriceCreate):
    __entity_name__ = "precio"  # <- También aquí, porque se usa para lectura

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

from pydantic import BaseModel

class MovementCreate(BaseModel):
    __entity_name__ =  "movimiento"  # <- Aquí se define el nombre general de la entidad
    id: int
    idtype: int
    amount: float

    def to_dict(self):
        return self.model_dump()
    
    @classmethod
    def get_fields(cls) -> dict:
        return {
            "id": "INTEGER PRIMARY KEY",
            "idtype": "INTEGER",
            "amount": "FLOAT"
        }

class MovementOut(MovementCreate):
    __entity_name__ = "movimiento"  # <- También aquí, porque se usa para lectura
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

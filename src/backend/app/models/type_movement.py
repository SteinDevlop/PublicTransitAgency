from pydantic import BaseModel

class TypeMovementCreate(BaseModel):
    __entity_name__ = "tipomovimiento"  # <- Aquí se define el nombre general de la entidad
    id: int
    type: str

    def to_dict(self):
        return self.model_dump()
    @classmethod
    def get_fields(cls) -> dict:
        return {
            "id": "INTEGER PRIMARY KEY",
            "type": "varchar(20)",
        }
class TypeMovementOut(TypeMovementCreate):
    __entity_name__ = "tipomovimiento"  # <- También aquí, porque se usa para lectura
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

from pydantic import BaseModel

class RolUserCreate(BaseModel):
    __entity_name__ =  "rolusuario"  # <- Aquí se define el nombre general de la entidad
    id: int
    type: str

    def to_dict(self):
        return self.model_dump()

    @classmethod
    def get_fields(cls) -> dict:
        return {
            "id": "INTEGER PRIMARY KEY",
            "type": "varchar(100)",
        }
class RolUserOut(RolUserCreate):
    __entity_name__ = "rolusuario"  # <- También aquí, porque se usa para lectura
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

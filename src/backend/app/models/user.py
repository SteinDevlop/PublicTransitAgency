from pydantic import BaseModel
class UserCreate(BaseModel):
    __entity_name__ = "user"  # <- Aquí se define el nombre general de la entidad
    id: int
    identification: int
    name: str
    lastname: str
    email: str
    password: str
    idtype_user: int
    idturn: int

    def to_dict(self):
        return self.dict()

class UserOut(UserCreate):
    __entity_name__ = "user"  # <- También aquí, porque se usa para lectura

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
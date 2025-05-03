from pydantic import BaseModel
class UserCreate(BaseModel):
    __entity_name__ = "usuario"  # <- Aquí se define el nombre general de la entidad
    id: int
    identification: int
    name: str
    lastname: str
    email: str
    password: str
    idtype_user: int
    idturn: int

    def to_dict(self):
        return self.model_dump()
        
    @classmethod
    def get_fields(cls) -> dict:
        return {
            "id": "SERIAL PRIMARY KEY",
            "identification": "INTEGER",
            "name": "VARCHAR(100)",
            "lastname": "VARCHAR(100)",
            "email": "VARCHAR(100)",
            "password": "VARCHAR(100)",
            "idtype_user": "INTEGER",
            "idturn": "INTEGER"
        }
class UserOut(UserCreate):
    __entity_name__ = "usuario"  # <- También aquí, porque se usa para lectura

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
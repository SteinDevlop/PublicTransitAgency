from pydantic import BaseModel
import datetime
class PQRCreate(BaseModel):
    __entity_name__ = "PQR"  # <- Aquí se define el nombre general de la entidad
    id: int
    type: str
    description: str
    fecha: str
    iduser:int
    codigogenerado:str

    def to_dict(self):
        return self.model_dump()
        
    @classmethod
    def get_fields(cls) -> dict:
        return {
            "id": "INTEGER PRIMARY KEY",
            "iduser": "INTEGER",
            "type": "VARCHAR",
            "description": "VARCHAR",
            "fecha": "DATE",
            "codigogenerado":"VARCHAR"
        }
class PQROut(PQRCreate):
    __entity_name__ = "PQR"  # <- También aquí, porque se usa para lectura

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
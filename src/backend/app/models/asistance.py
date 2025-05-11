from pydantic import BaseModel
import datetime
class AsistanceCreate(BaseModel):
    __entity_name__ = "Asistencia"  # <- Aquí se define el nombre general de la entidad
    id: int
    iduser: int  #identification user
    horainicio: datetime.time
    horafinal:datetime.time
    fecha: datetime.date

    def to_dict(self):
        return self.model_dump()
        
    @classmethod
    def get_fields(cls) -> dict:
        return {
            "id": "INTEGER PRIMARY KEY",
            "iduser": "INTEGER",
            "horainicio": "TIME",
            "horafinal": "TIME",
            "fecha": "DATE"
        }
class AsistanceOut(AsistanceCreate):
    __entity_name__ = "Asistencia"  # <- También aquí, porque se usa para lectura

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
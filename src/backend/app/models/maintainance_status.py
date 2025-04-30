from typing import Optional
from pydantic import BaseModel

class MaintainanceStatusCreate(BaseModel):
    __entity_name__ = "estatusmantenimiento"  # Importante para el UniversalController
    ID: Optional[int] = None  # Clave primaria, debe ser "ID"
    TipoEstado: str  # Renombrado para coincidir con la tabla
    UnidadTransporte: Optional[str] = None # Ahora es opcional
    Status: str # Nuevo atributo

    def to_dict(self):
        """
        Convierte el modelo a un diccionario para la interacción con la base de datos.
        """
        return self.dict(by_alias=False) # Aseguramos que los nombres de los campos coincidan

    @classmethod
    def get_fields(cls):
        """
        Define la estructura de la tabla en la base de datos.
        """
        return {
            "ID": "INTEGER PRIMARY KEY",  # Clave primaria
            "TipoEstado": "TEXT NOT NULL",
            "UnidadTransporte": "TEXT",  # Corregido: TEXT, era "REAL" incorrectamente
            "Status": "TEXT NOT NULL"
        }

class MaintainanceStatusOut(MaintainanceStatusCreate):
    """
    Modelo para la salida de datos, extiende MaintainanceStatusCreate.
    """
    @classmethod
    def from_dict(cls, data: dict):
        """
        Crea una instancia del modelo desde un diccionario.
        """
        return cls(**data)
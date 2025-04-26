from pydantic import BaseModel
from typing import Dict, Any
from src.backend.app.models.ticket import TicketOut  

class TransportBase(BaseModel):
    """Clase base con métodos esenciales"""
    __entity_name__ = "transport"
    
    @classmethod
    def get_fields(cls) -> Dict[str, str]:
        return {
            "id": "TEXT PRIMARY KEY",
            "type": "TEXT NOT NULL",
            "status": "TEXT NOT NULL",
            "ubication": "TEXT NOT NULL",
            "capacity": "INTEGER NOT NULL"
        }

    def to_dict(self) -> Dict[str, Any]:
        """Garantiza retorno como diccionario Python estándar"""
        return self.dict()

class TransportCreate(TransportBase):
    id: str
    type: str
    status: str  # Podría ser un Enum
    ubication: str
    capacity: int

    def validate_capacity(self):
        if self.capacity <= 0:
            raise ValueError("La capacidad debe ser positiva")

class TransportOut(TransportCreate):
    """Modelo para operaciones de lectura"""
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Crea instancia desde diccionario"""
        return cls(**data)

    @classmethod
    def get_empty_instance(cls):
        """Para uso con UniversalController"""
        return cls(id="", type="", status="", ubication="", capacity=0)
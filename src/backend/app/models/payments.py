from typing import Optional
from pydantic import BaseModel

class Payment(BaseModel):
    __entity_name__ = "pago"
    id: int  # Clave primaria, obligatorio
    iduser: Optional[int] = None  # Opcional
    amount: Optional[float] = None  # Opcional
    idmovement: Optional[int] = None  # Opcional
    idtransportunit: Optional[int] = None  # Opcional
    idcard: Optional[int] = None  # Opcional

    def to_dict(self):
        return self.model_dump()

    @classmethod
    def get_fields(cls):
        return {
            "id": "INTEGER PRIMARY KEY",
            "user": "TEXT",
            "payment_quantity": "REAL",
            "payment_method": "BOOLEAN",
            "vehicle_type": "INTEGER",
            "card_id": "INTEGER"
        }
    
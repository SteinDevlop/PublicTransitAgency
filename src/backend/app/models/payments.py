from typing import Optional
from pydantic import BaseModel

class Payment(BaseModel):
    __entity_name__ = "payments"
    id: int  # Clave primaria, obligatorio
    user: Optional[str] = None  # Opcional
    payment_quantity: Optional[float] = None  # Opcional
    payment_method: Optional[bool] = None  # Opcional
    vehicle_type: Optional[int] = None  # Opcional
    card_id: Optional[int] = None  # Opcional

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
    
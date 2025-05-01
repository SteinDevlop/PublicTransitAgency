from typing import Optional
from pydantic import BaseModel
import datetime

class PaymentBase(BaseModel):
    __entity_name__ = "payments"
    id: Optional[int] = None
    date: datetime.datetime
    user: str
    payment_quantity: float
    payment_method: bool
    vehicle_type: int
    card_id: Optional[int]  # Permitir que card_id sea None

    def to_dict(self):
        return self.dict()

    @classmethod
    def get_fields(cls):
        return {
            "id": "INTEGER PRIMARY KEY",
            "date": "DATETIME",
            "user": "TEXT",
            "payment_quantity": "REAL",
            "payment_method": "BOOLEAN",
            "vehicle_type": "INTEGER",
            "card_id": "INTEGER"  
        }

class PaymentCreate(PaymentBase):
    pass

class PaymentOut(PaymentBase):
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
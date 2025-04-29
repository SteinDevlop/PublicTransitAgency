from datetime import datetime
from typing import Dict, Any
from src.backend.app.models.base_model import DictModel
from models.card import Card  

class Payment(DictModel):
    id: int
    user: str
    payment_quantity: float
    payment_method: bool
    vehicle_type: int
    card: Dict[str, Any]  
    date: datetime = datetime.now()

    @classmethod
    def get_fields(cls) -> Dict[str, str]:
        return {
            "id": "INTEGER PRIMARY KEY",
            "user": "TEXT NOT NULL",
            "payment_quantity": "REAL NOT NULL",
            "payment_method": "BOOLEAN NOT NULL",
            "vehicle_type": "INTEGER NOT NULL",
            "card_id": "INTEGER NOT NULL",
            "date": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
            "FOREIGN KEY(card_id)": "REFERENCES card(id)"
        }

    def process_card(self):
        """Convierte el objeto Card a dict si es necesario"""
        if isinstance(self.card, Card):
            self.card = self.card.to_dict()
from typing import Optional, List, Union
from app.models.card import CardCreate, CardOut
from app.logic.universal_controller_sql import UniversalController

class CardService:
    def __init__(self):
        self.controller = UniversalController()

    def add(self, card: CardCreate) -> dict:
        try:
            self.controller.add(card)
            return {"message": "Tarjeta agregada correctamente"}
        except ValueError as e:
            return {"error": str(e)}

    def update(self, card: CardCreate) -> bool:
        existing = self.controller.get_by_id(CardOut, card.id)
        if not existing:
            return False
        self.controller.update(card)
        return True

    def delete(self, card_id: int) -> bool:
        existing = self.controller.get_by_id(CardOut, card_id)
        if not existing:
            return False
        self.controller.delete(existing)
        return True

    def get_all(self) -> List[CardOut]:
        data = self.controller.read_all(CardOut(id=0, tipo="", balance=0))
        return [CardOut.from_dict(d) for d in data]

    def get_by_id(self, card_id: int) -> Optional[CardOut]:
        return self.controller.get_by_id(CardOut, card_id)

    def get_all_as_dict(self) -> List[dict]:
        """Devuelve todas las tarjetas como diccionarios para plantillas HTML."""
        return self.controller.read_all(CardOut(id=0, tipo="", balance=0))

    def get_by_id_as_dict(self, card_id: int) -> Union[dict, None]:
        card = self.controller.get_by_id(CardOut, card_id)
        return card.dict() if card else None

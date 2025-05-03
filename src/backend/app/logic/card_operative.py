from backend.app.logic.card import Card
class CardOperative(Card):
    def __init__(self, card_id, card_type, card_number, expiration_date):
        super().__init__(card_id, card_type, card_number, expiration_date)
    def use_card(self):
            print(f"Card {self.id_card} used by user {self.user_id}. Remaining balance: {self.balance}")
            return True
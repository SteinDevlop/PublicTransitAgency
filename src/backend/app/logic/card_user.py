from backend.app.logic.card import Card
class CardUser(Card):
    def __init__(self, id_card: int, card_type: str, balance: float, user_id: int):
        super().__init__(id_card, card_type, balance)
        self.user_id = user_id
    def use_card(self):
        if self.balance >= 3000: ##Ah? 
            self.balance -= 3000
            print(f"Card {self.id_card} used by user {self.user_id}. Remaining balance: {self.balance}")
            return True
        else:
            print(f"Card {self.id_card} used by user {self.user_id}. Insufficient balance.")
            return False
class Card:
    def __init__(self, id_card: int, card_type: str, balance: float):
        self.id_card = id_card
        self.card_type = card_type
        self.balance = balance

    def use_card(self):
        raise NotImplementedError("The use_card method must be implemented by subclasses.")
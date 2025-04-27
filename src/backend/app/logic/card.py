class Card:
    """
    Abstract base class representing a generic card.

    Attributes:
        id_card (int): Unique identifier for the card.
        card_type (str): Type of the card.
        balance (float): Available balance on the card.
    """

    def __init__(self, id_card: int=1, card_type: str='type', balance: float=0):
        if balance < 0:
            raise ValueError("Balance cannot be negative.")
        self.__id_card = id_card
        self.__card_type = card_type
        self.__balance = balance

    @property
    def id_card(self) -> int:
        """Returns the card's ID."""
        return self.__id_card

    @id_card.setter
    def id_card(self, value: int):
        self.__id_card = value

    @property
    def card_type(self) -> str:
        """Returns the card type."""
        return self.__card_type

    @card_type.setter
    def card_type(self, value: str):
        self.__card_type = value

    @property
    def balance(self) -> float:
        """Returns the balance on the card."""
        return self.__balance

    @balance.setter
    def balance(self, value: float):
        if value < 0:
            raise ValueError("Balance cannot be negative.")
        self.__balance = value

    def get_card_information(self) -> dict:
        """Returns a dictionary with card information."""
        return {
            "id_card": self.id_card,
            "card_type": self.card_type,
            "balance": self.balance
        }
    
    def use_card(self):
        """Abstract method to be implemented in subclasses."""
        raise NotImplementedError("The use_card method must be implemented by subclasses.")
    
    def __str__(self):
        return dict(idn=self.id_card, tipo=self.card_type, saldo=self.balance).__str__()
        
if __name__ == "__main__":
    try:
        card = Card(1001, "Bus", 150.0)
        print(card)
        card.balance -= 50
        print(card)
    except Exception as e:
        print(f"Error: {e}")

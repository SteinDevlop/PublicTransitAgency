import unittest
from services.card_operative import CardOperative

class TestCardOperative(unittest.TestCase):
    def setUp(self):
        self.card = CardOperative(card_id=1, card_type='debit', card_number='1234567890123456', expiration_date='12/25')
        self.card.user_id = 1001  # Simulamos un usuario asignado
        self.card.balance = 5000.0  # Simulamos un saldo inicial

    def test_use_card(self):
        result = self.card.use_card()
        self.assertTrue(result)
    
    def test_card_attributes(self):
        self.assertEqual(self.card.id_card, 1)
        self.assertEqual(self.card.card_type, 'debit')
        self.assertEqual(self.card.card_number, '1234567890123456')
        self.assertEqual(self.card.expiration_date, '12/25')
        self.assertEqual(self.card.user_id, 1001)
        self.assertEqual(self.card.balance, 5000.0)

if __name__ == '__main__':
    unittest.main()

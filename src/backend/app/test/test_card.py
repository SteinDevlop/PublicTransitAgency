import unittest
from services.card import Card

class TestCard(unittest.TestCase):
    def setUp(self):
        self.card = Card(id_card=2, card_type='bus', balance=5000.0, user_id=2002)

    def test_use_card_sufficient_balance(self):
        result = self.card.use_card()
        self.assertTrue(result)
        self.assertEqual(self.card.balance, 2000.0)

    def test_use_card_insufficient_balance(self):
        self.card.balance = 1000.0
        result = self.card.use_card()
        self.assertFalse(result)
        self.assertEqual(self.card.balance, 1000.0)
    
    def test_card_user_attributes(self):
        self.assertEqual(self.card.id_card, 2)
        self.assertEqual(self.card.card_type, 'bus')
        self.assertEqual(self.card.balance, 5000.0)
        self.assertEqual(self.card.user_id, 2002)

if __name__ == '__main__':
    unittest.main()
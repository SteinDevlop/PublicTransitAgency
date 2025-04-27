import unittest
import datetime
from src.backend.app.logic.payments import Payments, Movement, TransactionType, Balance
from src.backend.app.logic.card import Card

class TestPaymentsSystem(unittest.TestCase):
    def setUp(self):
        self.card = Card("123", "John Doe", 100.0)
        self.card.balance_manager = Balance(100.0)
        
    def test_payment_creation(self):
        payment = Payments(
            user="John Doe",
            payment_quantity=50.0,
            payment_method=True,
            vehicle_type=1,
            card=self.card
        )
        
        self.assertEqual(payment.payment_quantity, 50.0)
        self.assertEqual(self.card.balance, 50.0)
        
    def test_insufficient_balance(self):
        with self.assertRaises(ValueError):
            Payments(
                user="John Doe",
                payment_quantity=150.0,
                payment_method=True,
                vehicle_type=1,
                card=self.card
            )
            
    def test_movement_creation(self):
        movement = Movement(
            transaction_type=TransactionType.PAYMENT,
            amount=30.0,
            vehicle_type=2
        )
        
        self.assertEqual(movement.transaction_type, TransactionType.PAYMENT)
        self.assertEqual(movement.amount, 30.0)
        self.assertEqual(movement.vehicle_type, 2)
        self.assertIsInstance(movement.date, datetime.datetime)
        
    def test_balance_management(self):
        balance = Balance(100.0)
        
        # Test payment
        payment_movement = Movement(TransactionType.PAYMENT, 40.0, 1)
        balance.add_movement(payment_movement)
        self.assertEqual(balance.balance, 60.0)
        
        # Test recharge
        recharge_movement = Movement(TransactionType.RECHARGE, 20.0, 0)
        balance.add_movement(recharge_movement)
        self.assertEqual(balance.balance, 80.0)
        
        # Test refund
        refund_movement = Movement(TransactionType.REFUND, 10.0, 0)
        balance.add_movement(refund_movement)
        self.assertEqual(balance.balance, 90.0)
        
    def test_payment_records_movement(self):
        payment = Payments(
            user="John Doe",
            payment_quantity=25.0,
            payment_method=True,
            vehicle_type=1,
            card=self.card
        )
        
        movements = self.card.balance_manager.get_movements()
        self.assertEqual(len(movements), 1)
        self.assertEqual(movements[0].transaction_type, TransactionType.PAYMENT)
        self.assertEqual(movements[0].amount, 25.0)
        
    def test_negative_payment_amount(self):
        with self.assertRaises(ValueError):
            payment = Payments(
                user="John Doe",
                payment_quantity=-10.0,
                payment_method=True,
                vehicle_type=1,
                card=self.card
            )

if __name__ == '__main__':
    unittest.main()
import unittest
import datetime
from src.backend.app.logic.card import Card
from src.backend.app.logic.payments import Payments



class TestPayments(unittest.TestCase):
    """
    Unit tests for the Payments class using a TestCard instance.
    """
    def test_successful_payment(self):
        """
        Test that a payment is created correctly when there is sufficient balance.
        """
        payment = Payments("user1", 30.0, True, 1, self.card)
        self.assertEqual(payment.user, "user1")
        self.assertEqual(payment.payment_quantity, 30.0)
        self.assertTrue(payment.payment_method)
        self.assertEqual(payment.vehicle_type, 1)
        self.assertEqual(payment.card.id_card, 1001)
        self.assertAlmostEqual(payment.card.balance, 70.0)
        self.assertIsInstance(payment.date, datetime.datetime)

    def test_insufficient_balance_raises_error(self):
        """
        Test that a payment with insufficient balance raises a ValueError.
        """
        with self.assertRaises(ValueError):
            Payments("user2", 200.0, True, 2, self.card)

    def test_payment_setters_update_values(self):
        """
        Test that the setters update the values correctly.
        """
        payment = Payments("user3", 20.0, False, 2, self.card)
        payment.user = "updated_user"
        payment.payment_quantity = 10.0
        payment.payment_method = True
        payment.vehicle_type = 3

        self.assertEqual(payment.user, "updated_user")
        self.assertEqual(payment.payment_quantity, 10.0)
        self.assertTrue(payment.payment_method)
        self.assertEqual(payment.vehicle_type, 3)

    def test_negative_payment_quantity_raises_error(self):
        """
        Test that setting a negative payment quantity raises a ValueError.
        """
        payment = Payments("user4", 15.0, True, 4, self.card)
        with self.assertRaises(ValueError):
            payment.payment_quantity = -5.0

    def test_str_representation_format(self):
        """
        Test that the __str__ method returns a properly formatted string.
        """
        payment = Payments("user5", 25.0, True, 1, self.card)
        output = str(payment)
        self.assertIn("=== Comprobante de Pago ===", output)
        self.assertIn("Usuario:          user5", output)
        self.assertIn("Monto Pagado:     $25.00", output)
        self.assertIn("Método de Pago:   Tarjeta", output)
        self.assertIn("Tipo de Vehículo: 1", output)
        self.assertIn("ID Tarjeta:       1001", output)
        self.assertIn("Saldo Restante:", output)


if __name__ == "__main__":
    unittest.main()

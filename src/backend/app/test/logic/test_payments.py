import unittest
import datetime
from backend.app.logic.card import Card
from backend.app.logic.payments import Payments

class TestPayments(unittest.TestCase):
    def setUp(self):
        # Crear una tarjeta de prueba con saldo suficiente
        self.card = Card("123456", "Juan Perez", 100.0)
        self.valid_payment = Payments(
            user="Juan Perez",
            payment_quantity=50.0,
            payment_method=True,
            vehicle_type=1,
            card=self.card
        )
    
    def test_payment_initialization(self):
        """Verifica que el pago se inicialice correctamente"""
        self.assertEqual(self.valid_payment.user, "Juan Perez")
        self.assertEqual(self.valid_payment.payment_quantity, 50.0)
        self.assertTrue(self.valid_payment.payment_method)
        self.assertEqual(self.valid_payment.vehicle_type, 1)
        self.assertIsInstance(self.valid_payment.date, datetime.datetime)
    
    def test_card_balance_updated(self):
        """Verifica que el saldo de la tarjeta se actualice correctamente"""
        self.assertEqual(self.card.balance, 50.0)  # 100 inicial - 50 del pago
    
    def test_insufficient_balance(self):
        """Verifica que se lance excepción con saldo insuficiente"""
        with self.assertRaises(ValueError):
            Payments(
                user="Juan Perez",
                payment_quantity=150.0,
                payment_method=True,
                vehicle_type=1,
                card=self.card
            )
    
    def test_negative_payment(self):
        """Verifica que no se permitan pagos con cantidad negativa"""
        with self.assertRaises(ValueError):
            self.valid_payment.payment_quantity = -10.0
    
    def test_property_setters(self):
        """Verifica los setters de las propiedades"""
        self.valid_payment.user = "Maria Garcia"
        self.valid_payment.payment_method = False
        self.valid_payment.vehicle_type = 2
        
        self.assertEqual(self.valid_payment.user, "Maria Garcia")
        self.assertFalse(self.valid_payment.payment_method)
        self.assertEqual(self.valid_payment.vehicle_type, 2)
    
    def test_str_representation(self):
        """Verifica la representación en cadena del pago"""
        str_repr = str(self.valid_payment)
        self.assertIn("=== Comprobante de Pago ===", str_repr)
        self.assertIn("Usuario:          Juan Perez", str_repr)
        self.assertIn("Monto Pagado:     $50.00", str_repr)
        self.assertIn("Método de Pago:   Tarjeta", str_repr)
        self.assertIn("Tipo de Vehículo: 1", str_repr)
        self.assertIn("ID Tarjeta:       123456", str_repr)
        self.assertIn("Saldo Restante:   $50.00", str_repr)

if __name__ == "__main__":
    unittest.main()
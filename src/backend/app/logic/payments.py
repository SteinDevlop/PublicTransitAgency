import datetime #aplicar fecha, eliminar id payment
class Payments:
    def __init__(self, id_payment: int, user: str, payment_quantity: float, payment_method: str):
        self.id_payment = id_payment
        self.user= user
        self.payment_quantity = payment_quantity
        self.payment_method = payment_method

    def process_payment(self, amount):
        if amount <= 0:
            raise ValueError("Payment amount must be greater than zero.")
        if amount > self.payment_quantity:
            raise ValueError("Insufficient payment quantity.")
        #Tener en cuenta tipos de vehiculo (crear el dato tipo_vehiculo (1,2,3 tentativamente.))
        print(f"Processing payment of ${amount}")
        return True

    def ticket_validation(self, transaction_id):
        if not transaction_id:
            raise ValueError("Transaction ID is required.")
        
        print(f"Validating ticket with transaction ID: {transaction_id}")
        return True
    ## Agregar atributo date, crear clases movimiento (Para guardar los datos (Dates, tipo_transaccion, monto, tipo_vehiculo), Saldo (para reflejar.))
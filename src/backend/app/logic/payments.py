import datetime
from backend.app.logic.card import Card  

class Payments:
    def __init__(self, user: str, payment_quantity: float, payment_method: bool, vehicle_type: int, card: Card):
        self._date = datetime.datetime.now()
        self._user = user 
        self._payment_quantity = payment_quantity
        self._payment_method = payment_method
        self._vehicle_type = vehicle_type
        self._card = card

        if self._card.balance < self._payment_quantity:
            raise ValueError("Saldo insuficiente para realizar el pago.")
        else:
            self._card.balance -= self._payment_quantity

    @property
    def date(self):
        return self._date

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value: str):
        self._user = value

    @property
    def payment_quantity(self):
        return self._payment_quantity

    @payment_quantity.setter
    def payment_quantity(self, value: float):
        if value < 0:
            raise ValueError("La cantidad del pago no puede ser negativa.")
        self._payment_quantity = value

    @property
    def payment_method(self):
        return self._payment_method

    @payment_method.setter
    def payment_method(self, value: bool):
        self._payment_method = value

    @property
    def vehicle_type(self):
        return self._vehicle_type

    @vehicle_type.setter
    def vehicle_type(self, value: int):
        self._vehicle_type = value

    @property
    def card(self):
        return self._card

    @card.setter
    def card(self, value: Card):
        self._card = value

    def __str__(self):
        return (
            f"=== Comprobante de Pago ===\n"
            f"Fecha:            {self.date.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"Usuario:          {self.user}\n"
            f"Monto Pagado:     ${self.payment_quantity:.2f}\n"
            f"Método de Pago:   {'Tarjeta' if self.payment_method else 'Efectivo'}\n"
            f"Tipo de Vehículo: {self.vehicle_type}\n"
            f"ID Tarjeta:       {self.card.id_card}\n"
            f"Saldo Restante:   ${self.card.balance:.2f}"
        )

    ## Agregar atributo date, crear clases movimiento (Para guardar los datos (Dates, tipo_transaccion, monto, tipo_vehiculo), Saldo (para reflejar.))
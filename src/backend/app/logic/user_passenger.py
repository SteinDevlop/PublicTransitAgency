from backend.app.logic.user import User
from backend.app.logic.payments import Payments
from backend.app.logic.routes import Routes
from backend.app.logic.stops import Stops
from backend.app.logic.card_user import CardUser

class Passenger(User):
    def __init__(self, id_user: int, type_identification: str, identification: int, name: str, email: str, password: str, role: str, card: CardUser):
        super().__init__(id_user, type_identification, identification, name, email, password, role, card)
        if not self.verify_name(name):
            raise ValueError("Invalid Name")
        if not self.verify_email(email):
            raise ValueError("Invalid Email")
        if not self.verify_password(password):
            raise ValueError("Invalid Password")

    def use_card(self, method: str):
        match method:
            case "pay":
                self._pay()
            case "recharge":
                self._recharge()
            case "get_card_information":
                return self._get_card_information()
            case _:
                raise ValueError("Invalid operation")

    def _pay(self):
        payment_quantity = input("Enter the payment quantity: ")
        payment_method = input("Enter the payment method: ")
        payment = Payments(self.name, payment_quantity, payment_method)
        payment.process_payment(payment_quantity)

    def _recharge(self):
        payment_quantity = input("Enter the recharge quantity: ")
        payment_method = input("Enter the recharge method: ")
        payment = Payments(self.name, payment_quantity, payment_method)
        payment.process_payment(payment_quantity)

    def _get_card_information(self):
        card_information = self.card.get_card_information()
        if card_information is None:
            raise ValueError("Card not found")
        return card_information

    def get_route_information(self, id_route: str):
        route_information = Routes.get_route_information(id_route)  # Usando un método adecuado para obtener la ruta
        if route_information is None:
            raise ValueError("Route not found")
        return route_information

    def get_stop_information(self, stop_id: str):
        stop_information = Stops.get_stop_information(stop_id)  # Usando un método adecuado para obtener la parada
        if stop_information is None:
            raise ValueError("Stop not found")
        return stop_information

    def plan_route(self):
        origin = input("Enter the origin parade: ")
        destination = input("Enter the destination parade: ")
        route = Routes.plan_route(origin, destination)  # Suponiendo que Routes tiene un método estático `plan_route`
        if route is None:
            raise ValueError("Route not found")
        return route

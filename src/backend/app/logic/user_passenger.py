from src.backend.app.logic.user import User
from src.backend.app.logic.payments import Payments
from src.backend.app.logic.routes import Routes
from src.backend.app.logic.stops import Stops
from src.backend.app.logic.card_user import CardUser
class Passenger(User):
    def __init__(self, id_user:int, type_identification:str,identification:int, name:str, email:str, password:str, role:str, card:CardUser):
        super().__init__(id_user,type_identification,identification, name, email, password, role, card)     
        if not self.verify_name(name):
            raise ValueError("Invalid Name")
        if not self.verify_email(email):
            raise ValueError("Invalid Email")
        if not self.verify_password(password):
            raise ValueError("Invalid Password")

    def use_card(self, method:str):
        match (method):
            case ("pay"):
                payment_quantity = input("Enter the payment quantity: ")
                payment_method = input("Enter the payment method: ")
                pay(self, payment_quantity , payment_method)
            case ("recharge"):
                payment_quantity = input("Enter the payment quantity: ")
                payment_method = input("Enter the payment method: ")
                recharge(self, payment_quantity , payment_method) 
            case ("get_card_information"):
                get_card_information(self)

        def pay(self, payment_quantity , payment_method):
            """
            Purpose: Pay for a route with a payment method.
            """
            payment = Payments(self.name, payment_quantity, payment_method)
            payment.process_payment(payment_quantity)
        def recharge(self, payment_quantity , payment_method): 
            """
            Purpose: Recharge the card with a payment method.
            """
            payment = Payments(self.name, payment_quantity, payment_method)
            payment.process_payment(payment_quantity)
        def get_card_information(self):
            """
            Purpose: Get Information of the card like amounnt-info, movement-stack, etc.
            """
            card_information = self.card.get(card_id=self.card.id_card)
            if card_information is None:
                raise ValueError("Card not found")
            else:
                return card_information
            
    def get_route_information(self, id_route:str):
        """
         Purpose: Get Information of any route like schedule of the route and its parades.
        """
        route_information = Routes.route_id
        if route_information is None:
            raise ValueError("Route not found")
        else:
            return route_information

    def get_stop_information(self,stop_id:str):
        """
        Purpose: Get information of a parade related by any of the routes that belong to the parade like th schedule.
        """
        stop_information = Stops.stop_id
        if stop_information is None:
            raise ValueError("Stop not found")
        else:
            return stop_information
    def plan_route(self):
        """
        Purpose: Get the best route to get to a parade, having as parameters the origin parade and the destination parade.
        """
        origin = input("Enter the origin parade: ")
        destination = input("Enter the destination parade: ")
        route = Routes(origin, destination)
        if route is None:
            raise ValueError("Route not found")
        else:
            return route
        # end def
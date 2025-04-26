from src.backend.app.logic.user import User
from src.backend.app.logic.payments import Payments
class Passenger(User):
    def __init__(self, id_user, type_identification,identification, name, email, password, role, card):
        super().__init__(id_user,type_identification,identification, name, email, password, role, card)     
        if not self.verify_name(name):
            raise ValueError("Invalid Name")
        if not self.verify_email(email):
            raise ValueError("Invalid Email")
        if not self.verify_password(password):
            raise ValueError("Invalid Password")

    def use_card(self):
        def pay(self, payment_quantity , payment_method):
            payment = Payments(self.name, payment_quantity, payment_method)
            payment.process_payment(payment_quantity)
        def recharge(self, payment_quantity , payment_method): 
            payment = Payments(self.name, payment_quantity, payment_method)
            payment.process_payment(payment_quantity)
        def get_card_information(self,card):
            """
            Purpose: Get Information of the card like amounnt-info, movement-stack, etc.
            """
    def get_route_information(self):
        """
         Purpose: Get Information of any route like schedule of the route and its parades.
        """ 
    def get_parade_information(self):
        """
        Purpose: Get information of a parade related by any of the routes that belong to the parade like th schedule.
        """
    def plan_route(self):
        """
        Purpose: Get the best route to get to a parade, having as parameters the origin parade and the destination parade.
        """
        
        # end def
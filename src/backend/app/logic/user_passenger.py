from user import User
from payments import Payments
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
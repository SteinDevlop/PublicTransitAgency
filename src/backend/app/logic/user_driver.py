from backend.app.logic.user import User
from backend.app.logic.card_operative import CardOperative
import re

class Worker(User):
    def __init__(self, id_user:int, type_identification:str,identification:int, name:str, email:str, password:str, 
                 role:str, card:CardOperative):
        super().__init__(id_user,type_identification,identification, name, email, password, role, card)
        self.routes_assigmented = []
                
        if not self.verify_name(name):
            raise ValueError("Invalid Name")
        if not self.verify_email(email):
            raise ValueError("Invalid Email")
        if not self.verify_password(password):
            raise ValueError("Invalid Password")
    def get_driver_assigment(self):
        """
        Purpose: Get information of driver's routes assigmented
        """
        return self.routes_assigmented
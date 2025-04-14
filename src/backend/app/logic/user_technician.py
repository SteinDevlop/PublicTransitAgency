from user import User

class Technician(User):
    def __init__(self, id_user, type_identification,identification, name, email, password, role):
        super().__init__(id_user,type_identification,identification, name, email, password, role)
                
        if not self.verify_name(name):
            raise ValueError("Invalid Name")
        if not self.verify_email(email):
            raise ValueError("Invalid Email")
        if not self.verify_password(password):
            raise ValueError("Invalid Password")
    def create_report(self):
        """
        Purpose: Create a manteinment report
        """
    def get_manteinment_schedule(self):
        """
        Purpose: Get schedule information
        """
    def set_manteinment_report(self, atributte, value):
        """
        Purpose: Actualize manteinment report
        """
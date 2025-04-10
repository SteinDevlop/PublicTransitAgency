from user import User

class Supervisor(User):
    def __init__(self, id_user, type_identification,identification, name, email, password, role):
        super().__init__(id_user,type_identification,identification, name, email, password, role)
                
        if not self.verify_name(name):
            raise ValueError("Invalid Name")
        if not self.verify_email(email):
            raise ValueError("Invalid Email")
        if not self.verify_password(password):
            raise ValueError("Invalid Password")
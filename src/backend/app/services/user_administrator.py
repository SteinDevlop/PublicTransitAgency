from user import User

class Administrator(User):
    def __init__(id_user, name, email, password, role):
        super().__init__(id_user, name, email, password, role)

    def get_information(self):
            print(f"Information: ID:{self.id_user},Name:{self.name}, Email:{self.email}, Password:{self.password}, Role:{self.role}")
            return True
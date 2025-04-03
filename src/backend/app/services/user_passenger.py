from user import User

class Passenger(User):
    def __init__(self, id_user, type_identification,identification, name, email, password, role):
        super().__init__(id_user,type_identification,identification, name, email, password, role)
                
        if not self.verify_name(name):
            raise ValueError("Invalid Name")
        if not self.verify_email(email):
            raise ValueError("Invalid Email")
        if not self.verify_password(password):
            raise ValueError("Invalid Password")
    
    @property
    def information(self):
            return(f"Information:\n"
                   f"\tID:{self.id_user}\n"
                   f"\tType of Identification: {self.type_identification}\n"
                   f"\tIdentification: {self.identification}\n"
                   f"\tName: {self.name}\n"
                   f"\tEmail: {self.email}\n"
                   f"\tPassword: {self.password}\n"
                   f"\tRole: {self.role}")
    
    def update_information(self, attribute, value):
        match attribute.lower():
            case "name":
                if not self.verify_name(value):
                    raise ValueError("Invalid Name")
                self.name = value
            case "email":
                if not self.verify_email(value):
                    raise ValueError("Invalid Email")
                self.email = value
            case "password":
                if not self.verify_password(value):
                    raise ValueError("Invalid Password")
            case _:
                raise ValueError("Not a Valid Attribute")

    def verify_information(self, attribute, value):
        match attribute.lower():
            case "name":
                if not self.verify_name(value):
                    raise ValueError("Invalid Name")
                self.name = value
            case "email":
                if not self.verify_email(value):
                    raise ValueError("Invalid Email")
                self.email = value
            case "password":
                if not self.verify_password(value):
                    raise ValueError("Invalid Password")
                self.password = value
            case _:
                raise ValueError("Not a Valid Attribute")

    @staticmethod
    def verify_name(value):
        return value.replace(" ", "").isalpha() and len(value) > 1  # Permite nombres con espacios

    @staticmethod
    def verify_email(value):
        import re
        return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", value) is not None

    @staticmethod
    def verify_password(value):
        return len(value) >= 6  # Se puede mejorar con más reglas
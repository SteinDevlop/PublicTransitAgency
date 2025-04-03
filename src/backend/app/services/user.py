class User:
    def __init__(self, id_user: int, type_identification: str, identification: int ,name: str, email: str, password: str, role: str):
        self.id_user = id_user
        self.type_identification = type_identification
        self.identification = identification
        self.name = name
        self.email = email
        self.password = password
        self.role = role

    @property
    def information(self):
        raise NotImplementedError("The user method must be implemented by subclasses.")
    
    def update_information(self):
        raise NotImplementedError("The user method must be implemented by subclasses.")
    
    def verify_information(self):
        raise NotImplementedError("The user method must be implemented by subclasses.")
    
    def use_card(self):
        raise NotImplementedError("The user method must be implemented by subclasses.")
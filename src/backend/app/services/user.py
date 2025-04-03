class User:
    def __init__(self, id_user: int, name: str, email: str, password: str, role: str):
        self.id_user = id_user
        self.name = name
        self.email = email
        self.password = password
        self.role = role

    def use_card(self):
        raise NotImplementedError("The use_card method must be implemented by subclasses.")
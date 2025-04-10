class Incidence ():
    def __init__(self, description: str, type: str, status: str, incidence_id: int = None):
        self.description = description
        self.type = type
        self.status = status
        self.incidence_id = incidence_id
    
    def register_incidence(self):
        if not self.description or not self.type:
            raise ValueError("Description and type are required.")
        
        print(f"Registering incidence: {self.description}, Type: {self.type}")
        return True
    
    def update_incidence(self, description: str, type: str, status: str, incidence_id: int):
        if not incidence_id:
            raise ValueError("Incidence ID is required.")
        
        self.description = description
        self.type = type
        self.status = status
    
        print(f"Updating incidence ID {incidence_id}: {self.description}, Type: {self.type}, Status: {self.status}")
        return True
        
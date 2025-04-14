from user import User

class Administrator(User):
    def __init__(self, id_user, type_identification,identification, name, email, password, role):
        super().__init__(id_user,type_identification,identification, name, email, password, role)
                
        if not self.verify_name(name):
            raise ValueError("Invalid Name")
        if not self.verify_email(email):
            raise ValueError("Invalid Email")
        if not self.verify_password(password):
            raise ValueError("Invalid Password")
    def assing_route(self, Driver):
        """
        Purpose: An administator can assign a route to a vehicle with an schedule
        """
    def create_parade(self):
        """
        Purpose: An administrator can create parades in order to create new routes, primary information:
            name, ubication, schedule related with a route
        """
    def create_route(self, list_parade):
        """
        Purpose: An administrator can create new routes, primary information:
            name, schedule
        """
    def create_vehicle(self, vehicle):
        """
        Purpose: An administrator can create new vehicles, primary information:
            name, capacity, etc.
        """
    def get_route_information(self, route):
        """
        Purpose: Get route information
        """
    def get_parade_information(self, parade):
        """
        Purpose: Get parade information
        """
    def get_vehicle_information(self,vehicle):
        """
        Purpose: Get vehicle information
        """
    def set_parade_information(self, atribute,value):
        """
        Purpose: Actualize parade information
        """
    def set_route_informaiton(self,atribute,value):
        """
        Purpose: Actualize route information
        """
    def get_report(self,query):
        """
        Purpose: Show results of a query
        """
    def get_user_information(self, user):
        """
        Purpose: Get user information
        """
    def set_user_information(self,user):
        """
        Purpose: Actualize user information
        """
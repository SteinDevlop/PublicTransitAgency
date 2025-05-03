from backend.app.logic.user import User
from backend.app.logic.card_operative import CardOperative
from backend.app.logic.routes import Routes
from backend.app.logic.stops import Stops
from backend.app.logic.unit_transport import Transport
from backend.app.logic.user_driver import Worker
from backend.app.logic.ticket import Ticket

class Administrator(User):
    def __init__(self, id_user:int, type_identification:str, identification:int, name:str, email:str, password:str, 
                 role:str, card:CardOperative):
        super().__init__(id_user, type_identification, identification, name, email, password, role, card)
                
        if not self.verify_name(name):
            raise ValueError("Invalid Name")
        if not self.verify_email(email):
            raise ValueError("Invalid Email")
        if not self.verify_password(password):
            raise ValueError("Invalid Password")

    def assign_route(self, driver:Worker, route: Routes):
        """
        Purpose: An administrator can assign a route to a driver with a schedule.
        """
        driver.routes_assigmented.append(route)
        print(f"Route '{route.route_id}' assigned to driver {driver.id_user}.")

    def create_parade(self, stop_information:dict):
        """
        Purpose: Create a parade (stop/station) with name, location, and schedule.
        """
        parade = Stops(stop_information)
        print(f"Parade '{parade.stop_id}' created successfully.")
        return parade

    def create_route(self,  route_information:dict):
        """
        Purpose: Create a route using a list of parades and a schedule.
        """
        route = Routes(route_information)
        print(f"Route '{route.route_id}' created with success.")
        return route

    def create_vehicle(self, id: str, type:str, status: Ticket, ubication:str, capacity:int):
        """
        Purpose: Create a vehicle with a name and capacity.
        """
        vehicle = Transport(id, type, status, ubication, capacity)
        print(f"Vehicle '{vehicle._id}' with capacity {vehicle._capacity} created.")
        return vehicle

    def get_route_information(self, route:Routes):
        """
        Purpose: Get and print route information.
        """
        print(f"Route Name: {route._route_id}, Informatio: {route._route}")

    def get_parade_information(self, parade:Stops):
        """
        Purpose: Get and print parade information.
        """
        print(f"Parade Name: {parade._stops_id}, Informatio: {parade._stops}")

    def get_vehicle_information(self, vehicle:Transport):
        """
        Purpose: Get and print vehicle information.
        """
        print(f"Vehicle Name: {vehicle.id}, Capacity: {vehicle.capacity}")

    def set_parade_information(self, parade:Stops, attribute:str, value):
        """
        Purpose: Update parade information by attribute name.
        """
        setattr(parade, attribute, value)
        print(f"Parade '{parade.name}' updated: {attribute} set to {value}.")

    def set_route_information(self, route:Routes, attribute:str, value):
        """
        Purpose: Update route information by attribute name.
        """
        setattr(route, attribute, value)
        print(f"Route '{route.name}' updated: {attribute} set to {value}.")

    def get_report(self, query_function):
        """
        Purpose: Execute a query function and print results.
        """
        result = query_function()
        print(f"Report Result: {result}")
        return result

    def get_user_information(self, user:User):
        """
        Purpose: Get and print user information.
        """
        print(f"User: {user.name}, Email: {user.email}, Role: {user.role}")

    def set_user_information(self, user:User, attribute:str, value):
        """
        Purpose: Update user information by attribute name.
        """
        setattr(user, attribute, value)
        print(f"User '{user.name}' updated: {attribute} set to {value}.")

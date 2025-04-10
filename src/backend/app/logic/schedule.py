import datetime
from logic import transport_route
class Schedule ():
    def __init__(self, schedule_id: str, arrival_date: datetime.datetime, departure_date: datetime.datetime, route: transport_route.Route):
        self.arrival_date = arrival_date
        self.schedule_id = schedule_id
        self.departure_date = departure_date
        self.route = route

    def schedule_adjustment(self):
        if self.arrival_date < datetime.datetime.now():
            raise ValueError("Arrival date cannot be in the past.")
        if self.departure_date < self.arrival_date:
            raise ValueError("Departure date must be after arrival date.")
        ##Por ahora, ni foking idea.
    
            
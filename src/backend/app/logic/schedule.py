import datetime
from backend.app.logic.transport_route import Route

class Schedule:
    def __init__(self, schedule_id: str, arrival_date: datetime.datetime, departure_date: datetime.datetime, route: Route):
        self._schedule_id = schedule_id
        self._arrival_date = arrival_date
        self._departure_date = departure_date
        self._route = route

    @property
    def schedule_id(self) -> str:
        return self._schedule_id

    @schedule_id.setter
    def schedule_id(self, value: str):
        self._schedule_id = value

    @property
    def arrival_date(self) -> datetime.datetime:
        return self._arrival_date

    @arrival_date.setter
    def arrival_date(self, value: datetime.datetime):
        self._arrival_date = value

    @property
    def departure_date(self) -> datetime.datetime:
        return self._departure_date

    @departure_date.setter
    def departure_date(self, value: datetime.datetime):
        self._departure_date = value

    @property
    def route(self) -> Route:
        return self._route

    @route.setter
    def route(self, value: Route):
        self._route = value

    ##def schedule_adjustment(self):
      ##  if self.arrival_date < datetime.datetime.now():
        ##    raise ValueError("Arrival date cannot be in the past.")
       ## if self.departure_date < self.arrival_date:
         ##   raise ValueError("Departure date must be after arrival date.")
    
            
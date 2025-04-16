import datetime
from src.backend.app.logic import unit_transport
from src.backend.app.logic import schedule as schedule_module 
from src.backend.app.logic import user_driver

class Shift:
    def __init__(
        self,
        unit: unit_transport.Transport,
        start_time: datetime.datetime,
        end_time: datetime.datetime,
        driver: user_driver,
        schedule: schedule_module.Schedule 
    ):
        self._unit = unit
        self._start_time = start_time
        self._end_time = end_time
        self._driver = driver
        self._schedule = schedule

    @property
    def unit(self) -> unit_transport.Transport:
        return self._unit

    @unit.setter
    def unit(self, value: unit_transport.Transport):
        self._unit = value

    @property
    def start_time(self) -> datetime.datetime:
        return self._start_time

    @start_time.setter
    def start_time(self, value: datetime.datetime):
        self._start_time = value

    @property
    def end_time(self) -> datetime.datetime:
        return self._end_time

    @end_time.setter
    def end_time(self, value: datetime.datetime):
        self._end_time = value

    @property
    def driver(self) -> str:
        return self._driver

    @driver.setter
    def driver(self, value: str):
        self._driver = value

    @property
    def schedule(self) -> schedule_module.Schedule:
        return self._schedule

    @schedule.setter
    def schedule(self, value: schedule_module.Schedule):
        self._schedule = value

    def shift_assigment(self):
        if self.start_time < datetime.datetime.now():
            raise ValueError("Start time cannot be in the past.")
        
        if self.end_time < self.start_time:
            raise ValueError("End time must be after start time.")
        
        if not self.unit.is_available(self.start_time, self.end_time):
            raise ValueError("Unit is not available for the specified time.")
        
        if not self.schedule.is_valid():
            raise ValueError("Schedule is not valid.")
        
        print(f"Shift assigned to driver {self.driver} for unit {self.unit.unit_id} from {self.start_time} to {self.end_time}.")
        return True

    def shift_change(self, new_start_time: datetime.datetime, new_end_time: datetime.datetime):
        if new_start_time < datetime.datetime.now():
            raise ValueError("Start time cannot be in the past.")
        
        if new_end_time < new_start_time:
            raise ValueError("End time must be after start time.")
        
        if not self.unit.is_available(new_start_time, new_end_time):
            raise ValueError("Unit is not available for the specified time.")
        
        self.start_time = new_start_time
        self.end_time = new_end_time
        
        print(f"Shift changed to {self.start_time} - {self.end_time} for driver {self.driver}.")
        return True



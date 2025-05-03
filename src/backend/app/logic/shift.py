import datetime
from backend.app.logic.unit_transport import Transport 
from backend.app.logic.schedule import Schedule 
from backend.app.logic.user_driver import Worker

class Shift:
    def __init__(
        self,
        unit: Transport,
        start_time: datetime.datetime,
        end_time: datetime.datetime,
        driver: Worker,
        schedule: Schedule 
    ):
        self._unit = unit
        self._start_time = start_time
        self._end_time = end_time
        self._driver = driver
        self._schedule = schedule

    @property
    def unit(self) -> Transport:
        return self._unit

    @unit.setter
    def unit(self, value: Transport):
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
    def schedule(self) -> Schedule:
        return self._schedule

    @schedule.setter
    def schedule(self, value: Schedule):
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



import datetime
from services import unit_transport 
from services import schedule

class Shift ():
    def __init__(self, unit : unit_transport.Transport, start_time: datetime.datetime, end_time: datetime.datetime, driver: str, schedule: schedule.Schedule):
        self.driver = driver
        self.schedule = schedule
        self.unit = unit
        self.start_time = start_time
        self.end_time = end_time
        pass
    
    def shift_assigment (self):
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
        # Por ahora le pongo esto.
    
    def shift_change (self, new_start_time: datetime.datetime, new_end_time: datetime.datetime):
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
        


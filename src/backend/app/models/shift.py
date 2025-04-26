from pydantic import BaseModel, validator
from datetime import datetime
from typing import Dict, Any
from models.transport import TransportOut
from models.schedule import ScheduleOut
from models.user_driver import WorkerOut #Implementacion pendiente.

class ShiftBase(BaseModel):
    @classmethod
    def get_fields(cls) -> Dict[str, str]:
        return {
            "shift_id": "TEXT PRIMARY KEY",
            "unit_id": "TEXT NOT NULL",
            "start_time": "TIMESTAMP NOT NULL",
            "end_time": "TIMESTAMP NOT NULL",
            "driver_id": "TEXT NOT NULL",
            "schedule_id": "TEXT NOT NULL",
            "FOREIGN KEY(unit_id)": "REFERENCES transport(unit_id)",
            "FOREIGN KEY(driver_id)": "REFERENCES workers(worker_id)",
            "FOREIGN KEY(schedule_id)": "REFERENCES schedules(schedule_id)"
        }

class ShiftCreate(ShiftBase):
    unit: Dict[str, Any]
    start_time: datetime
    end_time: datetime
    driver: Dict[str, Any]
    schedule: Dict[str, Any]

    @validator('end_time')
    def validate_times(cls, v, values):
        if 'start_time' in values and v <= values['start_time']:
            raise ValueError("End time must be after start time")
        if v < datetime.now():
            raise ValueError("Cannot create shift in the past")
        return v

    def to_dict(self) -> Dict[str, Any]:
        return {
            "unit_id": self.unit['unit_id'],
            "unit_data": self.unit,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "driver_id": self.driver['worker_id'],
            "driver_data": self.driver,
            "schedule_id": self.schedule['schedule_id'],
            "schedule_data": self.schedule
        }

class ShiftOut(ShiftCreate):
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            unit=data['unit_data'],
            start_time=datetime.fromisoformat(data['start_time']),
            end_time=datetime.fromisoformat(data['end_time']),
            driver=data['driver_data'],
            schedule=data['schedule_data']
        )
    
    @classmethod
    def get_empty_instance(cls):
        return cls(
            unit={},
            start_time=datetime.now(),
            end_time=datetime.now(),
            driver={},
            schedule={}
        )
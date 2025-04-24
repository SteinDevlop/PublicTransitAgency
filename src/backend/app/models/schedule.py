from pydantic import BaseModel, validator
from datetime import datetime
from typing import Dict, Any
from models.routes import RouteOut  

class ScheduleBase(BaseModel):
    @classmethod
    def get_fields(cls) -> Dict[str, str]:
        return {
            "schedule_id": "TEXT PRIMARY KEY",
            "arrival_date": "TIMESTAMP NOT NULL",
            "departure_date": "TIMESTAMP NOT NULL",
            "route_id": "TEXT NOT NULL",
            "FOREIGN KEY(route_id)": "REFERENCES routes(route_id)"
        }

class ScheduleCreate(ScheduleBase):
    schedule_id: str
    arrival_date: datetime
    departure_date: datetime
    route: Dict[str, Any]  # Serialized Route data

    @validator('departure_date')
    def validate_dates(cls, v, values):
        if 'arrival_date' in values and v < values['arrival_date']:
            raise ValueError("Departure date must be after arrival date")
        if v < datetime.now():
            raise ValueError("Dates cannot be in the past")
        return v

    def to_dict(self) -> Dict[str, Any]:
        return {
            "schedule_id": self.schedule_id,
            "arrival_date": self.arrival_date.isoformat(),
            "departure_date": self.departure_date.isoformat(),
            "route_id": self.route['route_id'],
            "route_data": self.route
        }

class ScheduleOut(ScheduleCreate):
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            schedule_id=data['schedule_id'],
            arrival_date=datetime.fromisoformat(data['arrival_date']),
            departure_date=datetime.fromisoformat(data['departure_date']),
            route=data['route_data']
        )
    
    @classmethod
    def get_empty_instance(cls):
        return cls(
            schedule_id="",
            arrival_date=datetime.now(),
            departure_date=datetime.now(),
            route={}
        )
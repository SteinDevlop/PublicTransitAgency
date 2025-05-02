import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel

class ScheduleBase(BaseModel):
    __entity_name__ = "Horario"  # Agrega el atributo __entity_name__
    schedule_id: Optional[str] = None
    arrival_date: Optional[datetime.datetime] = None
    departure_date: Optional[datetime.datetime] = None
    route_id: Optional[str] = None  # Foreign key to Route

    def to_dict(self) -> Dict[str, Any]:
        return self.dict()

    @classmethod
    def get_fields(cls) -> Dict[str, str]:
        return {
            "schedule_id": "TEXT PRIMARY KEY",
            "arrival_date": "DATETIME NOT NULL",
            "departure_date": "DATETIME NOT NULL",
            "route_id": "TEXT NOT NULL"
            # Define foreign key relationship in your database schema
        }

class ScheduleCreate(ScheduleBase):
    __entity_name__ = "Horario" #Agrega el atributo
    arrival_date: datetime.datetime
    departure_date: datetime.datetime
    route_id: str

class ScheduleOut(ScheduleBase):
    __entity_name__ = "Horario" #Agrega el atributo
    class Config:
        from_attributes = True

    @classmethod
    def from_dict(cls, data: dict) -> 'ScheduleOut':
        return cls(**data)

    @classmethod
    def get_empty_instance(cls) -> 'ScheduleOut':
        return cls(schedule_id="", arrival_date=datetime.datetime.now(), departure_date=datetime.datetime.now(), route_id="")
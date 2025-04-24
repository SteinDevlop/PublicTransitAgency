from pydantic import BaseModel, validator
from typing import Dict, Any

class StopBase(BaseModel):
    @classmethod
    def get_fields(cls) -> Dict[str, str]:
        return {
            "stop_id": "TEXT PRIMARY KEY",
            "stop_data": "JSON NOT NULL"
        }

class StopCreate(StopBase):
    stop_id: str
    stop_data: Dict[str, Any]

    @validator('stop_id')
    def validate_stop_id(cls, v):
        if not v:
            raise ValueError("stop_id cannot be empty")
        return v

    def to_dict(self) -> Dict[str, Any]:
        return {
            "stop_id": self.stop_id,
            "stop_data": self.stop_data
        }

class StopOut(StopCreate):
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            stop_id=data['stop_id'],
            stop_data=data['stop_data']
        )
    
    @classmethod
    def get_empty_instance(cls):
        return cls(stop_id="", stop_data={})
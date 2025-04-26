from pydantic import BaseModel
from typing import Dict, Any

class RouteBase(BaseModel):
    @classmethod
    def get_fields(cls) -> Dict[str, str]:
        return {
            "route_id": "TEXT PRIMARY KEY",
            "route": "JSON NOT NULL"
        }

class RouteCreate(RouteBase):
    route: Dict[str, Any]
    route_id: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "route_id": self.route_id,
            "route": self.route
        }

class RouteOut(RouteCreate):
    @classmethod
    def from_dict(cls, data: dict):
        return cls(route=data["route"], route_id=data["route_id"])
    
    @classmethod
    def get_empty_instance(cls):
        return cls(route={}, route_id="")
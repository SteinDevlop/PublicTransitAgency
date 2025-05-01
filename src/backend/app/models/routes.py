from typing import Optional
from pydantic import BaseModel

class RouteBase(BaseModel):
    __entity_name__ = "routes"
    route_id: str
    name: Optional[str] = None
    origin: Optional[str] = None
    destination: Optional[str] = None

    def to_dict(self):
        return self.dict()

    @classmethod
    def get_fields(cls):
        return {
            "route_id": "TEXT PRIMARY KEY",
            "name": "TEXT",
            "origin": "TEXT",
            "destination": "TEXT"
        }

class RouteCreate(RouteBase):
    pass

class RouteOut(RouteBase):
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
from typing import List
from backend.app.logic.transport_parade import Parade

class Route:
    """
    Represents a transport route with stops, estimated duration, origin, and destination.
    """

    def __init__(self, stops: List[Parade], estimated_duration: float, origin: str, destination: str):
        self.stops = stops
        self.estimated_duration = estimated_duration
        self.origin = origin
        self.destination = destination

    def update_route(self, stops: List[Parade] = None, estimated_duration: float = None, 
                     origin: str = None, destination: str = None):
        if stops is not None:
            self.stops = stops
        if estimated_duration is not None:
            self.estimated_duration = estimated_duration
        if origin is not None:
            self.origin = origin
        if destination is not None:
            self.destination = destination
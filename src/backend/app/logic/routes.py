from src.backend.app.logic.stops import Stops

class Routes(Stops):
    def __init__(self, route: dict, id: str) -> None:
        super().__init__(route, id)
        self._route = route
        self._route_id = route.get("route_id")

    @property
    def route(self) -> dict:
        return self._route

    @route.setter
    def route(self, value: dict) -> None:
        self._route = value
        self._route_id = value.get("route_id", None)

    @property
    def route_id(self) -> str:
        return self._route_id

    @route_id.setter
    def route_id(self, value: str) -> None:
        self._route_id = value

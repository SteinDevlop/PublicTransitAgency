class Stops:
    def __init__(self, stop: dict, stop_id: str = None) -> None:
        self._stop = stop
        self._stop_id = stop_id or stop.get("stop_id")

    @property
    def stop(self) -> dict:
        return self._stop

    @stop.setter
    def stop(self, value: dict):
        self._stop = value
        self._stop_id = value.get("stop_id")

    @property
    def stop_id(self) -> str:
        return self._stop_id

    @stop_id.setter
    def stop_id(self, value: str):
        self._stop_id = value

    def to_dict(self) -> dict:
        return {
            "stop_id": self._stop_id,
            "stop": self._stop
        }
    @classmethod
    def from_dict(cls, data: dict):
        return cls(stop=data.get("stop", {}), stop_id=data.get("stop_id"))

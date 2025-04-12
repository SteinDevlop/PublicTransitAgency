class Stops:

    def __init__(self, stop: dict, id: str) -> None:
        self._stop = stop
        self._stop_id = stop.get("stop_id")

    @property
    def stop(self) -> dict:
        return self._stop

    @stop.setter
    def stop(self, value: dict):
        self._stop = value
        self._stop_id = value.get("stop_id")  # update stop_id based on new stop dict

    @property
    def stop_id(self) -> str:
        return self._stop_id

    @stop_id.setter
    def stop_id(self, value: str):
        self._stop_id = value

        #Ni idea q hacer con esta 
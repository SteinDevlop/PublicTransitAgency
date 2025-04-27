class Stops:
    def __init__(self, stop_data: dict):
        self._stop = stop_data
        self._stop_id = stop_data.get('stop_id')

    @property
    def stop(self):
        return self._stop

    @stop.setter
    def stop(self, value: dict):
        self._stop = value
        self._stop_id = value.get('stop_id')

    @property
    def stop_id(self):
        return self._stop_id

    @stop_id.setter
    def stop_id(self, value):
        self._stop_id = value
        self._stop['stop_id'] = value  
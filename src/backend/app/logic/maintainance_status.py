class MaintainanceStatus:
    def __init__(self, id: int, unit: str, type: str, status: str):
        self._id = id
        self._unit = unit
        self._type = type
        self._status = status

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value: int):
        self._id = value

    @property
    def unit(self) -> str:
        return self._unit

    @unit.setter
    def unit(self, value: str):
        self._unit = value

    @property
    def type(self) -> str:
        return self._type

    @type.setter
    def type(self, value: str):
        self._type = value

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value: str):
        self._status = value


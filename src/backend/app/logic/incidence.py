from logic import ticket
class Incidence:
    def __init__(self, description: str, type: str, status: ticket, incidence_id: int = None):
        self._description = description
        self._type = type
        self._status = status
        self._incidence_id = incidence_id

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str):
        self._description = value

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

    @property
    def incidence_id(self) -> int:
        return self._incidence_id

    @incidence_id.setter
    def incidence_id(self, value: int):
        self._incidence_id = value

    def update_incidence(self, description: str, type: str, status: str, incidence_id: int):
        if incidence_id is None:
            raise ValueError("Incidence ID is required.")
        self.description = description
        self.type = type
        self.status = status

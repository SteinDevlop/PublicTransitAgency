from backend.app.logic.ticket import Ticket

class Incidence:
    def __init__(self, ID: int, description: str, status: Ticket, type: str, transport_id: int = None):
        self._ID = ID
        self._description = description
        self._status = status
        self._type = type
        self._status = status
        self._transport_id = transport_id

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str):
        self._description = value

    @property
    def status(self) -> Ticket:
        return self._status

    @status.setter
    def status(self, value: Ticket):
        self._status = value

    @property
    def type(self) -> str:
        return self._type

    @type.setter
    def type(self, value: str):
        self._type = value

    @property
    def incidence_id(self) -> int:
        return self._incidence_id

    @incidence_id.setter
    def incidence_id(self, value: int):
        self._incidence_id = value

    def update_incidence(self, description: str, status: Ticket, type: str, incidence_id: int):
        if incidence_id is None:
            raise ValueError("Incidence ID is required.")
        self.description = description
        self.status = status
        self.type = type
        self.incidence_id = incidence_id

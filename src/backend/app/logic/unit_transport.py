from backend.app.logic.ticket import Ticket

class Transport:
    def __init__(self, id: str, type: str, status: Ticket, ubication: str, capacity: int):
        self._id = id
        self._type = type
        self._status = status
        self._ubication = ubication
        self._capacity = capacity

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @property
    def ubication(self):
        return self._ubication

    @ubication.setter
    def ubication(self, value):
        self._ubication = value

    @property
    def capacity(self):
        return self._capacity

    @capacity.setter
    def capacity(self, value):
        self._capacity = value
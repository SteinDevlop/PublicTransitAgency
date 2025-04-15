class Ticket:
    """
    Clase que encapsula el estado de un ticket como un número entero (1, 2 o 3).
    """

    def __init__(self, status_code: int, ID : str):
        self._status_code = status_code
        self._ID = ID

    @property
    def status_code(self) -> int:
        return self._status_code

    @status_code.setter
    def status_code(self, value: int):
        self._status_code = value

    def __str__(self):
        return f"Ticket status: {self._status_code}"

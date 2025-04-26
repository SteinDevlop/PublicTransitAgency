from datetime import datetime

class Maintenance:
    def __init__(self, id, id_unit=None, id_status=None, type=None, date=None):
        self.id = id
        self.date = date
        self.type = type
        self.id_unit = id_unit
        self.id_status = id_status

    # Properties
    @property
    def id(self) -> int:
        return self.__id

    @id.setter
    def id(self, value: int):
        self.__id = value

    @property
    def date(self) -> datetime:
        return self.__date

    @date.setter
    def date(self, value: datetime):
        self.__date = value

    @property
    def type(self) -> str:
        return self.__type

    @type.setter
    def type(self, value: str):
        self.__type = value

    @property
    def id_unit(self) -> int:
        return self.__id_unit

    @id_unit.setter
    def id_unit(self, value: int):
        self.__id_unit = value

    @property
    def id_status(self) -> int:
        return self.__id_status

    @id_status.setter
    def id_status(self, value: int):
        self.__id_status = value

    # Necesario para el controller
    def to_dict(self) -> dict:
        return{
            "id": self.id if self.id is not None else None,
            "id_unit": self.id_unit if self.id_unit is not None else None,
            "id_status": self.id_status if self.id_status is not None else None,
            "type": self.type if self.type is not None else None,
            "date": self.date.isoformat() if self.date is not None else None
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=int(data.get("id")) if data.get("id") is not None else None,
            id_unit=int(data.get("id_unit")) if data.get("id_unit") is not None else None,
            id_status=int(data.get("id_status")) if data.get("id_status") is not None else None,
            type=str(data.get("type")) if data.get("type") is not None else None,
            date=datetime.fromisoformat(data.get("date")) if isinstance(data.get("date"), str) else None)

    @classmethod
    def get_fields(cls) -> dict:
        return {
            "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "id_unit": "INTEGER",
            "id_status": "INTEGER",
            "type": "TEXT",
            "date": "TEXT"
        }

    def __str__(self):
        return str(self.to_dict())

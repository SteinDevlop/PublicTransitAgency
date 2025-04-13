from datetime import datetime
class Maintenance:
    def __init__(self, id: int, id_unit: int, id_status: int, type: str, date: datetime):
        self.id = id
        self.date = date
        self.type = type
        self.id_unit = id_unit
        self.id_status = id_status

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

    def __str__(self):
        return dict(id_mantainment=self.id, id_unit=self.id_unit, id_status=self.id_status, type=self.type, date=self.date).__str__()

if __name__ == "__main__":
    try:
        m = Maintenance(1, 1, 1, "type", datetime.now())
        print(m)
    except Exception as e:
        print(e)
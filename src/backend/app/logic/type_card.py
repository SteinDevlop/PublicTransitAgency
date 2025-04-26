class TypeCard:
    def __init__(self, id: int=None, type: str=None):
        self.id = id
        self.type = type

    @property
    def id(self) -> int:
        return self.__id

    @id.setter
    def id(self, value: int):
        self.__id = value

    @property
    def type(self) -> str:
        return self.__type

    @type.setter
    def type(self, value: str):
        self.__type = value

    def __str__(self):
        return dict(id=self.id, type=self.type).__str__()
    @classmethod
    def get_fields(cls) -> dict:
        return {
            "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "type": "TEXT",
        }
    def to_dict(self) -> dict:
        return {
            "id": self.id if self.id is not None else None,
            "type": self.type if self.type is not None else None
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=int(data.get("id")) if data.get("id") is not None else None,
            type=str(data.get("type")) if data.get("type") is not None else None
        )
if __name__ == "__main__":
    try:
        tc = TypeCard(1, "type")
        print(tc)
    except Exception as e:
        print(e)
class TypeCard:
    def __init__(self, id: int, type: str):
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

if __name__ == "__main__":
    try:
        tc = TypeCard(1, "type")
        print(tc)
    except Exception as e:
        print(e)
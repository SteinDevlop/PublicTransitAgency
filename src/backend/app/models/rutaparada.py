from pydantic import BaseModel

class RutaParada(BaseModel):
    IDRuta: int
    IDParada: int

    __entity_name__ = "RutaParada"

    @staticmethod
    def get_fields():
        return {
            "IDRuta": "INT NOT NULL", #llave primaria
            "IDParada": "INT NOT NULL", #llave primaria
            "PRIMARY KEY": "(IDRuta, IDParada)"
        }

    def to_dict(self):
        return self.dict()
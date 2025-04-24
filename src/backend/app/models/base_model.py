from typing import Dict, Any
from pydantic import BaseModel

class DictModel(BaseModel):
    """Clase base que garantiza retorno como diccionario"""
    def to_dict(self) -> Dict[str, Any]:
        return self.dict()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(**data)
#La cree por si acaso 
"""from typing import Optional
from pydantic import BaseModel

class Incidence(BaseModel):
    __entity_name__ = "incidence"
    incidence_id: Optional[int] = None
    description: str
<<<<<<< HEAD
    status: str  # Relacionado con Ticket
    type: str
=======
    type: str
    status: str
>>>>>>> e4587d1 (changes to incidence logic)

    def to_dict(self):
        return self.model_dump()

    @classmethod
    def get_fields(cls):
        return {
            "incidence_id": "INTEGER PRIMARY KEY",
<<<<<<< HEAD
            "description": "TEXT NOT NULL",
            "status": "TEXT NOT NULL",
            "type": "TEXT"
        }"""
=======
            "description": "TEXT",
            "type": "TEXT",
            "status": "TEXT"
        }
>>>>>>> e4587d1 (changes to incidence logic)

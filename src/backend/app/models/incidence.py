from typing import Optional
from pydantic import BaseModel

class Incidence(BaseModel):
    __entity_name__ = "Incidencia"  # Nombre de la tabla en la base de datos
    ID: Optional[int] = None  # Clave primaria
    IDTicket: int = None  # Clave foránea al ticket
    Descripcion: str = None  # Descripción de la incidencia
    Tipo: str = None  # Tipo de incidencia
    IDUnidad: int = None  # Clave foránea a la unidad de transporte

    def to_dict(self):
        return self.model_dump()

    @classmethod
    def get_fields(cls):
        return {
            "ID": "INTEGER PRIMARY KEY",
            "IDTicket": "INTEGER NOT NULL",
            "Descripcion": "VARCHAR(100) NOT NULL",
            "Tipo": "VARCHAR(20) NOT NULL",
            "IDUnidad": "INTEGER NOT NULL"
        }

    @classmethod
    def ensure_table_exists(cls, cursor):
        """Verifica si la tabla existe y la crea si no existe."""
        table = cls.__entity_name__
        fields = cls.get_fields()
        columns = ", ".join(f"{k} {v}" for k, v in fields.items())
        sql = f"CREATE TABLE IF NOT EXISTS {table} ({columns})"
        cursor.execute(sql)
import pyodbc
from backend.app.core.config import Settings
from typing import Any
import os


class UniversalController:
    def __init__(self):
        try:
            settings = Settings()
            self.conn = pyodbc.connect(
    f"DRIVER={{SQL Server}};SERVER={settings.db_config['host']},1435;DATABASE={settings.db_config['dbname']};UID={settings.db_config['user']};PWD={settings.db_config['password']}"
)
            self.conn.autocommit = False  # Desactivar autocommit
            self.cursor = self.conn.cursor()
        except pyodbc.Error as e:
            raise ConnectionError(f"Error de conexión a la base de datos: {e}")

    def _get_table_name(self, obj: Any) -> str:
        if hasattr(obj, "__entity_name__"):
            return obj.__entity_name__
        elif hasattr(obj.__class__, "__entity_name__"):
            return obj.__class__.__entity_name__
        else:
            raise ValueError("El objeto o su clase no tienen definido '__entity_name__'.")

    def _ensure_table_exists(self, obj: Any):
        """Crea la tabla si no existe."""
        table = self._get_table_name(obj)
        fields = obj.get_fields()

        columns = []
        for k, v in fields.items():
            if k == "id":
                columns.append(f"{k} INT IDENTITY(1,1) PRIMARY KEY")
            else:
                columns.append(f"{k} {v}")

        sql = f"IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='{table}' AND xtype='U') CREATE TABLE {table} ({', '.join(columns)})"
        self.cursor.execute(sql)
        self.conn.commit()

    def drop_table(self, obj: Any) -> None:
        """Elimina la tabla de la base de datos."""
        table = self._get_table_name(obj)
        sql = f"IF EXISTS (SELECT * FROM sysobjects WHERE name='{table}' AND xtype='U') DROP TABLE {table}"
        self.cursor.execute(sql)
        self.conn.commit()

    def read_all(self, obj: Any) -> list[dict]:
        self._ensure_table_exists(obj)
        table = self._get_table_name(obj)
        self.cursor.execute(f"SELECT * FROM {table}")
        return [dict(zip([column[0] for column in self.cursor.description], row)) for row in self.cursor.fetchall()]

    def get_by_id(self, cls: Any, id_value: Any) -> Any | None:
        table = cls.__entity_name__
        sql = f"SELECT * FROM {table} WHERE id = ?"
        self.cursor.execute(sql, (id_value,))
        row = self.cursor.fetchone()

        return cls.from_dict(dict(zip([column[0] for column in self.cursor.description], row))) if row else None

    def add(self, obj: Any) -> Any:
        self._ensure_table_exists(obj)
        table = self._get_table_name(obj)
        data = obj.to_dict()

        if "id" in data:
            data.pop("id")

        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        values = list(data.values())

        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        try:
            self.cursor.execute(sql, values)
            self.conn.commit()
        except pyodbc.IntegrityError:
            self.conn.rollback()
            raise ValueError(f"Ya existe un objeto con la misma clave primaria en '{table}'.")
        except pyodbc.Error as e:
            self.conn.rollback()
            raise RuntimeError(f"Error al insertar datos en '{table}': {e}")

        return obj

    def update(self, obj: Any) -> Any:
        table = self._get_table_name(obj)
        data = obj.to_dict()

        if "id" not in data:
            raise ValueError("El objeto no tiene un campo 'id'.")

        assignments = ', '.join(f"{k} = ?" for k in data if k != "id")
        values = [v for k, v in data.items() if k != "id"]
        values.append(data["id"])

        sql = f"UPDATE {table} SET {assignments} WHERE id = ?"
        self.cursor.execute(sql, values)
        self.conn.commit()
        return obj

    def delete(self, obj: Any) -> bool:
        table = self._get_table_name(obj)
        data = obj.to_dict()

        if "id" not in data:
            raise ValueError("El objeto no tiene un campo 'id'.")

        sql = f"DELETE FROM {table} WHERE id = ?"
        self.cursor.execute(sql, (data["id"],))
        self.conn.commit()
        return True
    def get_by_unit(self, unit_id: int) -> list[dict]:
        sql = "SELECT * FROM mantenimiento WHERE id_unit = ?"
        try:
            self.cursor.execute(sql, (unit_id,))
            rows = self.cursor.fetchall()
            # Convertir cada fila en un diccionario utilizando los nombres de las columnas
            return [dict(zip([column[0] for column in self.cursor.description], row)) for row in rows]
        except pyodbc.Error as e:
            raise RuntimeError(f"Error al obtener registros de la unidad {unit_id}: {e}")
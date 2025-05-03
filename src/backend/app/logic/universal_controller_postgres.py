import os
import psycopg2
import psycopg2.extras
from backend.app.core.config import Settings
from typing import Any


class UniversalController:
    def __init__(self):
        try:
            settings = Settings()
            self.conn = psycopg2.connect(**settings.db_config)
            self.conn.autocommit = True
            self.cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        except psycopg2.Error as e:
            raise ConnectionError(f"Error de conexión a la base de datos: {e}")

    def _get_table_name(self, obj: Any) -> str:
        if hasattr(obj, "__entity_name__"):
            return obj.__entity_name__
        elif hasattr(obj.__class__, "__entity_name__"):
            return obj.__class__.__entity_name__
        else:
            raise ValueError("El objeto o su clase no tienen definido '__entity_name__'.")

    def _ensure_table_exists(self, obj: Any):
        """Crea la tabla si no existe (muy básico)."""
        table = self._get_table_name(obj)
        fields = obj.get_fields()
        columns = ", ".join(f"{k} {v}" for k, v in fields.items())
        sql = f"CREATE TABLE IF NOT EXISTS {table} ({columns})"
        self.cursor.execute(sql)

    def add(self, obj: Any) -> Any:
        self._ensure_table_exists(obj)
        table = self._get_table_name(obj)
        data = obj.to_dict()
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        values = list(data.values())
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        try:
            self.cursor.execute(sql, values)
        except psycopg2.IntegrityError:
            self.conn.rollback()
            raise ValueError(f"Ya existe un objeto con la misma clave primaria en '{table}'.")
        return obj

    def drop_table(self, obj: Any) -> None:
        """Elimina la tabla de la base de datos (solo para desarrollo)."""
        table = self._get_table_name(obj)
        sql = f'DROP TABLE IF EXISTS "{table}" CASCADE'
        self.cursor.execute(sql)


    def read_all(self, obj: Any) -> list[dict]:
        self._ensure_table_exists(obj)
        table = self._get_table_name(obj)
        self.cursor.execute(f"SELECT * FROM {table}")
        return self.cursor.fetchall()

    def get_by_id(self, cls: Any, id_value: Any) -> Any | None:
        table = cls.__entity_name__
        id_field = list(cls.model_fields.keys())[0]  # Asume que el primer campo es la clave primaria

        sql = f"SELECT * FROM {table} WHERE {id_field} = %s"
        self.cursor.execute(sql, (id_value,))
        row = self.cursor.fetchone()

        if row:
            return cls.from_dict(dict(row))
        return None

    def update(self, obj: Any) -> Any:
        self._ensure_table_exists(obj)
        table = self._get_table_name(obj)
        data = obj.to_dict()
        id_field = list(data.keys())[0]

        assignments = ', '.join(f"{k} = %s" for k in data if k != id_field)
        values = [v for k, v in data.items() if k != id_field]
        values.append(data[id_field])

        sql = f"UPDATE {table} SET {assignments} WHERE {id_field} = %s"
        self.cursor.execute(sql, values)

        return obj

    def delete(self, obj: Any) -> bool:
        self._ensure_table_exists(obj)
        table = self._get_table_name(obj)
        data = obj.to_dict()
        id_field = list(data.keys())[0]

        sql = f"DELETE FROM {table} WHERE {id_field} = %s"
        self.cursor.execute(sql, (data[id_field],))

        return True

    def clear_tables(self):
        """Vacía todas las tablas del esquema público."""
        self.cursor.execute("""
            SELECT tablename FROM pg_tables 
            WHERE schemaname = 'public'
        """)
        tables = self.cursor.fetchall()
        for table in tables:
            self.cursor.execute(f'DELETE FROM {table["tablename"]}')

import os
import sqlite3
from typing import Any

PATH = os.getcwd()
DIR_DATA = os.path.join(PATH, 'data')
DB_FILE = os.path.join(DIR_DATA, 'data.db')

class UniversalController:
    """Universal controller for CRUD operations using SQLite."""

    def __init__(self):
        """Initialize the database connection and cursor."""
        self.conn = sqlite3.connect(DB_FILE, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        self.cursor = self.conn.cursor()

    def _get_table_name(self, obj: Any) -> str:
        """Retrieve the table name based on the class name."""
        return obj.__class__.__name__.lower()

    def _ensure_table_exists(self, obj: Any):
        """Ensure that the table exists in the database; create it if it doesn't."""
        table = self._get_table_name(obj)
        fields = obj.get_fields()
        columns = ", ".join(f"{k} {v}" for k, v in fields.items())
        sql = f"CREATE TABLE IF NOT EXISTS {table} ({columns})"
        self.cursor.execute(sql)
        self.conn.commit()

    def add(self, obj: Any) -> Any:
        """Add a new object to the database."""
        self._ensure_table_exists(obj)
        table = self._get_table_name(obj)
        data = obj.to_dict()
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        values = list(data.values())
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

        try:
            self.cursor.execute(sql, values)
            self.conn.commit()
        except sqlite3.IntegrityError:
            raise ValueError(
                f"An object with the same primary key already exists in '{table}'."
            )

        return obj

    def read_all(self, obj: Any) -> list[dict]:
        """Retrieve all objects from a table."""
        self._ensure_table_exists(obj)
        table = self._get_table_name(obj)
        self.cursor.execute(f"SELECT * FROM {table}")
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]

    def get_by_id(self, cls: Any, id_value: Any) -> Any | None:
        """Retrieve an object by its ID."""
        dummy = cls.from_dict({k: None for k in cls.get_fields().keys()})
        self._ensure_table_exists(dummy)
        table = cls.__name__.lower()
        id_field = list(cls.get_fields().keys())[0]

        sql = f"SELECT * FROM {table} WHERE {id_field} = ?"
        self.cursor.execute(sql, (id_value,))
        row = self.cursor.fetchone()

        if row:
            return cls.from_dict(dict(row))

        return None

    def update(self, obj: Any) -> Any:
        """Update an existing object."""
        self._ensure_table_exists(obj)
        table = self._get_table_name(obj)
        data = obj.to_dict()
        id_field = list(data.keys())[0]

        assignments = ', '.join(
            f"{k} = ?" for k in data if k != id_field
        )
        values = [v for k, v in data.items() if k != id_field]
        values.append(data[id_field])

        sql = f"UPDATE {table} SET {assignments} WHERE {id_field} = ?"
        self.cursor.execute(sql, values)
        self.conn.commit()

        return obj

    def delete(self, obj: Any) -> bool:
        """Delete an object by its ID."""
        self._ensure_table_exists(obj)
        table = self._get_table_name(obj)
        data = obj.to_dict()
        id_field = list(data.keys())[0]

        sql = f"DELETE FROM {table} WHERE {id_field} = ?"
        self.cursor.execute(sql, (data[id_field],))
        self.conn.commit()

        return True

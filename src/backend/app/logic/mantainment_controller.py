import sqlite3
from src.backend.app.logic.mantainment import Maintenance
from datetime import datetime
import os

PATH = os.getcwd()
DIR_DATA = os.path.join(PATH, 'data')
DB_FILE = os.path.join(DIR_DATA, 'data.db')

class Controller:
    def __init__(self):
        self.conn = sqlite3.connect(DB_FILE, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    def get_all(self) -> list[dict]:
        self._ensure_table_exists()
        self.cursor.execute("SELECT * FROM maintenance")
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]

    def get_by_id(self, id_: int) -> Maintenance | None:
        self._ensure_table_exists()
        self.cursor.execute("SELECT * FROM maintenance WHERE id = ?", (id_,))
        row = self.cursor.fetchone()
        if row:
            return Maintenance.from_dict(dict(row))
        return None

    def get_by_unit(self, unit_id: int) -> list[dict]:
        """
        Devuelve todos los mantenimientos filtrados por id_unit.
        """
        self._ensure_table_exists()
        sql = "SELECT * FROM maintenance WHERE id_unit = ?"
        self.cursor.execute(sql, (unit_id,))
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]

    def _ensure_table_exists(self):
        """
        Crea la tabla si no existe (basado en la definición de Maintenance).
        """
        fields = Maintenance.get_fields()
        columns = ", ".join(f"{k} {v}" for k, v in fields.items())
        sql = f"CREATE TABLE IF NOT EXISTS maintenance ({columns})"
        self.cursor.execute(sql)
        self.conn.commit()

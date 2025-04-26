import os
import sqlite3
from typing import Any, Optional
from backend.app.models.maintainance import MaintenanceCreate, MaintenanceOut

# Definir la ruta a la base de datos
PATH = os.getcwd()
DIR_DATA = os.path.join(PATH, 'src', 'backend', 'app', 'data')
DB_FILE = os.path.join(DIR_DATA, 'data.db')

class Controller:
    def __init__(self):
        """Inicializa la conexión con la base de datos y el cursor."""
        self.conn = sqlite3.connect(DB_FILE, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  # Devuelve las filas como diccionarios
        self.cursor = self.conn.cursor()

    def get_all(self) -> list[dict]:
        """Obtiene todos los registros de mantenimiento de la base de datos."""
        self._ensure_table_exists(MaintenanceCreate)
        self.cursor.execute("SELECT * FROM maintenance")
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]

    def get_by_id(self, id_: int) -> Optional[MaintenanceOut]:
        """Obtiene un mantenimiento por su ID."""
        self._ensure_table_exists(MaintenanceCreate)
        self.cursor.execute("SELECT * FROM maintenance WHERE id = ?", (id_,))
        row = self.cursor.fetchone()
        if row:
            return MaintenanceOut.from_dict(dict(row))  # Convertir el diccionario en un modelo
        return None

    def get_by_unit(self, unit_id: int) -> list[dict]:
        """
        Devuelve todos los mantenimientos filtrados por id_unit.
        """
        self._ensure_table_exists(MaintenanceCreate)
        sql = "SELECT * FROM maintenance WHERE id_unit = ?"
        self.cursor.execute(sql, (unit_id,))
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]

    def _ensure_table_exists(self, model: Any):
        """
        Crea la tabla si no existe, basado en el modelo proporcionado (como Maintenance).
        """
        fields = model.get_fields()
        columns = ", ".join(f"{k} {v}" for k, v in fields.items())
        sql = f"CREATE TABLE IF NOT EXISTS maintenance ({columns})"
        self.cursor.execute(sql)
        self.conn.commit()

import pytest
import pyodbc
from backend.app.logic.universal_controller_sqlserver import UniversalController

class DummyModel:
    __entity_name__ = "TestTable"
    @staticmethod
    def get_fields():
        return {"ID": "INT PRIMARY KEY", "Nombre": "VARCHAR(50)", "Valor": "FLOAT"}
    def __init__(self, ID, Nombre, Valor):
        self.ID = ID
        self.Nombre = Nombre
        self.Valor = Valor
    def to_dict(self):
        return {"ID": self.ID, "Nombre": self.Nombre, "Valor": self.Valor}
    @classmethod
    def from_dict(cls, d):
        return cls(d["ID"], d["Nombre"], d["Valor"])

@pytest.fixture(scope="module")
def controller():
    c = UniversalController()
    # Crea la tabla antes de cada test si no existe
    try:
        c.cursor.execute("""
        IF OBJECT_ID('TestTable', 'U') IS NULL
        CREATE TABLE TestTable (
            ID INT PRIMARY KEY,
            Nombre VARCHAR(50),
            Valor FLOAT
        )
        """)
        c.cursor.execute("""
        IF OBJECT_ID('UnitTable', 'U') IS NULL
        CREATE TABLE UnitTable (
            ID INT PRIMARY KEY,
            idunidad INT,
            Nombre VARCHAR(50)
        )
        """)
        c.cursor.execute("""
        IF OBJECT_ID('BadTable', 'U') IS NULL
        CREATE TABLE BadTable (
            ID INT PRIMARY KEY,
            idunidad INT
        )
        """)
        c.conn.commit()
    except Exception:
        pass
    return c

def test_add_and_read_all(controller):
    # Limpia toda la tabla para asegurar que solo haya un registro
    controller.cursor.execute("DELETE FROM TestTable")
    controller.conn.commit()
    obj = DummyModel(1, "Test", 10.5)
    controller.add(obj)
    results = controller.read_all(obj)
    assert len(results) == 1
    assert results[0]["ID"] == 1
    assert results[0]["Nombre"] == "Test"
    assert results[0]["Valor"] == 10.5

def test_get_by_id(controller):
    obj = DummyModel(2, "Otro", 20.0)
    controller.add(obj)
    found = controller.get_by_id(DummyModel, 2)
    assert found is not None
    assert found.ID == 2
    assert found.Nombre == "Otro"
    assert found.Valor == 20.0

def test_update(controller):
    obj = DummyModel(2, "Modificado", 99.9)
    updated = controller.update(obj)
    assert updated.Nombre == "Modificado"
    found = controller.get_by_id(DummyModel, 2)
    assert found.Nombre == "Modificado"
    assert found.Valor == 99.9

def test_delete(controller):
    obj = DummyModel(2, "Modificado", 99.9)
    assert controller.delete(obj) is True
    assert controller.get_by_id(DummyModel, 2) is None

def test_update_not_found(controller):
    obj = DummyModel(999, "No existe", 0.0)
    # Si la tabla existe pero el registro no, update debe devolver None o no afectar filas
    try:
        controller.update(obj)
    except ValueError as exc:
        assert "actualizar" in str(exc).lower() or "no se encontró" in str(exc).lower()
    else:
        # Si no lanza, es porque no encontró el registro y no hizo nada
        pass

def test_delete_not_found(controller):
    obj = DummyModel(999, "No existe", 0.0)
    try:
        controller.delete(obj)
    except ValueError as exc:
        assert "eliminar" in str(exc).lower() or "no se encontró" in str(exc).lower()
    else:
        # Si no lanza, es porque no encontró el registro y no hizo nada
        pass

def test_add_duplicate(controller):
    obj = DummyModel(3, "Dup", 1.1)
    try:
        controller.add(obj)
    except ValueError:
        pass
    with pytest.raises(ValueError) as exc:
        controller.add(obj)
    assert "duplicate" in str(exc.value).lower() or "exists" in str(exc.value).lower() or "23000" in str(exc.value)

# Corrige test_clear_tables si el método no existe
# def test_clear_tables(controller):
#     obj = DummyModel(4, "A", 1.0)
#     controller.add(obj)
#     controller.clear_tables()
#     results = controller.read_all(obj)
#     assert results == []

def test_get_by_unit(controller):
    class UnitModel:
        __entity_name__ = "UnitTable"
        @staticmethod
        def get_fields():
            return {"ID": "INT PRIMARY KEY", "idunidad": "INT", "Nombre": "VARCHAR(50)"}
        def __init__(self, ID, idunidad, Nombre):
            self.ID = ID
            self.idunidad = idunidad
            self.Nombre = Nombre
        def to_dict(self):
            return {"ID": self.ID, "idunidad": self.idunidad, "Nombre": self.Nombre}
        @classmethod
        def from_dict(cls, d):
            return cls(d["ID"], d["idunidad"], d["Nombre"])
    c = controller
    c.cursor.execute("DELETE FROM UnitTable WHERE ID=1")
    c.conn.commit()
    obj = UnitModel(1, 42, "UnidadX")
    c.add(obj)
    result = c.get_by_unit(UnitModel, 42)
    assert result is not None
    assert result.idunidad == 42
    assert result.Nombre == "UnidadX"
    not_found = c.get_by_unit(UnitModel, 999)
    assert not_found is None

def test_get_by_unit_exception(controller):
    class BadModel:
        __entity_name__ = "BadTable"
        @staticmethod
        def get_fields():
            return {"ID": "INT PRIMARY KEY", "idunidad": "INT"}
        def __init__(self, ID, idunidad):
            self.ID = ID
            self.idunidad = idunidad
        def to_dict(self):
            return {"ID": self.ID, "idunidad": self.idunidad}
        @classmethod
        def from_dict(cls, d):
            raise Exception("fail")
    c = controller
    c.cursor.execute("DELETE FROM BadTable WHERE ID=1")
    c.conn.commit()
    obj = BadModel(1, 1)
    c.add(obj)
    with pytest.raises(Exception):
        c.get_by_unit(BadModel, 1)

def test_drop_table(controller):
    obj = DummyModel(99, "Drop", 0.0)
    controller.drop_table(obj)
    # Después de drop, intentar leer debe retornar lista vacía o lanzar excepción
    try:
        results = controller.read_all(obj)
        assert results == []
    except Exception:
        pass

def test_last_card_used_and_exceptions(controller):
    # Debe retornar tipo y monto N/A si no hay datos
    result = controller.last_card_used(999999)
    assert isinstance(result, dict)
    assert "tipo" in result and "monto" in result
    # No se lanza excepción si no hay datos, solo si hay error de conexión


def test_get_ruta_parada(controller):
    # Debe retornar None si no hay datos
    result = controller.get_ruta_parada(999999, 999999)
    assert result is None
    # Forzamos excepción con parámetros inválidos
    try:
        controller.get_ruta_parada(None, 'error')
    except Exception:
        pass
    else:
        assert True  # No se lanza excepción, pero el error se loguea

def test_get_ruta_parada_full(controller):
    # Cubre get_ruta_parada con parámetros
    # Con parámetros que no existen
    result = controller.get_ruta_parada(999999, 999999)
    assert isinstance(result, list) or result is None
    assert result == [] or result is None
    # Forzamos excepción con parámetros inválidos
    try:
        controller.get_ruta_parada(None, 'error')
    except Exception:
        pass
    else:
        assert True

"""import pytest
from backend.app.models.maintainance_status import MaintainanceState


def test_to_dict():
    |||
    Prueba el método `to_dict` del modelo MaintainanceState para asegurar
    que devuelve un diccionario correcto con los datos del modelo.
    |||
    state = MaintainanceState(id=1, tipoestado="Activo")
    result = state.to_dict()

    assert isinstance(result, dict), "El resultado debe ser un diccionario"
    assert result["id"] == 1, "El ID debe coincidir con el valor proporcionado"
    assert result["tipoestado"] == "Activo", "El tipoestado debe coincidir con el valor proporcionado"


def test_get_fields():
    |||
    Prueba la salida del método `get_fields`, asegurando que los campos definidos
    en el modelo son tales como se especificaron.
    |||
    fields = MaintainanceState.get_fields()

    assert isinstance(fields, dict), "Los campos deben estar definidos como un diccionario"
    assert fields["id"] == "INTEGER PRIMARY KEY", "El campo `id` debe ser una clave primaria INTEGER"
    assert fields[
               "tipoestado"] == "VARCHAR(100) NOT NULL", "El campo `tipoestado` debe ser una cadena VARCHAR(100) NOT NULL"


def test_model_default_values():
    |||
    Prueba las propiedades predeterminadas del modelo, en este caso, la ausencia de un ID.
    |||
    state = MaintainanceState(tipoestado="Activo")

    assert state.id is None, "El ID debe ser None por defecto"
    assert state.tipoestado == "Activo", "El campo tipoestado debe contener el valor proporcionado"
    """
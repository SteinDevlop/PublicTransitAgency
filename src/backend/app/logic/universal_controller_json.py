import os
import json
from typing import Any

PATH = os.getcwd()
DIR_DATA = PATH + '{0}data{0}'.format(os.sep)

class UniversalController:
    def __init__(self):
        self.file = '{0}{1}'.format(DIR_DATA, 'storage.json')
        if not os.path.exists(self.file):
            with open(self.file, 'w') as f:
                json.dump({}, f)

    def _get_entity_name(self, obj: Any) -> str:
        if hasattr(obj, "__entity_name__"):
            return getattr(obj, "__entity_name__")
        return obj.__class__.__name__.lower()


    def _get_id_field(self, obj_dict: dict) -> str:
        for key in obj_dict.keys():
            if key == "id" or key.endswith("_id") or key.endswith("idn"):
                return key
        raise ValueError("No se encontró un campo identificador (id, *_id o idn).")

    def _load_data(self):
        with open(self.file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _save_data(self, data: dict):
        with open(self.file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    def add(self, obj: Any):
        data = self._load_data()
        entity_name = self._get_entity_name(obj)
        obj_dict = obj.to_dict()
        id_field = self._get_id_field(obj_dict)

        if entity_name not in data:
            data[entity_name] = []

        for item in data[entity_name]:
            if item.get(id_field) == obj_dict.get(id_field):
                raise ValueError(f"{entity_name} con {id_field} = {obj_dict.get(id_field)} ya existe.")

        data[entity_name].append(obj_dict)
        self._save_data(data)
        return obj

    def read_all(self, obj: Any):
        data = self._load_data()
        entity_name = self._get_entity_name(obj)
        return data.get(entity_name, [])

    def get_by_id(self, obj_type: Any, id_value: Any):
        data = self._load_data()
        entity_name = obj_type.__name__.lower()
        items = data.get(entity_name, [])

        if not items:
            return None

        id_field = self._get_id_field(items[0])
        for item in items:
            if item.get(id_field) == id_value:
                return obj_type.from_dict(item)
        return None

    def update(self, obj: Any):
        data = self._load_data()
        entity_name = self._get_entity_name(obj)
        obj_dict = obj.to_dict()
        id_field = self._get_id_field(obj_dict)

        if entity_name not in data:
            raise ValueError(f"No hay datos para la entidad {entity_name}")

        for i, item in enumerate(data[entity_name]):
            if item.get(id_field) == obj_dict.get(id_field):
                data[entity_name][i] = obj_dict
                self._save_data(data)
                return obj
        raise ValueError(f"{entity_name} con {id_field} = {obj_dict.get(id_field)} no encontrado.")

    def delete(self, obj: Any):
        data = self._load_data()
        entity_name = self._get_entity_name(obj)
        obj_dict = obj.to_dict()
        id_field = self._get_id_field(obj_dict)

        if entity_name not in data:
            raise ValueError(f"No hay datos para la entidad {entity_name}")

        new_data = [item for item in data[entity_name] if item.get(id_field) != obj_dict.get(id_field)]
        data[entity_name] = new_data
        self._save_data(data)
        return True


        
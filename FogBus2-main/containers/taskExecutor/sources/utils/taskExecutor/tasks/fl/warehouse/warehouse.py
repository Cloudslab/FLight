"""
Collecting both data_warehouse & model_warehouse interface into a single class

"""

import uuid
from .data_warehouse import data_warehouse
from .model_warehouse import model_warehouse

data_storages = data_warehouse.data_accessory_name
data_storages_str = {"ram": data_storages.ram, "local_file": data_storages.local_file}
model_storages = model_warehouse.model_accessory_name
model_storages_str = {"ram": model_storages.ram, "local_file": model_storages.local_file, "ftp": model_storages.ftp}

class warehouse:
    def __init__(self):
        self._data_warehouse = data_warehouse()
        self._model_warehouse = model_warehouse()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            setattr(cls, "instance", super(warehouse, cls).__new__(cls))
        return getattr(cls, "instance")

    def set_model(self, model, model_id: str = None, storage: str = "ram"):
        storage_type = model_storages_str.get(storage, model_storages.ram)
        return self._set_model(model, model_id, storage_type)

    def _set_model(self, model, model_id: str = None, storage: model_storages = model_storages.ram):
        if not model_id: model_id = uuid.uuid1()
        actual_model_id = self._model_warehouse.set_model(model, model_id, storage)
        return actual_model_id

    def get_model(self, model_id: str):
        return self._model_warehouse.get_model(model_id)

    def set_data(self, data, data_id: str = None, storage: str = "ram"):
        storage_type = data_storages_str.get(storage, model_storages.ram)
        return self._set_data(data, data_id, storage_type)

    def _set_data(self, data, data_id: str = None, storage: data_storages = data_storages.ram):
        if not data_id: data_id = uuid.uuid1()
        actual_data_id = self._data_warehouse.set_data(data, data_id, storage)
        return actual_data_id

    def get_data(self, data_id: str):
        return self._data_warehouse.get_data(data_id)

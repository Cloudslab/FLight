"""
class provide getter & setter for model retrieval from different storage media

"""
from enum import Enum
from .Accessory import *


class model_warehouse:
    class model_accessory_name(Enum):
        ram = 1
        local_file = 2
        ftp = 3

    def __init__(self):
        self.id_to_storage = {}
        self.ram_storage = ram_accessory()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            setattr(cls, "instance", super(model_warehouse, cls).__new__(cls))
        return getattr(cls, "instance")

    def set_model(self, data, model_id: str, storage: model_accessory_name):
        result_model_id = None
        if storage == self.model_accessory_name.ram:
            result_model_id = self.ram_storage.set({"model": data}, model_id)
            self.id_to_storage[result_model_id] = self.model_accessory_name.ram
        return result_model_id

    def get_model(self, model_id: str):
        storage_type = self.id_to_storage.get(model_id, None)
        if storage_type == self.model_accessory_name.ram:
            return self.ram_storage.get({}, model_id)

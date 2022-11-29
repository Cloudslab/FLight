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
        self.local_file_storage = local_file_accessory()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            setattr(cls, "instance", super(model_warehouse, cls).__new__(cls))
        return getattr(cls, "instance")

    def set_model(self, data, model_id: str, storage: model_accessory_name):
        result_model_id = None
        if storage == self.model_accessory_name.ram:
            result_model_id = self.ram_storage.set({"model": data}, model_id)
            self.id_to_storage[result_model_id] = self.model_accessory_name.ram
        if storage == self.model_accessory_name.local_file:
            if type(data) is dict and "file_path" in data and "raw_data" in data:
                result_model_id = self.local_file_storage.set(data, model_id)
                self.id_to_storage[result_model_id] = self.model_accessory_name.local_file
        return result_model_id

    def get_model(self, model_id: str):
        storage = self.id_to_storage.get(model_id, None)
        if storage == self.model_accessory_name.ram:
            return self.ram_storage.get({}, model_id)
        if storage == self.model_accessory_name.local_file:
            return self.local_file_storage.get({}, model_id)

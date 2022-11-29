"""
class provide getter & setter for training data retrieval from different storage media

"""
from enum import Enum
from .Accessory import *

class data_warehouse:
    class data_accessory_name(Enum):
        ram = 1
        local_file = 2

    def __init__(self):
        self.id_to_storage = {}
        self.ram_storage = ram_accessory()
        self.local_file_storage = local_file_accessory()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            setattr(cls, "instance", super(data_warehouse, cls).__new__(cls))
        return getattr(cls, "instance")

    def set_data(self, data, data_id: str, storage: data_accessory_name):
        result_data_id = None
        if storage == self.data_accessory_name.ram:
            result_data_id = self.ram_storage.set({"data": data}, data_id)
            self.id_to_storage[result_data_id] = self.data_accessory_name.ram
        if storage == self.data_accessory_name.local_file:
            if type(data) is dict and "file_name" in data and "raw_data" in data:
                result_data_id = self.local_file_storage.set(data, data_id)
                self.id_to_storage[result_data_id] = self.data_accessory_name.local_file
        return result_data_id

    def get_data(self, data_id: str):
        storage = self.id_to_storage.get(data_id, None)
        if storage == self.data_accessory_name.ram:
            return self.ram_storage.get({}, data_id)
        if storage == self.data_accessory_name.local_file:
            return self.local_file_storage.get({}, data_id)

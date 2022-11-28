"""
class provide getter & setter for training data retrieval from different storage media

"""
from enum import Enum
from .Accessory import *

class data_warehouse:
    class data_accessory_name(Enum):
        ram = 1
        local_file_accessory = 2

    def __init__(self):
        self.ram_storage = ram_accessory()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            setattr(cls, "instance", super(data_warehouse, cls).__new__(cls))
        return getattr(cls, "instance")

    def set_data(self, data, data_id: str, storage: data_accessory_name):
        model_id = None
        if storage == self.data_accessory_name.ram:
            model_id = self.ram_storage.set({"data": data}, data_id)
        return model_id

    def get_data(self, data_id: str):
        pass

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
        self.ram_storage = ram_accessory()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            setattr(cls, "instance", super(model_warehouse, cls).__new__(cls))
        return getattr(cls, "instance")

    def set_model(self, data, model_id: str, storage: model_accessory_name):
        model_id = None
        if storage == self.model_accessory_name.ram:
            model_id = self.ram_storage.set({"model": model_id})
        return model_id

    def get_model(self, model_id: str):
        pass

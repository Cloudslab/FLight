"""
class provide getter & setter for model retrieval from different storage media

"""
from enum import Enum


class model_warehouse:
    class model_accessory_name(Enum):
        ram = 1
        local_file = 2
        ftp = 3

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            setattr(cls, "instance", super(model_warehouse, cls).__new__(cls))
        return getattr(cls, "instance")

    def set_model(self, data, model_id: str = None, storage: str = None):
        pass

    def get_model(self, model_id: str):
        pass

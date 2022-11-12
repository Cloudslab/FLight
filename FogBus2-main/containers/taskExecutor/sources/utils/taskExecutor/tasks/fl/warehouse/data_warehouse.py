"""
class provide getter & setter for training data retrieval from different storage media

"""
from enum import Enum


class data_warehouse:
    class data_accessory_name(Enum):
        ram = 1
        local_file_accessory = 2

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            setattr(cls, "instance", super(data_warehouse, cls).__new__(cls))
        return getattr(cls, "instance")

    def set_data(self, data, data_id: str, storage: data_accessory_name):
        pass

    def get_data(self, data_id: str):
        pass

"""
Collecting both data_warehouse & model_warehouse interface into a single class

"""

import uuid
from .data_warehouse import data_warehouse
from .model_warehouse import model_warehouse


class warehouse:
    def __init__(self):
        self.data_warehouse = data_warehouse()
        self.model_warehouse = model_warehouse()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            setattr(cls, "instance", super(warehouse, cls).__new__(cls))
        return getattr(cls, "instance")

    def set_model(self, model, model_id: str = None, storage: str = None):
        pass

    def get_model(self, model_id: str):
        pass

    def set_data(self, data, data_id: str = None, storage: str = None):
        pass

    def get_data(self, data_id: str):
        pass
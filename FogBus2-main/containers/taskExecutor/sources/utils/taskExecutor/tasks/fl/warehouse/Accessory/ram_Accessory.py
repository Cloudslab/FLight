""" This class represents data stored on RAM, everything stored in a dictionary"""

from .abstract_Accessory import abstract_accessory
from collections import defaultdict


class ram_accessory(abstract_accessory):
    def __init__(self):
        self._storage = defaultdict(None)

    def get(self, args: dict, data_id: str):
        return self._storage.get(data_id)

    def set(self, args: dict, data_id: str = None):
        if not data_id:
            data_id = self.get_new_id()
        if "data" in args:
            self._storage[data_id] = args["data"]
        if "model" in args:
            self._storage[data_id] = args["model"]
        return data_id

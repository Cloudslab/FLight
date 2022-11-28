""" This class represents data stored on RAM, everything stored in a dictionary"""

from .abstract_Accessory import abstract_accessory
from collections import defaultdict
import uuid


class ram_accessory(abstract_accessory):
    def __init__(self):
        self._storage = defaultdict(None)

    def get(self, args: dict, data_id: uuid.UUID):
        return self._storage.get(uuid)

    def set(self, args: dict, data_id: uuid.UUID = None):
        if data_id:
            data_id = self.get_new_id()
        if "data" in args:
            self._storage[data_id] = args["data"]
        if "model" in args:
            self._storage[data_id] = args["model"]

""" Accessory that every other accessory should follow """
import uuid
from abc import ABC, abstractmethod
from uuid import uuid1

class abstract_accessory(ABC):

    @abstractmethod
    def set(self, args: dict, data_id: str = None):
        pass

    @abstractmethod
    def get(self, args: dict, data_id: str):
        pass

    @staticmethod
    def get_new_id():
        return str(uuid1())

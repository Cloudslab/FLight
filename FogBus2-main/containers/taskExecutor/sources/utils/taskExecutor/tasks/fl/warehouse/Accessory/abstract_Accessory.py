""" Accessory that every other accessory should follow """

from abc import ABC, abstractmethod
from uuid import uuid1

class abstract_accessory(ABC):

    @abstractmethod
    def set(self, args: dict):
        pass

    @abstractmethod
    def get(self, args: dict):
        pass

    @staticmethod
    def get_new_id():
        return uuid1()

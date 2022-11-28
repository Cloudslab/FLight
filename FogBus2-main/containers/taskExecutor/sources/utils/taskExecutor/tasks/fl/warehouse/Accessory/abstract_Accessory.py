""" Accessory that every other accessory should follow """

from abc import ABC, abstractmethod


class abstract_accessory(ABC):

    @abstractmethod
    def set(self, args: dict):
        pass

    @abstractmethod
    def get(self, args: dict):
        pass

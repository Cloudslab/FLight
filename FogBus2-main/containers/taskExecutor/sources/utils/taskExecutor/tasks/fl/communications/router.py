"""This is the class used for communication between nodes"""

from .message_sender import message_sender
from .message_receiver import message_receiver


class router:

    def __init__(self, sender_address, receiver_address, name="default"):
        self._message_sender, self.sender_address = self.try_address(message_receiver, sender_address)
        self._message_receiver, self.receiver_address = self.try_address(receiver_address, receiver_address)
        self.set_default_router(name, self)

    @classmethod
    def set_default_router(cls, name, target_router):
        setattr(cls, name, target_router)

    @classmethod
    def get_router(cls, name):
        if hasattr(cls, name):
            return getattr(cls, name)
        else:
            return None

    @classmethod
    def get_default_router(cls):
        return cls.get_router("default")

    @staticmethod
    def try_address(obj_to_be_construct, address, retries=3):
        ip, port = address
        try:
            obj = obj_to_be_construct(address)
            return address, obj
        except Exception as e:
            return router.try_address(obj_to_be_construct, (ip, port+1), retries - 1)


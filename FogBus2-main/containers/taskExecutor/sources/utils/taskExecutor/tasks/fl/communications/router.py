"""This is the class used for communication between nodes"""

from .message_sender import message_sender
from .message_receiver import message_receiver


class router:
    def __init__(self, receiver_address=("127.0.0.1", 12345)):
        self._message_receiver, self.message_receiver_address = router.try_address(message_receiver, receiver_address)
        self._message_sender, _ = router.try_address(message_sender, self.message_receiver_address)
        self._message_receiver.start()
        self._message_sender.start()
        if not hasattr(router, "default_router"):
            setattr(router, "default_router", self)

    def send(self, address_to, event, data, reply_address=None):
        self._message_sender.send(address_to, event, data, reply_address)

    @staticmethod
    def try_address(obj_to_be_construct, address, retries=3):
        ip, port = address
        try:
            obj = obj_to_be_construct(address)
            return obj, address
        except Exception as e:
            return router.try_address(obj_to_be_construct, (ip, port+1), retries - 1)

    @classmethod
    def get_default_router(cls, router_name="default_router"):
        if not hasattr(router, router_name) or not isinstance(getattr(router, router_name)):
            router()
            router_name = "default_router"
        return getattr(router, router_name)

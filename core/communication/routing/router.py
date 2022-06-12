"""
A routing is the singleton class which hold a communicator (../utils/component/communicator), it is expected that
all incoming and outgoing messages are through this class. This class is created instead of using communicator directly
to leave place for future extension.
"""
from abc import ABC

from ..utils.component.communicator import Communicator
from ..utils.component.communicator import ComponentRole
from ..utils.types.basic.address import Address
from ..utils.connection.message.received import MessageReceived
from typing import Tuple

from ..utils.connection.message.received import MessageReceived
from ..utils.connection.message.toSend import MessageToSend
from ..utils.types.message.type import MessageType
from ..utils.types.component.identitySerializable import Component

# ToDo: read from .env
ADDRESS: Address = ["127.0.0.1", 5000]
PORT_RANGE = [5000, 5001]
LOG_LVL = 0
MASTER_ADDR = ["127.0.0.1", 5000]
RL_ADDR = ["127.0.0.1", 5000]


class Router:
    class _Communicator(Communicator, ABC):
        def handleMessage(self, message: MessageReceived):
            # ToDo: add a dispatcher here
            self.debugLogger.warning("----------------------------")
            self.debugLogger.warning(message.toDict())

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Router, cls).__new__(cls)
            cls.instance.communicator = \
                Router._Communicator(ComponentRole.DEFAULT, ADDRESS, PORT_RANGE, LOG_LVL, MASTER_ADDR, RL_ADDR)

        return cls.instance

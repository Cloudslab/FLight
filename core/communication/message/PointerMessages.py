"""
Messages required for Pointer (/ml/Pointer.py)

"""

from ..utils.connection.message.toSend import MessageToSend
from ..utils.types import MessageType, Address, Component
from ...ml.Pointer import Pointer
from enum import Enum


# after whatever object created, we wish to pass the pointer to remote interested site, or we want to use it to access
# remote object
class PointerMessage(MessageToSend):
    class purpose(Enum):
        INIT = 1
        RETRIEVE = 2

    def __init__(self, pointer: Pointer, purpose: purpose):
        super().__init__(MessageType.NONE, {"pointer": pointer, "purpose": purpose}, Component(pointer.address))

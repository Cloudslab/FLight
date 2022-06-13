"""
Messages required for Pointer (/ml/Pointer.py)

"""

from ..utils.connection.message.toSend import MessageToSend
from ..utils.types import MessageType, Address, Component
from ...ml.Pointer import Pointer


# after whatever object created, we wish to pass the pointer to remote interested site
class PointerMessage(MessageToSend):
    def __init__(self, pointer: Pointer, dest_addr):
        super().__init__(MessageType.NONE, {"id": "pointer_give", "pointer": pointer.__dict__}, Component(dest_addr))


# we want to use the pointer to retrieve remote data, also provides which object from ourselves interested in this data
class PointerMessage_RETRIEVE(MessageToSend):
    def __init__(self, pointer: Pointer, call_back_pointer: Pointer):
        super().__init__(MessageType.NONE, {"id": "pointer_ask", "pointer": pointer.__dict__,
                                            "call_back_pointer": call_back_pointer.__dict__},
                         Component(pointer.address))


class PointerDataMessage(MessageToSend):
    def __init__(self, data, call_back_pointer: Pointer):
        data = data.__dict__ if data is not None else {}
        super().__init__(MessageType.NONE, {"id": "pointer_data_load",
                                            "call_back_pointer": call_back_pointer.__dict__,
                                            "data": data},
                         Component(call_back_pointer.address))

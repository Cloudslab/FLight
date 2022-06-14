"""
Messages required for LinearRegressionPointer (/ml/model/LinearRegressionPointer.py)

"""

from ..utils.connection.message.toSend import MessageToSend
from ..utils.types import MessageType, Address, Component


class LinearRegressionAckMessage(MessageToSend):
    def __init__(self, pointer: 'Pointer', call_back_pointer: 'Pointer'):
        super().__init__(MessageType.NONE, {"id": "pointer_ack", "pointer": pointer.toDict(),
                                            "call_back_pointer": call_back_pointer.toDict()},
                         Component(pointer.address))

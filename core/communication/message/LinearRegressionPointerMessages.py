"""
Messages required for LinearRegressionPointer (/ml/model/LinearRegressionPointer.py)

"""

from ..utils.connection.message.toSend import MessageToSend
from ..utils.types import MessageType, Address, Component


class LinearRegressionAckMessage(MessageToSend):
    def __init__(self, pointer: 'Pointer', call_back_pointer: 'Pointer'):
        super().__init__(MessageType.NONE, {"id": "lr_ack", "pointer": pointer.toDict(),
                                            "call_back_pointer": call_back_pointer.toDict()},
                         Component(pointer.address))


class LinearRegressionStep(MessageToSend):
    def __init__(self, pointer: 'Pointer', call_back_pointer: 'Pointer'):
        super().__init__(MessageType.NONE, {"id": "lr_step", "pointer": pointer.toDict(),
                                            "call_back_pointer": call_back_pointer.toDict()},
                         Component(pointer.address))


class LinearRegressionFetchServer(MessageToSend):
    def __init__(self, pointer: 'Pointer', call_back_pointer: 'Pointer'):
        super().__init__(MessageType.NONE, {"id": "lr_fetch_server", "pointer": pointer.toDict(),
                                            "call_back_pointer": call_back_pointer.toDict()},
                         Component(pointer.address))


class LinearRegressionServerData(MessageToSend):
    def __init__(self, pointer: 'Pointer', call_back_pointer: 'Pointer', model: dict, flag: str):
        super().__init__(MessageType.NONE, {"id": "lr_server_data", "pointer": pointer.toDict(),
                                            "call_back_pointer": call_back_pointer.toDict(),
                                            "model": model,
                                            "flag": flag},
                         Component(pointer.address))


class LinearRegressionClientData(MessageToSend):
    def __init__(self, pointer: 'Pointer', call_back_pointer: 'Pointer', model: dict, flag: str):
        super().__init__(MessageType.NONE, {"id": "lr_client_data", "pointer": pointer.toDict(),
                                            "call_back_pointer": call_back_pointer.toDict(),
                                            "model": model,
                                            "flag": flag},
                         Component(pointer.address))

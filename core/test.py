from communication.utils.component.communicator import Communicator
from communication.utils.component.communicator import ComponentRole
from communication.utils.types.basic.address import Address
from communication.utils.connection.message.received import MessageReceived
from typing import Tuple, Dict

from communication.utils.connection.message.received import MessageReceived
from communication.utils.connection.message.toSend import MessageToSend
from communication.utils.types.message.type import MessageType
from communication.utils.types.component.identitySerializable import Component

from communication.routing import Router
from communication.utils.types import MessageSubType, MessageSubSubType


class aaaaa(MessageToSend):
    def __init__(self,
            messageType: MessageType,
            data: Dict,
            destination: Component,
            messageSubType: MessageSubType = MessageSubType.NONE,
            messageSubSubType: MessageSubSubType = MessageSubSubType.NONE):
        super().__init__(messageType, data, destination, messageSubType, messageSubSubType)
        self.x = 1

class test:
    def __init__(self):
        self.x = 1
        self.y = 2

if __name__ == "__main__":
    destination = Component(["127.0.0.1", 5000])
    message_to_send = aaaaa(
        MessageType.NONE,
        data={
            "w": 0,
            "bias": 0,
            "test": test().__dict__
        },
        destination=destination

    )

    r = Router()
    r.communicator.sendMessage(message_to_send)
    print(message_to_send.__class__)
    print("HW")
from communication.utils.component.communicator import Communicator
from communication.utils.component.communicator import ComponentRole
from communication.utils.types.basic.address import Address
from communication.utils.connection.message.received import MessageReceived
from typing import Tuple

from communication.utils.connection.message.received import MessageReceived
from communication.utils.connection.message.toSend import MessageToSend
from communication.utils.types.message.type import MessageType
from communication.utils.types.component.identitySerializable import Component

from communication.routing import Router

if __name__ == "__main__":
    destination = Component(["127.0.0.1", 5000])
    message_to_send = MessageToSend(
        MessageType.NONE,
        data={
            "w": 0,
            "bias": 0
        },
        destination=destination

    )

    r = Router()
    r.communicator.sendMessage(message_to_send)
    print("HW")
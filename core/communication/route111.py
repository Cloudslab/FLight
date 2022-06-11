from utils.component.communicator import Communicator
from utils.component.communicator import ComponentRole
from utils.types.basic.address import Address
from utils.connection.message.received import MessageReceived
from typing import Tuple

from utils.connection.message.received import MessageReceived
from utils.connection.message.toSend import MessageToSend
from utils.types.message.type import MessageType
from utils.types.component.identitySerializable import Component

class FlBasicCommunicator(Communicator):

    def __int__(self,
                role: ComponentRole,
                addr: Address,
                portRange: Tuple[int, int],
                logLevel: int,
                masterAddr: Address,
                remoteLoggerAddr: Address,
                ignoreSocketError: bool = False):

        super.__init__(role, addr, portRange, logLevel, masterAddr, remoteLoggerAddr, ignoreSocketError)
        self.x = 1

    def handleMessage(self, message: MessageReceived):
        self.debugLogger.warning("---------------------------------------------------")
        self.debugLogger.warning(message.toDict())

if __name__ == "__main__":

    componentRole = ComponentRole.DEFAULT
    my_address = ["10.211.55.4", 5000]
    port_range = [5000,5001]
    log_lvl = 0

    addr_holder = ["0.0.0.0", 80]
    master_addr = remote_logger_addr = addr_holder

    c = FlBasicCommunicator(componentRole, my_address, port_range, log_lvl, master_addr, remote_logger_addr)

    #from socket import *
    #s = socket(AF_INET, SOCK_STREAM)

    destination = Component(["10.211.55.4", 5000])

    import time
    time.sleep(2)
    message_to_send = MessageToSend(
        MessageType.NONE,
        data={
            "w":0,
            "bias":0
        },
        destination=destination

    )

    c.sendMessage(message_to_send)


    print("HW")



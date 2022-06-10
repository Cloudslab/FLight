from utils.component.communicator import Communicator
from utils.component.communicator import ComponentRole
from utils.types.basic.address import Address
from utils.connection.message.received import MessageReceived
from typing import Tuple

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

    def handlerMessage(self, message: MessageReceived):
        print(message.toDict())


if __name__ == "__main__":

    componentRole = ComponentRole.DEFAULT
    my_address = ["10.211.55.4", 5000]
    port_range = [5000,5001]
    log_lvl = 0

    addr_holder = ["0.0.0.0", 5000]
    master_addr = remote_logger_addr = addr_holder

    c = FlBasicCommunicator(componentRole, master_addr, port_range, log_lvl, addr_holder, remote_logger_addr)




    print("HW")



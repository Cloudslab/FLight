from utils.component.communicator import Communicator
from utils.component.communicator import ComponentRole
from utils.types.basic.address import Address
from typing import Tuple

if __name__ == "__main__":

    componentRole = ComponentRole.DEFAULT
    my_address = ["10.211.55.4", 5000]
    port_range = [5000,5001]
    log_lvl = 0

    addr_holder = ["0.0.0.0", 5000]
    master_addr = remote_logger_addr = addr_holder

    c = Communicator(componentRole, master_addr, port_range, log_lvl, addr_holder, remote_logger_addr)

    print("HW")
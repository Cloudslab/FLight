from threading import Thread

from federated_learning.federaed_learning_model.base import base_model
from federated_learning.federaed_learning_model.datawarehouse import model_warehouse
from federated_learning.communicate.router import router_factory, ftp_server_factory
from federated_learning.handler.relationship_handler import relationship_handler
from federated_learning.handler.model_communication_handler import model_communication_handler
from federated_learning.handler.remote_call_handler import remote_call_handler

import time

model_handbook = {
    "_bas": base_model
}

import glob

if __name__ == "__main__":
    addr, r = router_factory.get_router(("127.0.0.1", 12345))
    ftp_addr, ftp_server = ftp_server_factory.get_ftp_server(("127.0.0.1", 12345))
    r.add_handler("relation__", relationship_handler())
    r.add_handler("communicat", model_communication_handler())
    r.add_handler("cli_step__", remote_call_handler())
    model = base_model()
    for i in range(3):
        model.add_client(addr)
    while (len(model.client) + len(model.server) + len(model.peer)) < 3:
        time.sleep(0.01)
    for i in range(10):
        print(i)
        for cli in model.get_client():
            if model.eligible_client(cli):
                model.step_client(cli)

        while not model.can_federate():
            time.sleep(0.01)
        model.federate()

    m = model_warehouse()
    print(123)
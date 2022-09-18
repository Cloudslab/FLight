from threading import Thread

from federated_learning.federaed_learning_model.base import base_model
from federated_learning.federaed_learning_model.datawarehouse import model_warehouse
from federated_learning.communicate.router import router_factory, ftp_server_factory
from federated_learning.handler.relationship_handler import relationship_handler
from federated_learning.handler.model_communication_handler import model_communication_handler

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
    model = base_model()
    model.add_client(addr)
    model.add_client(addr)
    model.add_client(addr)
    while (len(model.client) + len(model.server) + len(model.peer)) < 3:
        time.sleep(0.01)

    for cli in model.get_client():
        model.fetch_client(cli)

    while len(model.get_remote_fetch_model_credential("c")) < 3:
        time.sleep(0.01)

    for ptr in model.get_remote_fetch_model_credential("c").keys():
        model.download_model(ptr, "c")


    m = model_warehouse()
    print(1234)